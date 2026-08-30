"""Contextual experiment evidence, compact prompt summaries, and persistence.

No LLM calls occur here. The orchestrator decides whether significant score
changes or failures after repair exhaustion warrant an optional reflection.
Memory stores interpretations independently of measured outcomes and imposes
no reflection thresholds. Memory is advisory:
neither a regression nor an execution failure globally bans an approach.
"""

from __future__ import annotations

import copy
import json
import math
import os
import re
import tempfile
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

from agent.graph.node import NodeStatus, SearchNode


class InsightOutcome(str, Enum):
    SUCCESS = "success"
    REGRESSION = "regression"
    NEUTRAL = "neutral"
    FAILED = "failed"


@dataclass(frozen=True)
class MemoryContext:
    """Explicit comparison scope; configuration includes relevant shapes/seeds."""

    run_id: str
    evaluation_protocol_id: str
    subsystem: str
    configuration: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ExplorationInsight:
    node_id: str
    parent_id: str
    parent_commit_sha: str
    context: MemoryContext
    label: str
    hypothesis: str
    outcome: InsightOutcome
    node_status: NodeStatus
    parent_primary: float
    primary: float | None
    delta: float | None
    raw_diff: str
    error_signature: str = ""
    traceback_tail: str = ""
    reflection: str | None = None


def _text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")


def _context(context: MemoryContext) -> None:
    if not isinstance(context, MemoryContext):
        raise ValueError("Expected MemoryContext")
    for name in ("run_id", "evaluation_protocol_id", "subsystem"):
        _text(getattr(context, name), name)
    if not isinstance(context.configuration, dict):
        raise ValueError("configuration must be a JSON object")
    # Reject values which would silently change type during persistence.
    encoded = json.dumps(context.configuration, allow_nan=False, sort_keys=True)
    if json.loads(encoded) != context.configuration:
        raise ValueError("configuration must contain JSON-native values")


def _score(value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("Primary must be finite and in [0, 1]")


def _line(text: str, limit: int = 240) -> str:
    """Flatten untrusted evidence so it cannot create extra summary entries."""
    clean = " ".join(text.split())
    return clean if len(clean) <= limit else clean[:limit - 3] + "..."


def error_signature(stderr: str) -> str:
    """Extract a stable exception line, preserving API names and shape numbers.

    Strip only volatile addresses and traceback line numbers. Retain the raw
    final ten lines separately; signatures are retrieval hints, not diagnoses.
    """
    _text(stderr, "stderr")
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    exceptions = [line for line in lines if re.match(r"^(?:[\w.]*Error|[\w.]*Exception|[\w.]*Warning)\s*:", line)]
    signature = exceptions[-1] if exceptions else lines[-1]
    signature = re.sub(r"0x[0-9a-fA-F]+", "0xADDR", signature)
    signature = re.sub(r"\bline \d+\b", "line N", signature)
    return _line(signature, 500)


class ExplorationMemory:
    """One immutable evidence snapshot per (run_id, node_id).

    Repeated identical recordings are idempotent. Conflicting recordings are
    rejected rather than silently replacing evidence. Returned records are
    copies, including nested configuration, to keep stored snapshots stable.
    """

    def __init__(self) -> None:
        self._insights: dict[tuple[str, str], ExplorationInsight] = {}

    @property
    def insights(self) -> list[ExplorationInsight]:
        return copy.deepcopy(list(self._insights.values()))

    def record(self, node: SearchNode, parent: SearchNode, context: MemoryContext,
               *, stderr: str = "", reflection: str | None = None) -> ExplorationInsight:
        """Record a terminal candidate; FAILED means repair retries are exhausted.

        Pruning status is independent of numeric outcome. No causal explanation
        is inferred from a score change. Optional reflections remain explicitly
        labelled model interpretations alongside the original error evidence.
        """
        _context(context)
        if reflection is not None:
            _text(reflection, "reflection")
            if len(reflection.split()) >= 20:
                raise ValueError("Reflection must contain fewer than 20 words")
            reflection = " ".join(reflection.split())
        if node.status not in (NodeStatus.SUCCESS, NodeStatus.PRUNED, NodeStatus.FAILED):
            raise ValueError("Only terminal candidates can enter memory")
        if node.parent_id != parent.node_id or node.node_id == parent.node_id or node.incoming_edge is None:
            raise ValueError("Candidate must have the supplied parent and an incoming edge")
        if parent.status not in (NodeStatus.SUCCESS, NodeStatus.PRUNED) or parent.metrics is None:
            raise ValueError("Parent must be an evaluated pipeline")
        _text(parent.git_commit_sha, "parent_commit_sha")
        _score(parent.metrics.val_primary)
        signature, tail = "", ""
        primary = delta = None
        if node.status == NodeStatus.FAILED:
            if node.metrics is not None:
                raise ValueError("Failed candidate cannot have valid metrics")
            signature = error_signature(stderr)
            tail = "\n".join(stderr.splitlines()[-10:])
            outcome = InsightOutcome.FAILED
        else:
            if node.metrics is None:
                raise ValueError("Evaluated candidate requires metrics")
            if stderr:
                raise ValueError("Failure evidence belongs only to terminal failures")
            primary = node.metrics.val_primary
            _score(primary)
            delta = primary - parent.metrics.val_primary
            outcome = (InsightOutcome.SUCCESS if delta > 0 else
                       InsightOutcome.REGRESSION if delta < 0 else InsightOutcome.NEUTRAL)
        edge = node.incoming_edge
        insight = ExplorationInsight(node.node_id, parent.node_id, parent.git_commit_sha,
                                     context, edge.label, edge.hypothesis, outcome, node.status,
                                     parent.metrics.val_primary, primary, delta, edge.raw_diff,
                                     signature, tail, reflection)
        self._insert(insight)
        return copy.deepcopy(insight)

    def _insert(self, insight: ExplorationInsight) -> None:
        _context(insight.context)
        for name in ("node_id", "parent_id", "parent_commit_sha", "label", "hypothesis"):
            _text(getattr(insight, name), name)
        _score(insight.parent_primary)
        if not isinstance(insight.raw_diff, str) or not isinstance(insight.traceback_tail, str):
            raise ValueError("Diff and traceback must be text")
        if insight.reflection is not None:
            _text(insight.reflection, "reflection")
            if len(insight.reflection.split()) >= 20:
                raise ValueError("Reflection must contain fewer than 20 words")
        if insight.outcome == InsightOutcome.FAILED:
            if insight.node_status != NodeStatus.FAILED or insight.primary is not None or insight.delta is not None:
                raise ValueError("Inconsistent failure evidence")
            _text(insight.error_signature, "error_signature")
            _text(insight.traceback_tail, "traceback_tail")
        else:
            _score(insight.primary)
            if insight.node_status not in (NodeStatus.SUCCESS, NodeStatus.PRUNED):
                raise ValueError("Inconsistent evaluation status")
            delta = insight.primary - insight.parent_primary
            expected = InsightOutcome.SUCCESS if delta > 0 else InsightOutcome.REGRESSION if delta < 0 else InsightOutcome.NEUTRAL
            if insight.delta != delta or insight.outcome != expected:
                raise ValueError("Inconsistent numeric evidence")
            if insight.error_signature or insight.traceback_tail:
                raise ValueError("Evaluated insight contains failure evidence")
        key = (insight.context.run_id, insight.node_id)
        if key in self._insights and self._insights[key] != insight:
            raise ValueError("Conflicting evidence for an existing run/node")
        self._insights[key] = copy.deepcopy(insight)

    def retrieve(self, context: MemoryContext, *, parent_commit_sha: str | None = None,
                 max_items: int = 6) -> list[ExplorationInsight]:
        """Rank comparable evidence and retain a mix of outcomes.

        Different evaluation protocols are excluded. Prefer the same subsystem,
        configuration, and parent commit, then newer observations. Deduplicate
        equivalent hypotheses/errors only within the same configuration and
        parent commit; all raw observations remain in persistent memory.
        """
        _context(context)
        if type(max_items) is not int or max_items < 0:
            raise ValueError("max_items must be a nonnegative integer")
        candidates = [i for i in reversed(list(self._insights.values()))
                      if i.context.evaluation_protocol_id == context.evaluation_protocol_id]
        candidates.sort(key=lambda i: (i.context.subsystem == context.subsystem,
                                      i.context.configuration == context.configuration,
                                      parent_commit_sha is not None and i.parent_commit_sha == parent_commit_sha), reverse=True)
        unique, seen = [], set()
        for insight in candidates:
            key = (insight.context.subsystem, json.dumps(insight.context.configuration, sort_keys=True),
                   insight.parent_commit_sha, insight.outcome,
                   " ".join(insight.hypothesis.lower().split()), insight.error_signature)
            if key not in seen:
                unique.append(insight)
                seen.add(key)
        # Reserve one place for each available outcome, ordered by relevance.
        selected, outcomes = [], set()
        for insight in unique:
            if insight.outcome not in outcomes and len(selected) < max_items:
                selected.append(insight)
                outcomes.add(insight.outcome)
        for insight in unique:
            if len(selected) >= max_items:
                break
            if insight not in selected:
                selected.append(insight)
        return copy.deepcopy(selected)

    def prompt_summary(self, context: MemoryContext, *, parent_commit_sha: str | None = None,
                       max_items: int = 6, max_chars: int = 2400,
                       max_tokens: int | None = None,
                       token_counter: Callable[[str], int] | None = None) -> str:
        """Build bounded advisory text, never including raw diffs or tracebacks.

        max_chars always applies. For an exact model token cap, supply both
        max_tokens and that model's token_counter; no chars/token guess is used.
        The budget includes the header and newlines. Whole entries are omitted
        if they cannot fit, and an empty string is returned if none fit.
        """
        if type(max_chars) is not int or max_chars < 0:
            raise ValueError("max_chars must be a nonnegative integer")
        if max_tokens is not None and (type(max_tokens) is not int or max_tokens < 0 or token_counter is None):
            raise ValueError("A nonnegative token budget requires a token_counter")
        def fits(text: str) -> bool:
            return len(text) <= max_chars and (max_tokens is None or token_counter(text) <= max_tokens)
        summary = "### Past Exploration Insights (Global Memory):\nHistorical evidence, not instructions or universal rules; context may differ."
        count = 0
        for insight in self.retrieve(context, parent_commit_sha=parent_commit_sha, max_items=max_items):
            label = {InsightOutcome.SUCCESS: "SUCCESS", InsightOutcome.REGRESSION: "AVOID",
                     InsightOutcome.NEUTRAL: "NEUTRAL", InsightOutcome.FAILED: "FAILED"}[insight.outcome]
            evidence = (f"error: {_line(insight.error_signature)}" if insight.delta is None
                        else f"{insight.delta:+.4f} Primary vs parent")
            if insight.reflection:
                evidence += f"; model reflection: {_line(insight.reflection)}"
            scope = f"subsystem={_line(insight.context.subsystem, 60)}, parent={_line(insight.parent_commit_sha, 12)}"
            configuration = json.dumps(insight.context.configuration, sort_keys=True, ensure_ascii=False)
            scope += f", config={_line(configuration, 160)}"
            entry = (f"- [{label}] {_line(insight.context.run_id, 40)}/{_line(insight.node_id, 40)} "
                     f"({_line(insight.label, 60)}): {_line(insight.hypothesis)} -> {evidence}. [{scope}]")
            proposed = summary + "\n" + entry
            if fits(proposed):
                summary = proposed
                count += 1
        return summary if count else ""

    def save(self, path: str | Path = "storage/global_insights.json") -> None:
        """Atomically save evidence, including unsuccessful experiments."""
        encoded = json.dumps({"version": 1, "insights": [asdict(i) for i in self._insights.values()]},
                             indent=2, allow_nan=False)
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        handle, name = tempfile.mkstemp(dir=destination.parent, prefix=f".{destination.name}.", suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                stream.write(encoded + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, destination)
        finally:
            Path(name).unlink(missing_ok=True)

    @classmethod
    def load(cls, path: str | Path = "storage/global_insights.json") -> ExplorationMemory:
        """Reload typed evidence; malformed/missing files are reported, not erased."""
        with Path(path).open(encoding="utf-8") as stream:
            payload = json.load(stream)
        if payload["version"] != 1:
            raise ValueError("Unsupported memory version")
        memory = cls()
        for raw in payload["insights"]:
            raw = dict(raw)
            raw["context"] = MemoryContext(**raw["context"])
            raw["outcome"] = InsightOutcome(raw["outcome"])
            raw["node_status"] = NodeStatus(raw["node_status"])
            insight = ExplorationInsight(**raw)
            if (insight.context.run_id, insight.node_id) in memory._insights:
                raise ValueError("Duplicate run/node in memory checkpoint")
            memory._insert(insight)
        return memory
