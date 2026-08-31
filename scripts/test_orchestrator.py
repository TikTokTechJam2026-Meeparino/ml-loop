"""Offline lifecycle tests using real Git and deterministic LLM/runner doubles."""

from dataclasses import asdict, replace
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.node import MetricResult
from agent.graph.tree import SearchConfig
from agent.llm.client import LLMError, LLMResponse, TokenUsage
from agent.llm.mock_client import MockLLMClient
from agent.orchestrator import Orchestrator, RunConfig
from agent.run_state import RunStore
from agent.sandbox.runner import RunResult

REAL_RUNNER = "--real-runner" in sys.argv
if REAL_RUNNER:
    sys.argv.remove("--real-runner")


SPLITS = {"train": [[1, 1, 1, 1, 1, 1, 0]], "valid": [[2, 1, 1, 1, 1, 1, 1]],
          "test": [[3, 1, 1, 1, 1, 1, 0]]}
PROPOSAL = '{"requirement": "Increase capacity in model.py"}'


def rejected_fixture(attempt):
    return (Path(__file__).parent / "fixtures" / "edit_rejections" /
            f"attempt_{attempt}.txt").read_text(encoding="utf-8")


def edit(old, new):
    return f"FILE: model.py\n```python\n<<<<<<< SEARCH\n{old}\n=======\n{new}\n>>>>>>> REPLACE\n```"


class FakeRunner:
    def __init__(self, directory, outcomes):
        self.storage_dir = Path(directory) / "executions"
        self.outcomes = list(outcomes)
        self.calls = []
        self.interrupt_after = None

    def run(self, workspace, **kwargs):
        self.calls.append(kwargs)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        folder = self.storage_dir / kwargs["attempt_id"]
        folder.mkdir(parents=True)
        checkpoint = Path(kwargs["checkpoint_path"])
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        checkpoint.write_text("checkpoint")
        final = kwargs["split"] == "test"
        result = RunResult("success" if outcome is not None else "failed", str(checkpoint), str(folder),
            MetricResult(outcome, outcome, outcome, 1) if outcome is not None and not final else None,
            {"GAUC": outcome, "nDCG@5": outcome, "primary": outcome} if outcome is not None else None,
            1, "ValueError: shape mismatch" if outcome is None else None)
        (folder / "result.json").write_text(json.dumps({**asdict(result), "split": kwargs["split"]}))
        if self.interrupt_after == len(self.calls):
            raise KeyboardInterrupt()
        return result


class OrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.run_dir = root / "run"
        template = root / "template"
        template.mkdir()
        for name in ("config.py", "features.py", "train.py"):
            (template / name).write_text("# placeholder\n")
        (template / "model.py").write_text("dim=16\n")
        (template / "requirements.txt").write_text("")
        self.config = RunConfig(str(self.run_dir), template_dir=str(template),
            search=SearchConfig(max_iterations=1), reflection_enabled=False,
            mutation_attempts=2)  # Keep historical two-attempt scenarios explicit.

    def run_with(self, responses, outcomes):
        client = MockLLMClient(responses)
        runner = FakeRunner(self.run_dir, outcomes)
        obj = Orchestrator(self.config, client=client, runner=runner, splits=SPLITS)
        return obj, client, runner

    def test_success_and_completed_resume_does_not_call_components(self):
        obj, client, runner = self.run_with([PROPOSAL, edit("dim=16", "dim=32")], [.5, .6, .55])
        report = obj.run()
        self.assertEqual(report["selected_node_id"], "node_001")
        self.assertAlmostEqual(report["validation_comparison"]["primary_gain"], .1)
        self.assertEqual(report["final_test"]["scores"]["primary"], .55)
        self.assertEqual([c["split"] for c in runner.calls], ["valid", "valid", "test"])
        self.assertFalse(runner.calls[-1]["train"])
        self.assertEqual(runner.calls[-1]["checkpoint_path"], runner.calls[1]["checkpoint_path"])
        resumed = Orchestrator.resume(self.run_dir, client=client, runner=runner, splits=SPLITS)
        self.assertEqual(resumed, report)
        self.assertEqual(len(runner.calls), 3)
        state, tree, memory = RunStore(self.run_dir).load()
        self.assertEqual(state["stage"], "done")
        self.assertEqual(tree.iteration_count, 1)
        self.assertEqual(len(memory.insights), 1)

    def test_improvement_receives_sibling_and_memory_provenance(self):
        from dataclasses import replace
        self.config = replace(self.config, search=SearchConfig(max_iterations=2))
        obj, client, _ = self.run_with(
            [PROPOSAL, edit("dim=16", "dim=32"), PROPOSAL, edit("dim=16", "dim=24")],
            [.5, .49, .55, .6])
        obj.run()
        prompt = client.requests[2].messages[1]['content']
        payload = json.loads(prompt.split('EXPERIMENT EVIDENCE (JSON)\n', 1)[1].split('\n\n', 1)[0])
        context = json.loads(payload['additional_context'])
        self.assertEqual(context['selected_parent_id'], 'genesis')
        self.assertEqual(context['siblings'][0]['parent_id'], 'genesis')
        self.assertEqual(context['siblings'][0]['relationship'], 'same_parent')
        self.assertIn('genesis -> node_001', context['memory'])
        self.assertIn('relationship=same_parent', context['memory'])

    def test_best_first_detour_resume_and_stagnation_finalize_once(self):
        self.config = replace(self.config, search=SearchConfig(max_iterations=20, stagnation_patience=1))
        obj, client, runner = self.run_with(
            [PROPOSAL, edit('dim=16', 'dim=32'),
             PROPOSAL, edit('dim=32', 'dim=48'),
             PROPOSAL, edit('dim=48', 'dim=64'),
             PROPOSAL, edit('dim=64', 'dim=80')], [.5, .6, .55, .4, .45, .58])
        runner.interrupt_after = 4
        with self.assertRaises(KeyboardInterrupt):
            obj.run()
        state, tree, _ = RunStore(self.run_dir).load()
        self.assertEqual(state['active'], 'node_003')
        self.assertEqual(tree.selection.detour_remaining, 2)
        runner.interrupt_after = None
        report = Orchestrator.resume(self.run_dir, client=client, runner=runner, splits=SPLITS)
        self.assertEqual(report['stop_reason'], 'stagnation')
        self.assertEqual(report['completed_iterations'], 4)
        self.assertEqual(report['selected_node_id'], 'node_001')
        self.assertEqual([n['parent_id'] for n in report['nodes'][1:]],
                         ['genesis', 'node_001', 'node_002', 'node_003'])
        self.assertEqual(report['selection_decisions']['node_003']['reason'], 'detour_start')
        self.assertEqual(report['selection_decisions']['node_004']['reason'], 'detour_continue')
        self.assertTrue(report['search_selection']['review_required'])
        self.assertEqual(len(runner.calls), 6)  # Completed result recovered, not retrained.
        self.assertEqual(len(client.requests), 8)

    def test_legacy_run_config_resumes_as_uct(self):
        self.config = replace(self.config, search=SearchConfig(strategy='uct', max_iterations=2))
        obj, client, runner = self.run_with(
            [PROPOSAL, edit('dim=16', 'dim=32'), PROPOSAL, edit('dim=16', 'dim=24')],
            [.5, .6, .55, .58])
        runner.interrupt_after = 2
        with self.assertRaises(KeyboardInterrupt):
            obj.run()
        pointer = json.loads((self.run_dir / 'current.json').read_text())
        folder = self.run_dir / 'snapshots' / pointer['generation']
        for filename in ('state.json', 'tree.json'):
            path = folder / filename
            payload = json.loads(path.read_text())
            config = payload['config']['search'] if filename == 'state.json' else payload['config']
            for key in ('strategy', 'stagnation_patience', 'detour_attempts', 'max_detours',
                        'promotion_threshold'):
                config.pop(key)
            if filename == 'tree.json':
                payload['version'] = 1
                payload.pop('selection')
            path.write_text(json.dumps(payload))
        runner.interrupt_after = None
        report = Orchestrator.resume(self.run_dir, client=client, runner=runner, splits=SPLITS)
        self.assertEqual(report['config']['search']['strategy'], 'uct')
        self.assertEqual(report['nodes'][2]['parent_id'], 'genesis')
        self.assertEqual(report['selected_node_id'], 'node_001')

    def test_repair_and_reflection_handoff(self):
        from dataclasses import replace
        self.config = replace(self.config, reflection_enabled=True)
        obj, client, runner = self.run_with(
            [PROPOSAL, edit("dim=16", "dim=32"), edit("dim=32", "dim=24"), "Capacity may help."],
            [.5, None, .6, .57])
        obj.run()
        _, tree, memory = RunStore(self.run_dir).load()
        event = tree.nodes["node_001"].recovery_events[0]
        self.assertTrue(event.succeeded)
        self.assertIn("+dim=24", event.raw_diff)
        self.assertEqual(memory.insights[0].reflection, "Capacity may help.")
        self.assertNotEqual(runner.calls[1]["checkpoint_path"], runner.calls[2]["checkpoint_path"])

    def test_checkpoint_reasons_and_response_metadata_without_content(self):
        obj, client, runner = self.run_with(
            [LLMResponse(PROPOSAL, "mock", TokenUsage(20, 5, 25), "stop", 1),
             edit("dim=16", "dim=32")], [.5, .6, .55])
        obj.run()
        log = (self.run_dir / "events.jsonl").read_text()
        saved = [json.loads(line)["data"] for line in log.splitlines()
                 if json.loads(line)["event"] == "stage.saved"]
        self.assertTrue(all(event["reason"] for event in saved))
        self.assertTrue({"stage_entered", "attempt_reserved", "model_request_started",
                         "model_response_received", "candidate_committed", "execution_scheduled"}
                        <= {event["reason"] for event in saved})
        requests = [event for event in saved if event["reason"] == "model_request_started"]
        responses = [event for event in saved if event["reason"] == "model_response_received"]
        self.assertEqual([event["call_id"] for event in requests], [1, 2])
        self.assertEqual([event["call_id"] for event in responses], [1, 2])
        self.assertEqual([event["attempt"] for event in requests], [1, 1])
        self.assertEqual(responses[0]["token_usage"], {"prompt_tokens": 20, "completion_tokens": 5, "total_tokens": 25})
        self.assertIsNone(responses[1]["token_usage"])
        self.assertEqual(responses[0]["finish_reason"], "stop")
        self.assertTrue(all(event["elapsed_s"] >= 0 for event in responses))
        self.assertNotIn("Increase capacity", log)
        self.assertNotIn("dim=32", log)

    def test_rejected_output_logs_response_and_retry_attempts(self):
        obj, _, _ = self.run_with([
            LLMResponse("private-response", "mock", None, "length", 1), PROPOSAL, "NO_CHANGES"], [.5, .4])
        obj.run()
        log = (self.run_dir / "events.jsonl").read_text()
        saved = [json.loads(line)["data"] for line in log.splitlines()
                 if json.loads(line)["event"] == "stage.saved"]
        responses = [event for event in saved if event["reason"] == "model_response_received"]
        self.assertEqual(responses[0]["finish_reason"], "length")
        self.assertEqual([event["attempt"] for event in responses], [1, 2, 1])
        self.assertNotIn("private-response", log)

    def test_no_change_and_invalid_proposals_count_without_training(self):
        for responses in ([PROPOSAL, "NO_CHANGES"], ["invalid", "invalid"]):
            with self.subTest(responses=responses):
                from dataclasses import replace
                self.config = replace(self.config, run_dir=str(self.run_dir / str(len(responses[0]))))
                obj, _, runner = self.run_with(responses, [.5, .4])
                report = obj.run()
                self.assertEqual(report["candidate_status_counts"], {"failed": 1})
                self.assertEqual(report["selected_node_id"], "genesis")
                self.assertEqual(len(runner.calls), 2)

    def test_logged_rejections_get_corrective_retry_and_apply_only_correction(self):
        for attempt in (1, 2):
            with self.subTest(attempt=attempt):
                self.config = replace(self.config, run_dir=str(self.run_dir / str(attempt)))
                rejected = rejected_fixture(attempt)
                obj, client, runner = self.run_with(
                    [PROPOSAL, rejected, edit("dim=16", "dim=32")], [.5, .6, .55])
                source = (Path(self.config.template_dir) / "model.py").read_bytes().decode("utf-8")
                original = obj._edit_rejected
                def inspect_rejection(exc):
                    original(exc)
                    state, _, _ = obj.store.load()
                    self.assertEqual(state["files"]["model.py"], source)
                    self.assertEqual(obj.git.read_active_files(["model.py"])["model.py"], source)
                    self.assertEqual(state["edit_retry"]["rejected_output"], rejected)
                    self.assertEqual(len(runner.calls), 1)
                obj._edit_rejected = inspect_rejection
                report = obj.run()
                self.assertEqual(report["selected_node_id"], "node_001")
                self.assertEqual(report["llm_calls"], 3)
                first, retry = client.requests[1:]
                self.assertEqual(retry.messages[:2], first.messages)
                self.assertEqual(retry.messages[2], {"role": "assistant", "content": rejected})
                self.assertIn("Missing marker lines", retry.messages[3]["content"])
                self.assertEqual(obj.git.read_active_files(["model.py"])["model.py"], source.replace("16", "32"))
                state, _, _ = obj.store.load()
                self.assertNotIn("edit_retry", state)
                self.assertEqual(len(runner.calls), 3)

    def test_rejection_feedback_survives_restart(self):
        rejected = rejected_fixture(1)
        obj, client, runner = self.run_with([PROPOSAL, rejected], [.5, .6, .55])
        original = obj._edit_rejected
        def interrupt(exc):
            original(exc)
            raise KeyboardInterrupt()
        obj._edit_rejected = interrupt
        with self.assertRaises(KeyboardInterrupt):
            obj.run()
        state, _, _ = obj.store.load()
        self.assertEqual(state["attempts"]["mutation"], 1)
        resumed_client = MockLLMClient([edit("dim=16", "dim=32")])
        report = Orchestrator.resume(self.run_dir, client=resumed_client, runner=runner, splits=SPLITS)
        messages = resumed_client.requests[0].messages
        self.assertEqual(messages[:2], client.requests[1].messages)
        self.assertEqual(messages[2]["content"], rejected)
        self.assertIn(state["edit_retry"]["error"], messages[3]["content"])
        self.assertEqual(report["llm_calls"], 3)

    def test_repeated_rejections_stop_at_limit_and_do_not_leak_to_next_candidate(self):
        self.config = replace(self.config, search=SearchConfig(max_iterations=2))
        obj, client, runner = self.run_with(
            [PROPOSAL, rejected_fixture(1), rejected_fixture(2), PROPOSAL, edit("dim=16", "dim=32")],
            [.5, .6, .55])
        report = obj.run()
        self.assertEqual(report["candidate_status_counts"], {"failed": 1, "success": 1})
        self.assertEqual(len(client.requests), 5)
        self.assertEqual(len(client.requests[2].messages), 4)
        self.assertEqual(len(client.requests[4].messages), 2)
        self.assertEqual(len(runner.calls), 3)

    def test_repair_format_failure_gets_feedback_then_clears_for_new_source(self):
        rejected = edit("dim=32", "dim=24").replace("<<<<<<< SEARCH\n", "")
        obj, client, runner = self.run_with(
            [PROPOSAL, edit("dim=16", "dim=32"), rejected,
             edit("dim=32", "dim=24"), edit("dim=24", "dim=20")],
            [.5, None, None, .6, .55])
        report = obj.run()
        self.assertEqual(report["selected_node_id"], "node_001")
        self.assertEqual(client.requests[3].messages[:2], client.requests[2].messages)
        self.assertEqual(client.requests[3].messages[2]["content"], rejected)
        self.assertEqual(len(client.requests[4].messages), 2)
        self.assertIn("dim=24", client.requests[4].messages[1]["content"])
        self.assertEqual(len(runner.calls), 5)

    def test_retry_context_is_redacted_before_checkpoint_and_replay(self):
        secret = "fixture-sensitive-value-123"
        rejected = "malformed output " + secret
        obj, client, _ = self.run_with([PROPOSAL, rejected, edit("dim=16", "dim=32")], [.5, .6, .55])
        with patch.dict("os.environ", {"TEST_API_KEY": secret}):
            obj.run()
        self.assertEqual(client.requests[2].messages[2]["content"], "malformed output [REDACTED]")
        for path in obj.directory.glob("snapshots/*/state.json"):
            self.assertNotIn(secret, path.read_text(encoding="utf-8"))

    def test_correction_still_obeys_model_call_limit(self):
        self.config = replace(self.config, max_llm_calls=2)
        obj, client, runner = self.run_with([PROPOSAL, rejected_fixture(1)], [.5, .4])
        report = obj.run()
        self.assertEqual(report["llm_calls"], 2)
        self.assertEqual(len(client.requests), 2)
        self.assertEqual(len(runner.calls), 2)

    def test_third_attempt_uses_latest_rejection_without_growing_history(self):
        self.config = replace(self.config, mutation_attempts=3)
        obj, client, _ = self.run_with(
            [PROPOSAL, rejected_fixture(1), rejected_fixture(2), edit("dim=16", "dim=32")],
            [.5, .6, .55])
        obj.run()
        messages = client.requests[3].messages
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[:2], client.requests[1].messages)
        self.assertEqual(messages[2]["content"], rejected_fixture(2))
        self.assertIn("found ['=======']", messages[3]["content"])

    def test_default_four_attempts_allow_third_correction_and_stop_at_limit(self):
        default = RunConfig(str(self.run_dir)).mutation_attempts
        self.assertEqual(default, 4)
        self.config = replace(self.config, mutation_attempts=default, search=SearchConfig(max_iterations=2))
        bad = rejected_fixture(1)
        obj, client, runner = self.run_with(
            [PROPOSAL, bad, bad, bad, edit('dim=16', 'dim=32'),
             PROPOSAL, bad, bad, bad, bad], [.5, .6, .55])
        report = obj.run()
        self.assertEqual(report['completed_iterations'], 2)
        self.assertEqual(report['candidate_status_counts'], {'success': 1, 'failed': 1})
        self.assertEqual(len(client.requests), 10)
        self.assertEqual(len(runner.calls), 3)
        self.assertEqual(len(client.requests[4].messages), 4)

    def test_oversized_correction_does_not_bypass_prompt_budget(self):
        obj, client, runner = self.run_with([PROPOSAL, rejected_fixture(1)], [.5])
        original = obj._edit_rejected
        def limit_retry(exc):
            original(exc)
            obj.client.max_prompt_chars = sum(len(m["content"]) for m in client.requests[-1].messages)
        obj._edit_rejected = limit_retry
        with self.assertRaisesRegex(ValueError, "Prompt exceeds configured character budget"):
            obj.run()
        state, _, _ = obj.store.load()
        self.assertEqual(len(client.requests), 2)
        self.assertEqual(len(runner.calls), 1)
        self.assertEqual(state["attempts"]["mutation"], 1)
        self.assertEqual(state["edit_retry"]["rejected_output"], rejected_fixture(1))

    def test_completed_evaluation_recovered_without_retraining(self):
        obj, client, runner = self.run_with([PROPOSAL, edit("dim=16", "dim=32")], [.5, .6, .55])
        runner.interrupt_after = 2
        with self.assertRaises(KeyboardInterrupt):
            obj.run()
        runner.interrupt_after = None
        report = Orchestrator.resume(self.run_dir, client=client, runner=runner, splits=SPLITS)
        self.assertEqual(report["completed_iterations"], 1)
        self.assertEqual(len(runner.calls), 3)

    def test_interrupted_final_test_is_not_repeated(self):
        obj, client, runner = self.run_with([PROPOSAL, "NO_CHANGES"], [.5, .4])
        runner.interrupt_after = 2
        with self.assertRaises(KeyboardInterrupt):
            obj.run()
        runner.interrupt_after = None
        report = Orchestrator.resume(self.run_dir, client=client, runner=runner, splits=SPLITS)
        self.assertEqual(report["final_test"]["status"], "success")
        self.assertEqual(len(runner.calls), 2)

    def test_provider_failure_pauses_without_failed_experiment(self):
        obj, _, runner = self.run_with([LLMError("secret-provider-error")], [.5, .4])
        with self.assertRaises(LLMError):
            obj.run()
        state, tree, memory = RunStore(self.run_dir).load()
        self.assertEqual(tree.iteration_count, 0)
        self.assertEqual(len(memory.insights), 0)
        self.assertEqual(state["paused_error"], "LLMError")
        Orchestrator.resume(self.run_dir, client=MockLLMClient([PROPOSAL, "NO_CHANGES"]),
                            runner=runner, splits=SPLITS)

    def test_genesis_failure_reports_without_search(self):
        obj, client, runner = self.run_with([], [None])
        report = obj.run()
        self.assertEqual(report["stop_reason"], "genesis_failed")
        self.assertEqual(client.requests, [])

    def test_insufficient_headroom_stops_before_starting_a_candidate(self):
        from dataclasses import replace
        # FakeRunner reports elapsed_s=1, so a x100 headroom needs 100s.
        self.config = replace(self.config, candidate_headroom=100)
        obj, client, runner = self.run_with([], [.5, .4])
        original = obj._search
        def shrink():
            obj.budget.deadline = __import__("time").time() + obj.config.final_reserve_s + 30
            original()
        obj._search = shrink
        report = obj.run()
        self.assertEqual(report["stop_reason"], "candidate_time_budget")
        self.assertEqual(report["completed_iterations"], 0)
        self.assertEqual(report["final_test"]["status"], "success")  # Reserve intact.
        self.assertEqual(client.requests, [])  # No proposal was paid for.

    def test_headroom_uses_the_median_of_evaluated_nodes(self):
        from dataclasses import replace
        obj, _, _ = self.run_with([PROPOSAL, edit("dim=16", "dim=32")], [.5, .6, .55])
        obj.run()
        self.assertEqual(obj._typical_candidate_s(), 1.0)
        self.assertEqual(obj._candidate_headroom_s(), 1.25)
        self.assertEqual(RunConfig(str(self.run_dir)).candidate_headroom, 1.25)
        for value in (-1, float("inf"), float("nan"), True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                replace(self.config, candidate_headroom=value)

    def test_recalibrated_default_reflects_on_a_small_real_gain(self):
        from dataclasses import replace
        self.assertEqual(RunConfig(str(self.run_dir)).breakthrough_delta, .0005)
        self.config = replace(self.config, reflection_enabled=True)
        obj, client, _ = self.run_with(
            [PROPOSAL, edit("dim=16", "dim=32"), "Small capacity gain."], [.5, .501, .5])
        obj.run()
        _, _, memory = RunStore(self.run_dir).load()
        self.assertEqual(len(client.requests), 3)
        self.assertEqual(memory.insights[0].reflection, "Small capacity gain.")

    def test_budget_reserve_skips_search_but_allows_final_test(self):
        obj, client, runner = self.run_with([], [.5, .4])
        original = obj._search
        def stop_search():
            obj.budget.deadline = __import__("time").time() + 60
            original()
        obj._search = stop_search
        report = obj.run()
        self.assertEqual(report["stop_reason"], "time_budget")
        self.assertEqual(report["final_test"]["status"], "success")
        self.assertEqual(client.requests, [])

    def test_resume_rejects_changed_dataset(self):
        obj, _, runner = self.run_with([LLMError("pause")], [.5])
        with self.assertRaises(LLMError):
            obj.run()
        with self.assertRaises(ValueError):
            Orchestrator.resume(self.run_dir, client=MockLLMClient([]), runner=runner,
                                splits={**SPLITS, "test": []})

    def test_model_call_budget_finishes_active_attempt(self):
        from dataclasses import replace
        self.config = replace(self.config, max_llm_calls=1)
        obj, client, runner = self.run_with([PROPOSAL], [.5, .4])
        report = obj.run()
        self.assertEqual(report["stop_reason"], "model_call_budget")
        self.assertEqual(report["completed_iterations"], 1)
        self.assertEqual(len(client.requests), 1)

    def test_repair_exhaustion_and_final_test_failure(self):
        from dataclasses import replace
        self.config = replace(self.config, max_repairs=1)
        obj, _, runner = self.run_with([PROPOSAL, edit("dim=16", "dim=32"), "NO_CHANGES"],
                                       [.5, None, None])
        report = obj.run()
        self.assertEqual(report["selected_node_id"], "genesis")
        self.assertEqual(report["candidate_status_counts"], {"failed": 1})
        self.assertEqual(report["final_test"]["status"], "failed")

    def test_multiple_generations_pass_lineage_and_memory(self):
        from dataclasses import replace
        self.config = replace(self.config, search=SearchConfig(max_iterations=2, max_children=1))
        obj, client, runner = self.run_with(
            [PROPOSAL, edit("dim=16", "dim=32"), PROPOSAL, edit("dim=32", "dim=64")],
            [.5, .6, .65, .61])
        report = obj.run()
        _, tree, memory = RunStore(self.run_dir).load()
        self.assertEqual(tree.nodes["node_002"].parent_id, "node_001")
        self.assertEqual(report["selected_node_id"], "node_002")
        self.assertEqual(len(memory.insights), 2)
        prompt = client.requests[2].messages[1]["content"]
        self.assertIn("dim=32", prompt)
        self.assertIn("0.6", prompt)

    def test_checkpoint_drift_prevents_test_inference(self):
        obj, client, runner = self.run_with([PROPOSAL, "NO_CHANGES"], [.5])
        original = obj._final_execute
        def corrupt_checkpoint():
            Path(obj.state["artifacts"]["genesis"]["checkpoint"]).write_text("corrupted")
            original()
        obj._final_execute = corrupt_checkpoint
        with self.assertRaises(ValueError):
            obj.run()
        self.assertEqual(len(runner.calls), 1)

    def test_exact_reflection_threshold_does_not_trigger(self):
        from dataclasses import replace
        # Pin the threshold so this keeps testing exact-threshold semantics
        # rather than tracking whatever the default happens to be.
        self.config = replace(self.config, reflection_enabled=True, breakthrough_delta=.01)
        obj, client, runner = self.run_with([PROPOSAL, edit("dim=16", "dim=32")], [.5, .51, .5])
        obj.run()
        self.assertEqual(len(client.requests), 2)

    def test_expired_final_budget_is_reported(self):
        obj, client, runner = self.run_with([PROPOSAL, "NO_CHANGES"], [.5])
        original = obj._final_execute
        def expired():
            obj.budget.deadline = 0
            original()
        obj._final_execute = expired
        report = obj.run()
        self.assertEqual(report["final_test"]["status"], "not_run")
        self.assertEqual(len(runner.calls), 1)

    def test_infrastructure_result_pauses_without_tree_penalty(self):
        from dataclasses import replace
        obj, client, runner = self.run_with([PROPOSAL, edit("dim=16", "dim=32")], [.5, None])
        original = runner.run
        def infrastructure(workspace, **kwargs):
            result = original(workspace, **kwargs)
            if len(runner.calls) == 2:
                result = replace(result, failure_kind="infrastructure")
            return result
        runner.run = infrastructure
        with self.assertRaises(RuntimeError):
            obj.run()
        _, tree, memory = RunStore(self.run_dir).load()
        self.assertEqual(tree.iteration_count, 0)
        self.assertEqual(len(memory.insights), 0)

    def test_resume_between_tree_completion_and_memory_records_once(self):
        obj, client, runner = self.run_with([PROPOSAL, "NO_CHANGES"], [.5, .4])
        original = obj._stage
        def interrupt(stage):
            original(stage)
            if stage == "reflect":
                raise KeyboardInterrupt()
        obj._stage = interrupt
        with self.assertRaises(KeyboardInterrupt):
            obj.run()
        report = Orchestrator.resume(self.run_dir, client=client, runner=runner, splits=SPLITS)
        _, tree, memory = RunStore(self.run_dir).load()
        self.assertEqual(report["completed_iterations"], 1)
        self.assertEqual(len(memory.insights), 1)

    @unittest.skipUnless(REAL_RUNNER, "pass --real-runner to execute real training")
    def test_real_runner_with_mocked_model(self):
        from dataclasses import replace
        from test_runner import fixture
        from agent.orchestrator import ROOT
        config = replace(self.config, template_dir=str(ROOT / "workspace_template"))
        edit_config = ('FILE: config.py\n```python\n<<<<<<< SEARCH\n'
                       'DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)\n'
                       '=======\n'
                       'DEFAULTS = dict(k=16, lr=0.002, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)\n'
                       '>>>>>>> REPLACE\n```')
        client = MockLLMClient(['{"requirement":"Increase lr to 0.002 in config.py"}', edit_config])
        report = Orchestrator(config, client=client, splits=fixture()).run()
        self.assertEqual(report["final_test"]["status"], "success")
        self.assertEqual(report["completed_iterations"], 1)
        self.assertEqual(report["candidate_status_counts"].get("failed", 0), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
