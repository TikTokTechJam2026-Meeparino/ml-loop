"""Offline reflection-to-memory checks: python -B scripts/test_reflection.py."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.memory import ExplorationMemory, InsightOutcome, MemoryContext
from agent.graph.node import EdgeAction, MetricResult, NodeStatus, RecoveryEvent, SearchNode
from agent.graph.reflection import ReflectionEngine
from agent.llm.client import LLMError, LLMResponse
from agent.llm.mock_client import MockLLMClient


class ReflectionTests(unittest.TestCase):
    def setUp(self):
        self.parent = SearchNode("root", status=NodeStatus.SUCCESS, git_commit_sha="a" * 40,
                                 metrics=MetricResult(.5, .5, .5, 1))
        self.node = SearchNode("child", parent_id="root", depth=1, status=NodeStatus.SUCCESS,
                               incoming_edge=EdgeAction("change", "Increase capacity", "actual diff"),
                               metrics=MetricResult(.6, .6, .6, 2))
        self.context = MemoryContext("run", "protocol", "unspecified", {"k": 32})

    def reflect(self, client, **kwargs):
        return ReflectionEngine(client).reflect(self.node, self.parent, self.context, **kwargs)

    def test_evidence_and_memory_handoff_without_mutating_inputs(self):
        self.node.recovery_events.append(RecoveryEvent(1, "Shape mismatch", True, "repair diff"))
        client = MockLLMClient(["Greater capacity may help, although the repair complicates attribution."])
        reflection = self.reflect(client, model="mock/reflector", max_tokens=96)
        memory = ExplorationMemory()
        insight = memory.record(self.node, self.parent, self.context, reflection=reflection)
        self.assertEqual(insight.reflection, reflection)
        self.assertAlmostEqual(insight.delta, .1)
        self.assertEqual(insight.outcome, InsightOutcome.SUCCESS)
        self.assertEqual(self.node.metrics.val_primary, .6)
        sent = client.requests[0]
        payload = json.loads(sent.messages[1]["content"])
        self.assertEqual(payload["evidence"]["hypothesis"], "Increase capacity")
        self.assertEqual(payload["evidence"]["raw_diff"], "actual diff")
        self.assertEqual(payload["parent_metrics"]["val_primary"], .5)
        self.assertEqual(payload["candidate_metrics"]["val_primary"], .6)
        self.assertEqual(payload["repairs"][0]["raw_diff"], "repair diff")
        self.assertEqual(sent.model, "mock/reflector")
        self.assertEqual(sent.max_tokens, 96)

    def test_terminal_failure_preserves_diagnostics_without_inventing_score(self):
        self.node.status = NodeStatus.FAILED
        self.node.metrics = None
        stderr = "Traceback\nValueError: incompatible shapes"
        client = MockLLMClient(["Shape incompatibility prevented evaluation; capacity effects remain unknown."])
        reflection = self.reflect(client, stderr=stderr)
        insight = ExplorationMemory().record(self.node, self.parent, self.context,
                                              stderr=stderr, reflection=reflection)
        self.assertEqual(insight.outcome, InsightOutcome.FAILED)
        self.assertIsNone(insight.delta)
        self.assertEqual(insight.traceback_tail, stderr)

    def test_unavailable_reflection_does_not_prevent_recording(self):
        outputs = [LLMError("provider failure"), "", "NO_REFLECTION", "word " * 20,
                   "```invalid```", LLMResponse("Plausible short text", "mock", None, "length", 1)]
        for output in outputs:
            with self.subTest(output=output):
                reflection = self.reflect(MockLLMClient([output]))
                self.assertIsNone(reflection)
                result = ExplorationMemory().record(self.node, self.parent, self.context,
                                                     reflection=reflection)
                self.assertEqual(result.primary, .6)

    def test_invalid_evidence_fails_before_initialization(self):
        with patch("agent.graph.reflection.LLMClient.from_env") as factory:
            self.node.status = NodeStatus.RUNNING
            with self.assertRaises(ValueError):
                ReflectionEngine().reflect(self.node, self.parent, self.context)
            factory.assert_not_called()

    def test_pruning_is_not_a_trigger_or_a_numeric_failure(self):
        self.node.status = NodeStatus.PRUNED
        client = MockLLMClient(["Capacity may help."])
        self.reflect(client)
        payload = json.loads(client.requests[0].messages[1]["content"])
        self.assertEqual(payload["evidence"]["outcome"], "success")

    def test_client_reuse_and_unavailable_configuration(self):
        client = MockLLMClient(["Capacity may help."] * 2)
        with patch("agent.graph.reflection.LLMClient.from_env", return_value=client) as factory:
            engine = ReflectionEngine()
            for _ in range(2):
                engine.reflect(self.node, self.parent, self.context)
            factory.assert_called_once_with(profile="low")
        with patch("agent.graph.reflection.LLMClient.from_env", side_effect=LLMError("unavailable")):
            self.assertIsNone(ReflectionEngine().reflect(self.node, self.parent, self.context))
        with patch("agent.graph.reflection.LLMClient.from_env", side_effect=ValueError("invalid config")):
            self.assertIsNone(ReflectionEngine().reflect(self.node, self.parent, self.context))


if __name__ == "__main__":
    unittest.main(verbosity=2)
