"""Offline deadline, generation publication, and process-lock checks."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.budget import BudgetClient, BudgetExhausted, RunBudget
from agent.llm.mock_client import MockLLMClient
from agent.graph.memory import ExplorationMemory
from agent.llm.client import LLMClient, LLMConfig, LLMError
from agent.run_state import RunStore


class BudgetStateTests(unittest.TestCase):
    def test_response_callback_observes_request_duration(self):
        budget = Mock()
        budget.allowance.return_value = 30
        observed = []
        client = BudgetClient(MockLLMClient(["answer"]), budget, 100,
                              on_response=lambda response: observed.append(client.last_elapsed_s))
        with patch("agent.budget.time.monotonic", side_effect=[10.0, 12.5]):
            client.complete([{"role": "user", "content": "private prompt"}])
        self.assertEqual(observed, [2.5])

    def test_final_reserve_and_wall_clock_rollback(self):
        with patch("agent.budget.time.time", return_value=100), patch("agent.budget.time.monotonic", return_value=10):
            budget = RunBudget(100, 100, 20)
            self.assertEqual(budget.remaining(), 80)
        with patch("agent.budget.time.time", return_value=80), patch("agent.budget.time.monotonic", return_value=95):
            self.assertEqual(budget.remaining(), 0)
            self.assertEqual(budget.remaining(final=True), 15)
            with self.assertRaises(BudgetExhausted):
                budget.allowance(10)

    def test_llm_retry_timeout_and_sleep_respect_deadline(self):
        clock = [100.0]
        def transport(**kwargs):
            self.assertLessEqual(kwargs["timeout"], 2)
            clock[0] += 1.5
            raise TimeoutError()
        def sleep(seconds):
            self.assertLessEqual(seconds, .5)
            clock[0] += seconds
        client = LLMClient(LLMConfig("mock", timeout=60), transport=transport, sleep=sleep)
        with patch("agent.llm.client.time.monotonic", side_effect=lambda: clock[0]):
            with self.assertRaises(LLMError):
                client.complete([{"role": "user", "content": "test"}], deadline=102)
        self.assertEqual(clock[0], 102)

    def test_expired_llm_deadline_never_calls_transport(self):
        transport = Mock()
        client = LLMClient(LLMConfig("mock"), transport=transport)
        with self.assertRaises(LLMError):
            client.complete([{"role": "user", "content": "test"}], deadline=0)
        transport.assert_not_called()

    def test_incomplete_generation_does_not_replace_current(self):
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            store.save({"version": 1, "stage": "before"}, None, ExplorationMemory())
            with patch("agent.run_state.write_report", side_effect=OSError("disk failure")):
                with self.assertRaises(OSError):
                    store.save({"version": 1, "stage": "after"}, None, ExplorationMemory())
            state, _, _ = store.load()
            self.assertEqual(state["stage"], "before")

    def test_lock_released_on_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            with self.assertRaises(RuntimeError):
                with store.lock():
                    raise RuntimeError("interrupted")
            with store.lock():
                pass

    def test_second_owner_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with RunStore(directory).lock():
                with self.assertRaises(RuntimeError):
                    with RunStore(directory).lock():
                        self.fail("Concurrent ownership must be rejected")


if __name__ == "__main__":
    unittest.main(verbosity=2)
