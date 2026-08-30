"""Offline checks for stage routing and isolated provider credentials."""
import os
import unittest
from unittest.mock import Mock, patch

from agent.budget import BudgetClient
from agent.llm.client import LLMClient, LLMConfig


class ProfileTests(unittest.TestCase):
    def config(self, values, profile):
        with patch.dict(os.environ, values, clear=True), patch('dotenv.load_dotenv'):
            return LLMConfig.from_env(profile=profile)

    def test_base_model_is_not_a_fallback(self):
        for profile in ('high', 'low'):
            with self.assertRaisesRegex(ValueError, f'LLM_{profile.upper()}_MODEL'):
                self.config({'LLM_MODEL': 'gemini/legacy'}, profile)

    def test_independent_profiles(self):
        values = {'LLM_API_KEY': 'shared',
                  'LLM_HIGH_MODEL': 'openai/high-model', 'LLM_HIGH_API_KEY': 'high-key',
                  'LLM_HIGH_API_BASE': 'https://high.invalid',
                  'LLM_HIGH_REASONING_EFFORT': 'high', 'LLM_HIGH_TIMEOUT': '180',
                  'LLM_LOW_MODEL': 'gemini/low-model', 'LLM_LOW_REASONING_EFFORT': 'low'}
        high, low = self.config(values, 'high'), self.config(values, 'low')
        self.assertEqual((high.model, high.api_key, high.reasoning_effort, high.timeout),
                         ('openai/high-model', 'high-key', 'high', 180))
        self.assertEqual(high.api_base, 'https://high.invalid')
        self.assertEqual(low.api_key, '')
        self.assertIsNone(low.api_base)

    def test_all_shared_settings_are_ignored(self):
        values = {'LLM_LOW_MODEL': 'test/low', 'LLM_API_KEY': 'unused',
                  'LLM_API_BASE': 'https://unused.invalid', 'LLM_TIMEOUT': '999',
                  'LLM_MAX_RETRIES': '99', 'LLM_MAX_TOKENS': '99999',
                  'LLM_REASONING_EFFORT': 'high'}
        config = self.config(values, 'low')
        self.assertEqual(config.api_key, '')
        self.assertIsNone(config.api_base)
        self.assertEqual((config.timeout, config.max_retries, config.max_tokens), (60, 2, 1024))
        self.assertIsNone(config.reasoning_effort)

    def test_unqualified_client_uses_low_profile(self):
        config = self.config({'LLM_HIGH_MODEL': 'test/high', 'LLM_LOW_MODEL': 'test/low'}, None)
        self.assertEqual(config.model, 'test/low')

    def test_routing_caches_clients_and_shares_callbacks(self):
        raw = {'choices': [{'message': {'content': 'answer'}, 'finish_reason': 'stop'}]}
        high_transport, low_transport = Mock(return_value=raw), Mock(return_value=raw)
        clients = {'high': LLMClient(LLMConfig('test/high', reasoning_effort='high'), transport=high_transport),
                   'low': LLMClient(LLMConfig('test/low', reasoning_effort='low'), transport=low_transport)}
        budget = Mock()
        budget.allowance.return_value = 60
        profile = ['high']
        on_request = Mock()
        client = BudgetClient(None, budget, 100, profile=lambda: profile[0], on_request=on_request)
        with patch.object(LLMClient, 'from_env', side_effect=lambda **kw: clients[kw['profile']]) as factory:
            for name in ('high', 'low', 'high'):
                profile[0] = name
                client.complete([{'role': 'user', 'content': 'hello'}])
        self.assertEqual(factory.call_count, 2)
        self.assertEqual(on_request.call_count, 3)
        self.assertEqual(high_transport.call_count, 2)
        self.assertEqual(low_transport.call_args.kwargs['reasoning_effort'], 'low')
        self.assertEqual(high_transport.call_args.kwargs['reasoning_effort'], 'high')


if __name__ == '__main__':
    unittest.main()
