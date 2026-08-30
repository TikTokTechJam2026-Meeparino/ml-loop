"""Offline proposal-to-mutation checks: python -B scripts/test_improvement.py."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.node import EdgeAction, MetricResult, NodeStatus, SearchNode
from agent.improvement import ImprovementEngine, ProposalError
from agent.llm.client import LLMError, LLMResponse
from agent.llm.mock_client import MockLLMClient
from agent.mutation.mutation import CodeMutationEngine


class ImprovementTests(unittest.TestCase):
    def setUp(self):
        self.files = {"model.py": "dim=16\n"}
        self.root = SearchNode("root", status=NodeStatus.SUCCESS,
                               metrics=MetricResult(.5, .5, .5, 1))
        self.child = SearchNode("child", parent_id="root", depth=1,
                                status=NodeStatus.SUCCESS,
                                incoming_edge=EdgeAction("previous", "Use embeddings", "old diff"),
                                metrics=MetricResult(.6, .6, .6, 2))
        self.options = dict(objective="Improve validation Primary",
                            constraints="Keep evaluation and test isolation unchanged.")

    def test_proposal_feeds_mutation_and_preserves_history(self):
        requirement = "Increase dim from 16 to 32 in model.py to test capacity."
        client = MockLLMClient([
            json.dumps({"requirement": requirement}),
            "FILE: model.py\n```python\n<<<<<<< SEARCH\ndim=16\n=======\ndim=32\n>>>>>>> REPLACE\n```",
        ])
        selected = ImprovementEngine(client).propose(
            self.files, [self.root, self.child], context="Sibling attempt failed: OOM",
            model="mock/proposer", max_tokens=400, **self.options)
        updated = CodeMutationEngine(client).mutate(selected, self.files)
        self.assertEqual(updated["model.py"], "dim=32\n")
        self.assertEqual(self.files["model.py"], "dim=16\n")
        prompt = client.requests[0].messages[1]["content"]
        for text in ("Use embeddings", "old diff", '"val_primary": 0.5',
                     '"val_primary": 0.6', "Sibling attempt failed", "dim=16"):
            self.assertIn(text, prompt)
        self.assertIn(self.options["constraints"], selected)
        self.assertEqual(client.requests[0].model, "mock/proposer")
        self.assertEqual(client.requests[0].max_tokens, 400)

    def test_bad_lineage_and_files_fail_before_client_initialization(self):
        with patch("agent.improvement.improvement.LLMClient.from_env") as factory:
            engine = ImprovementEngine()
            for chain in ([], [self.child], [self.child, self.root], [self.root, self.root]):
                with self.assertRaises(ValueError):
                    engine.propose(self.files, chain, **self.options)
            with self.assertRaises(ValueError):
                engine.propose({"../secret.py": "x"}, [self.root], **self.options)
            factory.assert_not_called()

    def test_invalid_or_truncated_output_never_becomes_requirement(self):
        for output in ("not json", "{}", '[]', '{"requirement": " "}',
                       '{"requirement": 1}', '{"requirement": "x", "category": "x"}',
                       LLMResponse('{"requirement": "x"}', "mock", None, "length", 1)):
            with self.subTest(output=output), self.assertRaises(ProposalError):
                ImprovementEngine(MockLLMClient([output])).propose(
                    self.files, [self.root], **self.options)

    def test_provider_errors_propagate(self):
        with self.assertRaises(LLMError):
            ImprovementEngine(MockLLMClient([LLMError("failed")])).propose(
                self.files, [self.root], **self.options)

    def test_complete_json_fence_is_accepted_but_partial_output_is_not(self):
        complete = '```json\n{"requirement": "Increase capacity"}\n```'
        result = ImprovementEngine(MockLLMClient([complete])).propose(
            self.files, [self.root], **self.options)
        self.assertIn("Increase capacity", result)
        for output in (complete[:-3], "Explanation\n" + complete,
                       complete + "\nExtra commentary", complete + "\n" + complete,
                       LLMResponse(complete, "mock", None, "length", 1)):
            with self.subTest(output=output), self.assertRaises(ProposalError):
                ImprovementEngine(MockLLMClient([output])).propose(
                    self.files, [self.root], **self.options)

    def test_default_client_reused(self):
        client = MockLLMClient(['{"requirement": "Try capacity"}'] * 2)
        with patch("agent.improvement.improvement.LLMClient.from_env", return_value=client) as factory:
            engine = ImprovementEngine()
            for _ in range(2):
                engine.propose(self.files, [self.root], **self.options)
            factory.assert_called_once_with(profile="high")


if __name__ == "__main__":
    unittest.main(verbosity=2)
