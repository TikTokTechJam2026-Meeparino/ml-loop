"""Offline mutation integration tests: python scripts/test_mutation.py."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.mutation.mutation import CodeMutationEngine
from agent.mutation.parser import EditError
from agent.llm.client import LLMResponse, LLMError
from agent.llm.mock_client import MockLLMClient


def edit(filename, search, replacement):
    return (
        f"FILE: {filename}\n```python\n<<<<<<< SEARCH\n{search}\n"
        f"=======\n{replacement}\n>>>>>>> REPLACE\n```\n"
    )


class MutationTests(unittest.TestCase):
    def engine(self, *responses):
        return CodeMutationEngine(MockLLMClient(responses))

    def test_full_pipeline_multiple_files_and_client_reuse(self):
        output = edit("model.py", "dim=64", "dim=128")
        engine = self.engine(output, output)
        files = {"model.py": "dim=64\n", "train.py": "pass\n"}
        result = engine.mutate("Increase dimension to 128", files, model="test/other", max_tokens=500)
        self.assertEqual(result, {"model.py": "dim=128\n", "train.py": "pass\n"})
        self.assertEqual(files["model.py"], "dim=64\n")
        sent = engine.client.requests[0]
        self.assertEqual(sent.model, "test/other")
        self.assertEqual(sent.max_tokens, 500)
        self.assertEqual(sent.messages[0]["role"], "system")
        self.assertIn("Increase dimension to 128", sent.messages[1]["content"])
        self.assertIn("FILE: train.py", sent.messages[1]["content"])
        engine.mutate("Increase dimension", files)
        self.assertEqual(len(engine.client.requests), 2)
        self.assertEqual(engine.client.remaining_responses, 0)

    def test_no_changes(self):
        engine = self.engine("NO_CHANGES")
        files = {"model.py": "pass"}
        result = engine.mutate("Keep existing behavior", files)
        self.assertEqual(result, files)
        self.assertIsNot(result, files)

    def test_invalid_inputs_do_not_initialize_client(self):
        with patch("agent.mutation.mutation.LLMClient.from_env") as factory:
            engine = CodeMutationEngine()
            for requirement, files in [("", {"a.py": "x"}), ("Edit", {}),
                                       ("Edit", {"../a.py": "x"}), ("Edit", {"a.py": 123}),
                                       ("Edit", [{"a.py": "x"}])]:
                with self.subTest(files=files), self.assertRaises((ValueError, TypeError)):
                    engine.mutate(requirement, files)
            factory.assert_not_called()

    def test_parse_and_match_failures_propagate_without_mutation(self):
        files = {"a.py": "one"}
        for output in ["malformed", edit("a.py", "one", "two") + edit("a.py", "missing", "three")]:
            with self.subTest(output=output), self.assertRaises(EditError):
                self.engine(output).mutate("Edit", files)
            self.assertEqual(files, {"a.py": "one"})

    def test_complete_block_with_truncated_finish_is_rejected(self):
        engine = self.engine(LLMResponse(edit("a.py", "one", "two"), "mock/model", None, "length", 1))
        with self.assertRaises(EditError):
            engine.mutate("Edit", {"a.py": "one"})

    def test_provider_errors_propagate(self):
        engine = self.engine(LLMError("Request failed"))
        with self.assertRaises(LLMError):
            engine.mutate("Edit", {"a.py": "one"})
        self.assertEqual(len(engine.client.requests), 1)

    def test_default_client_initialized_once(self):
        client = MockLLMClient(["NO_CHANGES", "NO_CHANGES"])
        with patch("agent.mutation.mutation.LLMClient.from_env", return_value=client) as factory:
            engine = CodeMutationEngine()
            engine.mutate("Keep", {"a.py": "one"})
            engine.mutate("Keep", {"a.py": "one"})
            factory.assert_called_once_with(profile="low")


if __name__ == "__main__":
    unittest.main(verbosity=2)
