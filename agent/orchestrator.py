"""Sequential, restartable research loop composed from the agent components."""

from dataclasses import asdict, dataclass, field, replace
import hashlib
import json
import math
import os
from pathlib import Path
import re
import time
import uuid

from agent.budget import BudgetClient, BudgetExhausted, RunBudget
from agent.diagnostics import sanitize
from agent.graph.memory import ExplorationMemory, MemoryContext
from agent.graph.node import EdgeAction, MetricResult, NodeStatus, RecoveryEvent, SearchNode
from agent.graph.reflection import ReflectionEngine
from agent.graph.tree import SearchConfig, SearchTree
from agent.improvement import ImprovementEngine, ProposalError
from agent.llm.client import LLMError
from agent.log import RunLogger
from agent.mutation.mutation import CodeMutationEngine
from agent.mutation.parser import EditError
from agent.mutation.prompts import EditFeedback
from agent.recovery import RecoveryEngine
from agent.reporting import FinalTestResult, build_report, write_report
from agent.run_state import RunStore
from agent.sandbox.git_driver import GitDriver
from agent.sandbox.protocol import STARTER
from agent.sandbox.runner import Runner, RunResult
from agent.sandbox.environment import pinned_requirements
from agent.sandbox.lease import file_lease


ROOT = Path(__file__).resolve().parents[1]
FILES = ("config.py", "features.py", "model.py", "train.py", "requirements.txt")
CONSTRAINTS = (
    "Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 "
    "evaluation, and test isolation. Do not read test data during search. "
    "Keep the train.train and model.load_predictor contracts in the supplied files. "
    "Do not modify the agent, evaluator, dataset, shared environments, or external files. "
    "Only edit the supplied files. Keep artifacts outside source."
)


@dataclass(frozen=True)
class RunConfig:
    run_dir: str
    data_dir: str | None = None
    template_dir: str = str(ROOT / "workspace_template")
    environment_dir: str = str(ROOT / "storage" / "environments")
    wheelhouse: str | None = None
    search: SearchConfig = field(default_factory=SearchConfig)
    candidate_timeout_s: float = 1800
    final_reserve_s: float = 120
    max_repairs: int = 3
    proposal_attempts: int = 2
    mutation_attempts: int = 4
    proposal_tokens: int = 4096
    mutation_tokens: int = 8192
    max_prompt_chars: int = 200000
    max_llm_calls: int = 200
    reflection_enabled: bool = True
    breakthrough_delta: float = .01
    collapse_delta: float = -.01

    def __post_init__(self):
        for name in ("run_dir", "template_dir", "environment_dir", "data_dir", "wheelhouse"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, str(Path(value).resolve()))
        for name in ("proposal_attempts", "mutation_attempts", "proposal_tokens",
                     "mutation_tokens", "max_prompt_chars", "max_llm_calls"):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if type(self.max_repairs) is not int or self.max_repairs < 0:
            raise ValueError("max_repairs must be nonnegative")
        for name in ("candidate_timeout_s", "final_reserve_s", "breakthrough_delta", "collapse_delta"):
            value = getattr(self, name)
            if isinstance(value, bool) or not math.isfinite(value):
                raise ValueError(f"Invalid {name}")
        if (self.candidate_timeout_s <= 0 or not 0 <= self.final_reserve_s < self.search.max_wall_clock_s
                or self.breakthrough_delta <= 0 or self.collapse_delta >= 0):
            raise ValueError("Invalid timeout, reserve, or reflection thresholds")


def _hash_files(paths):
    result = {}
    for path in sorted(paths):
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        result[str(path)] = digest.hexdigest()
    return result


class Orchestrator:
    """Own one run; injected clients/runners support offline lifecycle tests.

    Candidate code is trusted local code: the runner is NOT a security sandbox.
    State is durable at stage boundaries; interrupted model calls can be billed
    again, but consume persisted retry allowances. No credentials are persisted.
    """

    def __init__(self, config: RunConfig, *, client=None, runner=None, splits=None):
        if (config.data_dir is None) == (splits is None):
            raise ValueError("Supply exactly one of config.data_dir or injected splits")
        self.config = config
        self.directory = Path(config.run_dir)
        self.store = RunStore(self.directory)
        self.git = GitDriver(self.directory / "workspace")
        self.runner = runner if runner is not None else Runner(
            storage_dir=self.directory / "executions", checkpoint_dir=self.directory / "checkpoints",
            environment_dir=config.environment_dir, wheelhouse=config.wheelhouse,
            log_path=self.directory / "events.jsonl")
        self.raw_client = client
        self.splits = splits
        self.tree = None
        self.memory = ExplorationMemory()
        self.state = None
        self.logger = RunLogger(self.directory / "events.jsonl")

    def _fingerprint(self):
        protocol = _hash_files([STARTER / "data.py", STARTER / "evaluate.py",
                                ROOT / "agent/sandbox/protocol.py"])
        if self.splits is not None:
            data = hashlib.sha256(json.dumps(self.splits, sort_keys=True, allow_nan=False).encode()).hexdigest()
        else:
            paths = list(Path(self.config.data_dir).rglob("*.csv"))
            if not paths:
                raise ValueError("Data directory contains no CSV files")
            data = _hash_files(paths)
        return hashlib.sha256(json.dumps({"protocol": protocol, "data": data}, sort_keys=True).encode()).hexdigest()

    def _bind(self):
        self.budget = RunBudget(self.state["started_at"], self.config.search.max_wall_clock_s,
                                self.config.final_reserve_s)
        self.client = BudgetClient(self.raw_client, self.budget, self.config.max_prompt_chars,
                                   on_request=self._model_request, on_response=self._model_response,
                                   audit=self._audit,
                                   profile=lambda: 'high' if self.state['stage'] == 'propose' else 'low')
        self.improvement = ImprovementEngine(self.client)
        self.mutation = CodeMutationEngine(self.client)
        self.reflection = ReflectionEngine(self.client)

    def _audit(self, event, **data):
        config = getattr(self.client.client, 'config', None)
        self.logger.secrets = (getattr(config, 'api_key', ''),)
        context = dict(stage=self.state['stage'], node_id=self.state.get('active'),
                       call_id=self.state['llm_calls'], attempts=self.state.get('attempts'))
        error = data.pop('error', None)
        if error is not None:
            self.logger.exception(event, error, component='orchestrator', run_id=self.state['run_id'], **context, **data)
        else:
            self.logger.diagnostic(event, component='orchestrator', run_id=self.state['run_id'], **context, **data)

    def _model_request(self):
        if self.state["llm_calls"] >= self.config.max_llm_calls:
            raise BudgetExhausted("Model call budget exhausted")
        self.state["llm_calls"] += 1
        self._save("model_request_started", call_id=self.state["llm_calls"])

    def _model_response(self, response):
        if response.usage is None:
            self.state["responses_without_usage"] += 1
        else:
            self.state["reported_tokens"] += response.usage.total_tokens
        finish_reason = response.finish_reason
        if finish_reason is not None and finish_reason not in {
                "stop", "length", "max_tokens", "content_filter", "tool_calls", "function_call"}:
            finish_reason = "other"
        self._save("model_response_received", call_id=self.state["llm_calls"],
                   elapsed_s=self.client.last_elapsed_s,
                   token_usage=asdict(response.usage) if response.usage is not None else None,
                   finish_reason=finish_reason)

    def _save(self, reason, *, attempt=None, call_id=None, elapsed_s=None, token_usage=None,
              finish_reason=None, execution_id=None):
        """Publish a checkpoint and log only bounded operational metadata."""
        self.store.save(self.state, self.tree, self.memory)
        details = {"reason": reason}
        stage = self.state["stage"]
        if attempt is None and stage in ("propose", "mutate"):
            attempt = self.state.get("attempts", {}).get("proposal" if stage == "propose" else "mutation")
        elif attempt is None and stage == "repair" and self.state.get("active"):
            attempt = len(self._node().recovery_events)
        elif attempt is None and stage == "reflect" and self.state.get("reflection_attempted"):
            attempt = 1
        if attempt:
            details["attempt"] = attempt
        if call_id is not None:
            details["call_id"] = call_id
        if reason == "model_response_received":
            details.update(elapsed_s=elapsed_s, token_usage=token_usage, finish_reason=finish_reason)
        if execution_id is not None:
            details["execution_id"] = execution_id
        self.logger.emit("stage.saved", component="orchestrator", run_id=self.state["run_id"],
                         stage=stage, node_id=self.state.get("active"), **details)

    def _stage(self, stage):
        if stage != self.state["stage"]:
            self.state.pop("edit_retry", None)
        self.state["stage"] = stage
        self._save("stage_entered")

    def _edit_feedback(self):
        saved = self.state.get("edit_retry")
        return EditFeedback(**saved) if saved is not None else None

    def _edit_rejected(self, exc):
        # Keep the latest rejection across restarts without persisting credentials.
        # The source snapshot is untouched, so a correction must repeat all edits.
        config = getattr(self.client.client, "config", None)
        self.state["edit_retry"] = sanitize(
            asdict(EditFeedback(str(exc), exc.rejected_output)),
            (getattr(config, "api_key", ""),),
        ) if exc.rejected_output else None
        self._save("edit_output_rejected")
        self._audit("output.rejected", error=exc)

    def run(self):
        with self.store.lock():
            if any(p.name != "run.lock" for p in self.directory.iterdir()):
                raise ValueError("Run directory is not empty; resume it or use a new directory")
            self.state = dict(version=1, run_id=uuid.uuid4().hex, config=asdict(self.config),
                              started_at=time.time(), stage="genesis_prepare", active=None,
                              artifacts={}, execution=None, stop_reason=None, final_test=None,
                              selected=None, diagnostic="", attempts={}, paused_error=None,
                              llm_calls=0, reported_tokens=0, responses_without_usage=0)
            self.state["protocol_id"] = self._fingerprint()
            self._bind()
            self._save("stage_entered")
            return self._drive()

    @classmethod
    def resume(cls, run_dir, *, client=None, runner=None, splits=None):
        store = RunStore(run_dir)
        with store.lock():
            state, tree, memory = store.load()
            raw = dict(state["config"])
            raw["search"] = SearchConfig(**raw["search"])
            config = RunConfig(**raw)
            if Path(config.run_dir) != store.directory:
                raise ValueError("Run directory differs from the saved location")
            obj = cls(config, client=client, runner=runner, splits=splits)
            obj.state, obj.tree, obj.memory = state, tree, memory
            obj._bind()
            if state["stage"] != "done" and obj._fingerprint() != state["protocol_id"]:
                raise ValueError("Dataset or evaluation protocol changed; refusing to resume")
            obj.state["paused_error"] = None
            return obj._drive()

    def _drive(self):
        try:
            while self.state["stage"] != "done":
                stage_started = time.monotonic()
                previous_stage = self.state['stage']
                self._audit('stage.started', state=self.state)
                getattr(self, "_" + self.state["stage"])()
                self._audit('stage.finished', previous_stage=previous_stage,
                            elapsed_s=time.monotonic() - stage_started, state=self.state)
            return json.loads((self.directory / "report.json").read_text(encoding="utf-8"))
        except Exception as exc:
            self._audit('run.failed', error=exc)
            # Never publish partially changed in-memory state after a failed
            # transition; retain the last successfully published generation.
            self.state, self.tree, self.memory = self.store.load()
            self.state["paused_error"] = type(exc).__name__
            self._save("run_paused")
            raise

    def _redact(self, text):
        text = str(text)
        for name, value in os.environ.items():
            if len(value) >= 6 and re.search(r"key|token|secret|password", name, re.I):
                text = text.replace(value, "[REDACTED]")
        config = getattr(self.client.client, "config", None)
        if config is not None and getattr(config, "api_key", ""):
            text = text.replace(config.api_key, "[REDACTED]")
        text = re.sub(r"(?i)(bearer\s+)[^\s]+", r"\1[REDACTED]", text)
        text = re.sub(r"(?i)((?:api[_-]?key|token|password|secret)\s*[:=]\s*)\S+", r"\1[REDACTED]", text)
        return "\n".join(text.splitlines()[-10:])[-2400:] or "Execution failed without diagnostic output"

    def _diagnostics(self, result):
        pieces = [result.error or result.status]
        for name in ("train.stderr.log", "predict.stderr.log"):
            path = Path(result.artifact_dir) / name
            if path.exists():
                with path.open("rb") as stream:
                    stream.seek(0, 2)
                    stream.seek(max(0, stream.tell() - 8192))
                    pieces.append(stream.read().decode("utf-8", errors="replace"))
        return self._redact("\n".join(pieces))

    def _execute(self, node_id, *, final=False):
        """Recover completed result.json before scheduling a new execution ID."""
        pending = self.state["execution"]
        if pending is not None:
            path = Path(self.runner.storage_dir) / pending["id"] / "result.json"
            if path.exists():
                raw = json.loads(path.read_text(encoding="utf-8"))
                if (raw["checkpoint_path"] != pending["checkpoint"]
                        or raw.get("split", "test" if final else "valid") != ("test" if final else "valid")):
                    raise ValueError("Saved execution does not match the active stage")
                result = RunResult(**{name: raw[name] for name in RunResult.__dataclass_fields__})
                if result.metrics is not None:
                    result = replace(result, metrics=MetricResult(**result.metrics))
                return result
        allowance = self.budget.allowance(self.config.candidate_timeout_s, final=final)
        checkpoint = (pending["checkpoint"] if pending is not None else
                      self.state["artifacts"][node_id]["checkpoint"] if final else
                      str((self.directory / "checkpoints" / (uuid.uuid4().hex + ".pkl")).resolve()))
        execution_id = uuid.uuid4().hex
        self.state["execution"] = {"id": execution_id, "checkpoint": checkpoint}
        self._save("execution_scheduled", execution_id=execution_id)
        allowance = self.budget.allowance(self.config.candidate_timeout_s, final=final)
        return self.runner.run(self.git.workspace_dir, data_dir=self.config.data_dir,
                               splits=self.splits, checkpoint_path=checkpoint,
                               timeout_s=allowance, split="test" if final else "valid",
                               train=not final, attempt_id=execution_id)

    def _index(self, node_id, result):
        refs = self.state["artifacts"].setdefault(node_id, {})
        refs.update(checkpoint=result.checkpoint_path, latest_execution=result.artifact_dir)
        refs[f"execution_{self.state['execution']['id']}"] = result.artifact_dir
        if result.status == "success":
            refs["checkpoint_sha256"] = _hash_files([Path(result.checkpoint_path)])[result.checkpoint_path]

    def _check_infrastructure(self, result):
        if result.failure_kind == "infrastructure":
            self.state["execution"] = None
            self._save("execution_retry_prepared")
            raise RuntimeError("Runner infrastructure failure; inspect execution artifacts before resuming")

    def _genesis_prepare(self):
        self.state["genesis_commit"] = self.git.init_workspace(self.config.template_dir)
        self._stage("genesis_execute")

    def _genesis_execute(self):
        self._restore(self.state["genesis_commit"])
        try:
            result = self._execute("genesis")
        except BudgetExhausted:
            self.state["stop_reason"] = "genesis_time_budget"
            self._stage("report")
            return
        self._index("genesis", result)
        self._check_infrastructure(result)
        if result.status != "success":
            self.state["stop_reason"] = "genesis_failed"
            self.state["diagnostic"] = self._diagnostics(result)
            self._stage("report")
            return
        root = SearchNode("genesis", status=NodeStatus.SUCCESS, metrics=result.metrics,
                          git_commit_sha=self.state["genesis_commit"])
        self.tree = SearchTree(root, self.config.search, started_at=self.state["started_at"])
        self.state["execution"] = None
        self._stage("search")

    def _search(self):
        reason = self.tree.stop_reason()
        if self.budget.remaining() <= 0:
            reason = "time_budget"
        elif self.state["llm_calls"] >= self.config.max_llm_calls:
            reason = "model_call_budget"
        parent = None if reason else self.tree.select_parent()
        if reason or parent is None:
            self.state["stop_reason"] = reason or "exhausted"
            self._stage("final_prepare")
            return
        node_id = f"node_{len(self.tree.nodes):03d}"
        node = SearchNode(node_id, parent_id=parent.node_id, depth=parent.depth + 1,
                          incoming_edge=EdgeAction("unproposed", "Proposal not produced"),
                          git_branch=f"codex/{node_id}")
        self.tree.add_node(node)
        self.state.update(active=node_id, attempts={"proposal": 0, "mutation": 0},
                          diagnostic="", execution=None, files=None, repair_pending=False,
                          candidate_started=time.time(), candidate_elapsed=0.0)
        self._stage("propose")

    def _node(self):
        return self.tree.nodes[self.state["active"]]

    def _restore(self, commit):
        # Refuse to overwrite source while a surviving worker holds its lease.
        with file_lease(self.directory / "checkpoints" / "worker.lock"):
            self.git.restore(commit)

    def _parent(self):
        return self.tree.nodes[self._node().parent_id]

    def _context(self):
        return MemoryContext(self.state["run_id"], self.state["protocol_id"], "unspecified",
                             {"parent_commit": self._parent().git_commit_sha})

    def _fail(self, diagnostic):
        self.state["diagnostic"] = self._redact(diagnostic)
        self.state["outcome"] = None
        self._stage("complete_candidate")

    def _propose(self):
        if self.budget.remaining() <= 0:
            self._fail("Time budget exhausted before proposal")
            return
        if self.state["attempts"]["proposal"] >= self.config.proposal_attempts:
            self._fail("Proposal attempts exhausted")
            return
        self._restore(self._parent().git_commit_sha)
        files = self.git.read_active_files(FILES)
        siblings = [dict(node_id=n.node_id, parent_id=n.parent_id, relationship='same_parent', hypothesis=n.incoming_edge.hypothesis,
                         status=n.status.value, metrics=asdict(n.metrics) if n.metrics else None)
                    for n in (self.tree.nodes[i] for i in self._parent().children_ids)
                    if n.node_id != self.state["active"]]
        context = json.dumps({"selected_parent_id": self._parent().node_id,
                              "siblings": siblings, "remaining_seconds": self.budget.remaining(),
                              "memory": self.memory.prompt_summary(self._context(),
                                  parent_commit_sha=self._parent().git_commit_sha,
                                  nodes=self.tree.nodes, selected_parent_id=self._parent().node_id)})
        self.state["attempts"]["proposal"] += 1
        self._save("attempt_reserved")
        try:
            requirement = self.improvement.propose(files, self.tree.get_lineage_chain(self._parent().node_id),
                objective="Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.",
                constraints=CONSTRAINTS, context=context, max_tokens=self.config.proposal_tokens)
        except ProposalError as exc:
            self._audit("output.rejected", error=exc)
            return
        except BudgetExhausted:
            self._fail("Model or time budget exhausted during proposal")
            return
        except (LLMError, ValueError):
            if self.budget.remaining() <= 0:
                self._fail("Time budget exhausted during proposal")
                return
            self.state["attempts"]["proposal"] -= 1
            self._save("attempt_released", attempt=self.state["attempts"]["proposal"] + 1)
            raise
        self._node().incoming_edge = EdgeAction("change", requirement, tokens_used=self.client.last_usage)
        self.state["files"] = files
        self._stage("mutate")

    def _mutate(self):
        if self.budget.remaining() <= 0:
            self._fail("Time budget exhausted before mutation")
            return
        if self.state["attempts"]["mutation"] >= self.config.mutation_attempts:
            self._fail("Mutation output could not be applied")
            return
        self.state["attempts"]["mutation"] += 1
        self._save("attempt_reserved")
        try:
            files = self.mutation.mutate(self._node().incoming_edge.hypothesis, self.state["files"],
                                          max_tokens=self.config.mutation_tokens,
                                          feedback=self._edit_feedback())
        except EditError as exc:
            self._edit_rejected(exc)
            return
        except BudgetExhausted:
            self._fail("Model or time budget exhausted during mutation")
            return
        except (LLMError, ValueError):
            if self.budget.remaining() <= 0:
                self._fail("Time budget exhausted during mutation")
                return
            self.state["attempts"]["mutation"] -= 1
            self._save("attempt_released", attempt=self.state["attempts"]["mutation"] + 1)
            raise
        if files == self.state["files"]:
            self._fail("Mutation produced no code changes")
            return
        self.state["files"] = files
        self._stage("evaluate")

    def _prepare_code(self):
        with file_lease(self.directory / "checkpoints" / "worker.lock"):
            if self.state["execution"] is not None:
                self.git.restore(self._node().git_commit_sha)
                commit = self._node().git_commit_sha
            else:
                self.git.ensure_branch(self._parent().git_commit_sha, self._node().git_branch)
                self.git.write_files(self.state["files"])
                commit = self.git.commit_if_changed(self._node().node_id, "candidate snapshot")
        self._node().git_commit_sha = commit
        self._node().incoming_edge = replace(self._node().incoming_edge,
            raw_diff=self.git.get_diff(self._parent().git_commit_sha, commit))
        if self._node().status == NodeStatus.PENDING:
            self.tree.mark_running(self._node().node_id)
        self._save("candidate_restored" if self.state["execution"] is not None else "candidate_committed")

    def _evaluate(self):
        self._prepare_code()
        try:
            pinned_requirements(self.state["files"]["requirements.txt"])
        except ValueError:
            self.state["diagnostic"] = "requirements.txt must contain exact package==version pins without options or duplicates"
            self._stage("repair")
            return
        try:
            result = self._execute(self._node().node_id)
        except BudgetExhausted:
            self._fail("Time budget exhausted before evaluation")
            return
        self._index(self._node().node_id, result)
        self._check_infrastructure(result)
        self.state["candidate_elapsed"] += result.elapsed_s
        if self.state["repair_pending"]:
            self._node().recovery_events[-1] = replace(self._node().recovery_events[-1],
                                                       succeeded=result.status == "success")
            self.state["repair_pending"] = False
        if self.git.read_active_files(FILES) != self.state["files"]:
            self._fail("Candidate modified its source during execution")
            return
        if result.status == "success":
            self.state["outcome"] = asdict(replace(result.metrics, wall_clock_s=self.state["candidate_elapsed"]))
            self.state["diagnostic"] = ""
            self._stage("complete_candidate")
        else:
            self.state["diagnostic"] = self._diagnostics(result)
            self.state["execution"] = None
            self._stage("repair")

    def _repair(self):
        if len(self._node().recovery_events) >= self.config.max_repairs or self.budget.remaining() <= 0:
            self._fail(self.state["diagnostic"])
            return
        recovery = RecoveryEngine(self.mutation, max_attempts=self.config.max_repairs,
                                  history=self._node().recovery_events)
        self._node().recovery_events.append(RecoveryEvent(
            len(self._node().recovery_events) + 1, self.state["diagnostic"], False))
        self._save("attempt_reserved")
        try:
            proposal = recovery.propose(self.state["files"], hypothesis=self._node().incoming_edge.hypothesis,
                diagnostics=self.state["diagnostic"], constraints=CONSTRAINTS,
                max_tokens=self.config.mutation_tokens, feedback=self._edit_feedback())
        except EditError as exc:
            self._edit_rejected(exc)
            return
        except BudgetExhausted:
            self._fail(self.state["diagnostic"])
            return
        except (LLMError, ValueError):
            if self.budget.remaining() <= 0:
                self._fail(self.state["diagnostic"])
                return
            self._node().recovery_events.pop()
            self._save("attempt_released", attempt=len(self._node().recovery_events) + 1)
            raise
        self.state.pop("edit_retry", None)
        if proposal is None:
            self._save("repair_no_changes")
            return
        self._node().recovery_events[-1] = replace(self._node().recovery_events[-1],
                                                   raw_diff=proposal.raw_diff, tokens_used=self.client.last_usage)
        self.state["files"] = proposal.files
        self.state["repair_pending"] = True
        self.state["execution"] = None
        self._stage("evaluate")

    def _complete_candidate(self):
        node = self._node()
        if node.status in (NodeStatus.PENDING, NodeStatus.RUNNING):
            metrics = MetricResult(**self.state["outcome"]) if self.state["outcome"] else None
            self.tree.record_result(node.node_id, metrics)
        self.state["reflection_attempted"] = False
        self.state["reflection"] = None
        self._stage("reflect")

    def _reflect(self):
        node = self._node()
        delta = node.metrics.val_primary - self._parent().metrics.val_primary if node.metrics else None
        significant = node.status == NodeStatus.FAILED or (
            delta is not None and (
                (delta > self.config.breakthrough_delta
                 and not math.isclose(delta, self.config.breakthrough_delta, rel_tol=0, abs_tol=1e-12))
                or (delta < self.config.collapse_delta
                    and not math.isclose(delta, self.config.collapse_delta, rel_tol=0, abs_tol=1e-12))))
        if (self.config.reflection_enabled and significant and not self.state["reflection_attempted"]
                and self.budget.remaining() > 0):
            self.state["reflection_attempted"] = True
            self._save("attempt_reserved")
            try:
                self.state["reflection"] = self.reflection.reflect(node, self._parent(), self._context(),
                    stderr=self.state["diagnostic"] if node.status == NodeStatus.FAILED else "")
                self._audit('reflection.completed', accepted=self.state['reflection'] is not None,
                            reflection=self.state['reflection'])
            except (ValueError, LLMError) as exc:
                self._audit("reflection.failed", error=exc)
                self.state["reflection"] = None
        self.memory.record(node, self._parent(), self._context(),
                           stderr=self.state["diagnostic"] if node.status == NodeStatus.FAILED else "",
                           reflection=self.state["reflection"])
        self.state.update(active=None, files=None, execution=None)
        self._stage("search")

    def _final_prepare(self):
        self.state["selected"] = self.tree.best_node().node_id
        self.state["execution"] = None
        self._stage("final_execute")

    def _final_execute(self):
        selected = self.tree.nodes[self.state["selected"]]
        self._restore(selected.git_commit_sha)
        refs = self.state["artifacts"][selected.node_id]
        if _hash_files([Path(refs["checkpoint"])])[refs["checkpoint"]] != refs["checkpoint_sha256"]:
            raise ValueError("Selected checkpoint changed after validation")
        try:
            result = self._execute(selected.node_id, final=True)
        except BudgetExhausted:
            self.state["final_test"] = asdict(FinalTestResult(selected.node_id, "not_run",
                                                             error="Final inference time budget exhausted"))
        else:
            self._check_infrastructure(result)
            self.state["final_test"] = asdict(FinalTestResult(selected.node_id, result.status,
                scores=result.scores if result.status == "success" else None,
                artifact_dir=result.artifact_dir,
                error=self._diagnostics(result) if result.status != "success" else None))
            self.state["artifacts"][selected.node_id]["final_test"] = result.artifact_dir
        self._stage("report")

    def _report(self):
        if self.tree is None:
            report = dict(schema_version=1, stop_reason=self.state["stop_reason"],
                          diagnostic=self.state["diagnostic"], selected_node_id=None,
                          final_test={"status": "not_run"}, artifacts=self.state["artifacts"])
        else:
            report = build_report(self.tree, selected_node_id=self.state["selected"],
                stop_reason=self.state["stop_reason"], artifacts=self.state["artifacts"],
                final_test=FinalTestResult(**self.state["final_test"]) if self.state["final_test"] else None)
        report.update(run_id=self.state["run_id"], protocol_id=self.state["protocol_id"],
                      elapsed_s=time.time() - self.state["started_at"], config=asdict(self.config),
                      llm_calls=self.state["llm_calls"], reported_tokens=self.state["reported_tokens"],
                      responses_without_usage=self.state["responses_without_usage"])
        write_report(report, self.directory / "report.json")
        self._stage("done")
