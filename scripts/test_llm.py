"""Run offline checks by default; --live sends one small paid API request."""

import argparse
import sys
import unittest
from dataclasses import asdict
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.llm.client import LLMClient, LLMConfig, LLMError, TokenUsage


def response(usage=True):
    result = {
        "model": "test/model",
        "choices": [{"message": {"content": "OK"}, "finish_reason": "stop"}],
    }
    if usage:
        result["usage"] = {"prompt_tokens": 5, "completion_tokens": 1, "total_tokens": 6}
    return result


class ClientTests(unittest.TestCase):
    def client(self, transport, **options):
        return LLMClient(LLMConfig(model="test/model", **options), transport=transport, sleep=lambda _: None)

    def test_usage_and_model_override(self):
        transport = Mock(return_value=response())
        client = self.client(transport, api_base="http://localhost:1234/v1")
        result = client.complete(
            [{"role": "system", "content": "Be brief"}, {"role": "user", "content": "Hello"}],
            model="test/other",
        )
        client.complete([{"role": "user", "content": "Again"}])
        self.assertEqual(result.text, "OK")
        self.assertEqual(client.total_usage, TokenUsage(10, 2, 12))
        args = transport.call_args_list[0].kwargs
        self.assertEqual(args["model"], "test/other")
        self.assertEqual(args["api_base"], "http://localhost:1234/v1")
        self.assertEqual(args["num_retries"], 0)

    def test_retry_then_success(self):
        transport = Mock(side_effect=[TimeoutError(), response()])
        self.assertEqual(self.client(transport).complete([{"role": "user", "content": "Hello"}]).attempts, 2)

    def test_retry_exhaustion(self):
        transport = Mock(side_effect=TimeoutError("secret"))
        with self.assertRaises(LLMError):
            self.client(transport, max_retries=2).complete([{"role": "user", "content": "Hello"}])
        self.assertEqual(transport.call_count, 3)

    def test_rate_limit_retries(self):
        error = RuntimeError("rate limited")
        error.status_code = 429
        transport = Mock(side_effect=[error, response()])
        self.assertEqual(self.client(transport).complete([{"role": "user", "content": "Hello"}]).attempts, 2)

    def test_auth_failure_is_not_retried_or_exposed(self):
        error = RuntimeError("secret-api-key")
        error.status_code = 401
        transport = Mock(side_effect=error)
        with self.assertRaises(LLMError) as caught:
            self.client(transport).complete([{"role": "user", "content": "Hello"}])
        self.assertNotIn("secret-api-key", str(caught.exception))
        self.assertEqual(transport.call_count, 1)

    def test_missing_usage_is_explicit(self):
        client = self.client(Mock(return_value=response(usage=False)))
        self.assertIsNone(client.complete([{"role": "user", "content": "Hello"}]).usage)
        self.assertEqual(client.responses_without_usage, 1)

    def test_placeholder_and_empty_messages_never_call_transport(self):
        transport = Mock()
        with self.assertRaises(ValueError):
            self.client(transport, api_key="<YOUR-API-KEY>").complete([{"role": "user", "content": "Hello"}])
        with self.assertRaises(ValueError):
            self.client(transport).complete([{"role": "user", "content": ""}])
        with self.assertRaises(ValueError):
            self.client(transport).complete([])
        transport.assert_not_called()

    def test_empty_response_preserves_reported_usage(self):
        raw = response()
        raw["choices"][0]["message"]["content"] = None
        client = self.client(Mock(return_value=raw))
        with self.assertRaises(LLMError):
            client.complete([{"role": "user", "content": "Hello"}])
        self.assertEqual(client.total_usage.total_tokens, 6)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Send a request using root .env")
    args = parser.parse_args()
    if not args.live:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ClientTests))
        return 0 if result.wasSuccessful() else 1
    try:
        client = LLMClient.from_env()
        result = client.complete(
            [{"role": "user", "content": "Reply with only the word OK."}], max_tokens=128
        )
    except (ValueError, LLMError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"Response: {result.text}")
    print(f"Model: {result.model}; attempts: {result.attempts}; finish: {result.finish_reason}")
    print(f"Usage: {asdict(result.usage) if result.usage else 'not reported by provider'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
