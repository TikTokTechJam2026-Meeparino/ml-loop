"""Offline checks for the reusable LLM mock."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.llm.client import LLMError, LLMResponse, TokenUsage
from agent.llm.mock_client import MockLLMClient


class MockClientTests(unittest.TestCase):
    def test_queue_and_response_metadata(self):
        explicit = LLMResponse("partial", "provider/model", TokenUsage(2, 3, 5), "length", 2)
        client = MockLLMClient(["first", explicit])
        result = client.complete([], model="override/model", max_tokens=80)
        self.assertEqual(result.text, "first")
        self.assertEqual(result.model, "override/model")
        self.assertIsNone(result.usage)
        self.assertIs(client.complete([]), explicit)
        self.assertEqual(client.remaining_responses, 0)
        self.assertEqual(client.requests[0].max_tokens, 80)

    def test_exception_consumed_and_next_call_succeeds(self):
        error = LLMError("planned failure")
        client = MockLLMClient([error, "recovered"])
        with self.assertRaises(LLMError) as caught:
            client.complete([])
        self.assertIs(caught.exception, error)
        self.assertEqual(client.complete([]).text, "recovered")
        self.assertEqual(len(client.requests), 2)

    def test_exhaustion_is_recorded_and_fails(self):
        client = MockLLMClient([])
        with self.assertRaisesRegex(AssertionError, "exhausted"):
            client.complete([])
        self.assertEqual(len(client.requests), 1)

    def test_request_snapshot_and_queue_are_independent_of_inputs(self):
        responses = ["OK"]
        client = MockLLMClient(responses)
        responses.clear()
        messages = [{"role": "user", "content": "before"}]
        client.complete(messages)
        messages[0]["content"] = "after"
        messages.clear()
        self.assertEqual(client.requests[0].messages, [{"role": "user", "content": "before"}])

    def test_bad_response_configuration(self):
        for responses in ("NO_CHANGES", [123], [{}]):
            with self.subTest(responses=responses), self.assertRaises(TypeError):
                MockLLMClient(responses)


if __name__ == "__main__":
    unittest.main(verbosity=2)
