"""Offline repair lifecycle checks: python -B scripts/test_recovery.py."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.llm.client import LLMError
from agent.llm.mock_client import MockLLMClient
from agent.mutation.mutation import CodeMutationEngine
from agent.mutation.parser import EditError
from agent.recovery import RecoveryEngine, RecoveryExhausted


EDIT = "FILE: model.py\n```python\n<<<<<<< SEARCH\nbroken\n=======\nfixed\n>>>>>>> REPLACE\n```"


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.files = {"model.py": "broken"}
        self.kwargs = dict(hypothesis="Test capacity", diagnostics="Shape mismatch",
                           constraints="Keep frozen evaluation")

    def engine(self, responses, limit=3):
        client = MockLLMClient(responses)
        return RecoveryEngine(CodeMutationEngine(client), max_attempts=limit), client

    def test_pending_then_success_and_diff(self):
        engine, client = self.engine([EDIT])
        proposal = engine.propose(self.files, **self.kwargs)
        self.assertEqual(proposal.files, {"model.py": "fixed"})
        self.assertEqual(self.files, {"model.py": "broken"})
        self.assertIn("-broken\n\\ No newline at end of file\n+fixed", proposal.raw_diff)
        self.assertEqual(engine.events, [])
        with self.assertRaises(RuntimeError):
            engine.propose(self.files, **self.kwargs)
        event = engine.record_result(succeeded=True)
        self.assertTrue(event.succeeded)
        self.assertEqual(event.raw_diff, proposal.raw_diff)
        self.assertEqual(engine.remaining_attempts, 0)
        with self.assertRaises(RecoveryExhausted):
            engine.propose(self.files, **self.kwargs)
        prompt = client.requests[0].messages[1]["content"]
        self.assertIn("Shape mismatch", prompt)
        self.assertIn("Keep frozen evaluation", prompt)

    def test_failed_execution_can_resume_from_completed_history(self):
        engine, _ = self.engine([EDIT], limit=2)
        engine.propose(self.files, **self.kwargs)
        engine.record_result(succeeded=False)
        restored = RecoveryEngine(CodeMutationEngine(MockLLMClient([EDIT])),
                                  max_attempts=2, history=engine.events)
        self.assertEqual(restored.propose(self.files, **self.kwargs).attempt, 2)
        restored.record_result(succeeded=False)
        with self.assertRaises(RecoveryExhausted):
            restored.propose(self.files, **self.kwargs)

    def test_errors_and_no_changes_consume_allowance(self):
        engine, client = self.engine([LLMError("redacted"), "bad edits", "NO_CHANGES"])
        for error in (LLMError, EditError):
            with self.assertRaises(error):
                engine.propose(self.files, **self.kwargs)
        self.assertIsNone(engine.propose(self.files, **self.kwargs))
        self.assertEqual([e.attempt for e in engine.events], [1, 2, 3])
        self.assertTrue(all(not e.succeeded for e in engine.events))
        with self.assertRaises(RecoveryExhausted):
            engine.propose(self.files, **self.kwargs)
        self.assertEqual(len(client.requests), 3)

    def test_invalid_input_and_zero_allowance_make_no_calls(self):
        engine, client = self.engine([])
        with self.assertRaises(ValueError):
            engine.propose({"../bad.py": "x"}, **self.kwargs)
        self.assertEqual(engine.remaining_attempts, 3)
        self.assertEqual(client.requests, [])
        engine, _ = self.engine([], limit=0)
        with self.assertRaises(RecoveryExhausted):
            engine.propose(self.files, **self.kwargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
