"""Offline checks for structured, best-effort run logging."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent.log import RunLogger


class RunLogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'storage/run_log.jsonl'
        self.logger = RunLogger(self.path)

    def test_append_schema_unicode_and_newlines(self):
        self.assertTrue(self.logger.emit('run.started', component='runner', run_id='abc',
                                         message='café\nsecond line'))
        self.assertTrue(self.logger.emit('run.finished', component='runner', run_id='abc'))
        rows = [json.loads(line) for line in self.path.read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['data']['message'], 'café\nsecond line')
        self.assertEqual(rows[0]['schema_version'], 1)
        self.assertEqual(rows[0]['run_id'], 'abc')
        self.assertIsNotNone(datetime.fromisoformat(rows[0]['timestamp']).tzinfo)

    def test_threads_and_multiple_logger_instances(self):
        def emit(index):
            return RunLogger(self.path).emit('test', component='test', index=index)
        with ThreadPoolExecutor(max_workers=8) as executor:
            self.assertTrue(all(executor.map(emit, range(100))))
        rows = [json.loads(line) for line in self.path.read_text().splitlines()]
        self.assertEqual({r['data']['index'] for r in rows}, set(range(100)))

    def test_failures_do_not_raise_or_leak_exception_text(self):
        with patch.object(Path, 'open', side_effect=PermissionError('SECRET')), \
                patch('sys.stderr', new_callable=io.StringIO) as stderr:
            self.assertFalse(self.logger.emit('test', component='test'))
        self.assertIn('PermissionError', stderr.getvalue())
        self.assertNotIn('SECRET', stderr.getvalue())
        with patch('sys.stderr', new_callable=io.StringIO):
            self.assertFalse(self.logger.emit('test', component='test', score=float('nan')))
        self.assertFalse(self.path.exists())


if __name__ == '__main__':
    unittest.main()
