"""Offline coverage for diagnostic completeness and credential redaction."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.log import RunLogger
from agent.llm.client import LLMClient, LLMConfig, LLMError
from agent.diagnostics import exception_details, sanitize


class DiagnosticTests(unittest.TestCase):
    def test_full_payload_and_nested_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            logger = RunLogger(Path(directory) / 'events.jsonl')
            logger.secrets = ('private-key-123',)
            path = logger.diagnostic('request', component='test', text='x' * 30000,
                nested={'authorization': 'Bearer hidden', 'api_key': 'private-key-123'},
                url='https://user:pass@example.com/?api_key=hidden', echo='private-key-123')
            text = Path(path).read_text()
            self.assertNotIn('hidden', text)
            self.assertNotIn('private-key-123', text)
            self.assertNotIn('user:pass', text)
            self.assertEqual(len(json.loads(text)['text']), 30000)
            self.assertNotIn('x' * 100, logger.path.read_text())

    def test_exception_chain_and_subprocess_output(self):
        import subprocess
        try:
            try:
                raise subprocess.CalledProcessError(7, ['git', 'status'], stderr=b'precise failure')
            except Exception as cause:
                raise RuntimeError('outer') from cause
        except Exception as error:
            details = exception_details(error)
        self.assertIn('RuntimeError: outer', details['traceback'])
        self.assertEqual(details['cause']['returncode'], 7)
        self.assertEqual(details['cause']['stderr'], 'precise failure')

    def test_transport_retry_response_and_error_survive(self):
        rows = []
        error = RuntimeError('quota exceeded api_key=hidden')
        error.status_code = 429
        error.response = Mock(status_code=429, text='quota detail', headers={'retry-after': '2'})
        raw = {'choices': [{'message': {'content': 'full reply'}, 'finish_reason': 'stop'}],
               'usage': {'total_tokens': 9}}
        client = LLMClient(LLMConfig('test/model', api_key='configured-secret'),
                           transport=Mock(side_effect=[error, raw]), sleep=lambda _: None)
        client.complete([{'role': 'user', 'content': 'full prompt'}],
                        audit=lambda event, **data: rows.append((event, data)))
        self.assertEqual([row[0] for row in rows], ['transport.started', 'transport.failed',
            'transport.retry_scheduled', 'transport.started', 'transport.response'])
        self.assertEqual(rows[1][1]['exception']['status_code'], 429)
        self.assertEqual(rows[1][1]['exception']['response']['headers']['retry-after'], '2')
        self.assertNotIn('configured-secret', json.dumps(rows))
        self.assertNotIn('hidden', json.dumps(rows))
        self.assertEqual(rows[-1][1]['response'], raw)
        client._transport = Mock(side_effect=error)
        with self.assertRaises(LLMError) as caught:
            client.complete([{'role': 'user', 'content': 'again'}])
        self.assertEqual(caught.exception.details['status_code'], 429)

    def test_broken_audit_does_not_break_generation(self):
        raw = {'choices': [{'message': {'content': 'ok'}}]}
        client = LLMClient(LLMConfig('test/model'), transport=lambda **_: raw)
        result = client.complete([{'role': 'user', 'content': 'hello'}],
                                 audit=Mock(side_effect=OSError('disk full')))
        self.assertEqual(result.text, 'ok')


if __name__ == '__main__':
    unittest.main()
