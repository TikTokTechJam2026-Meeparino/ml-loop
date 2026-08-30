"""Offline environment tests using a tiny local wheel; no package index needed."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent.sandbox.environment import EnvironmentManager, pinned_requirements
from agent.sandbox.runner import Runner
from agent.log import RunLogger


class EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'workspace'
        self.workspace.mkdir()
        self.artifacts = self.root / 'logs'
        self.artifacts.mkdir()
        self.wheels = self.root / 'wheels'
        self.wheels.mkdir()
        self.log_path = self.root / 'run_log.jsonl'
        self.manager = EnvironmentManager(self.root / 'environments', wheelhouse=self.wheels,
                                          logger=RunLogger(self.log_path))
        self.requirements = self.workspace / 'requirements.txt'
        self.requirements.write_text('runner-fixture==1.0\n')
        wheel = self.wheels / 'runner_fixture-1.0-py3-none-any.whl'
        with zipfile.ZipFile(wheel, 'w') as archive:
            archive.writestr('runner_fixture.py', 'VALUE = 1\n')
            archive.writestr('runner_fixture-1.0.dist-info/METADATA',
                             'Metadata-Version: 2.1\nName: runner-fixture\nVersion: 1.0\n')
            archive.writestr('runner_fixture-1.0.dist-info/WHEEL',
                             'Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
            archive.writestr('runner_fixture-1.0.dist-info/RECORD', '')

    def prepare(self):
        return self.manager.prepare(self.workspace, self.artifacts, time.monotonic() + 60)

    def test_pin_validation(self):
        self.assertEqual(pinned_requirements('# comment\na_b==1.2.3\n'), {'a-b': '1.2.3'})
        for text in ('numpy>=1', '-r other.txt', 'https://example.com/a.whl', '-e .',
                     'a==1; python_version>"3"', 'a[x]==1', 'a==1\na==2', 'a==1.*'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                pinned_requirements(text)

    def test_isolation_reuse_and_requirement_identity(self):
        first = self.prepare()
        self.assertNotEqual(first.python, sys.executable)
        self.assertEqual(first.metadata['packages']['runner-fixture'], '1.0')
        self.assertNotIn('numpy', first.metadata['packages'])
        self.assertNotIn('litellm', first.metadata['packages'])
        self.assertFalse((self.workspace / '.venv').exists())
        with patch.object(self.manager, '_run', wraps=self.manager._run) as commands:
            second = self.prepare()
        self.assertEqual(first, second)
        self.assertFalse(any('install' in call.args[0] or 'venv' in call.args[0]
                             for call in commands.call_args_list))
        self.requirements.write_text('# new declaration\nrunner-fixture==1.0\n')
        third = self.prepare()
        self.assertNotEqual(first.metadata['key'], third.metadata['key'])
        self.assertNotEqual(first.python, third.python)

    def test_polluted_cache_rejected(self):
        environment = self.prepare()
        site = json.loads(subprocess.check_output([environment.python, '-I', '-c',
            'import json, sysconfig; print(json.dumps(sysconfig.get_path("purelib")))'], text=True))
        extra = Path(site) / 'unexpected-1.0.dist-info'
        extra.mkdir()
        (extra / 'METADATA').write_text('Metadata-Version: 2.1\nName: unexpected\nVersion: 1.0\n')
        with self.assertRaisesRegex(ValueError, 'environment changed'):
            self.prepare()

    def test_install_failure_is_logged_and_not_cached(self):
        self.requirements.write_text('unavailable-runner-package==1.0\n')
        with self.assertRaises(subprocess.CalledProcessError):
            self.prepare()
        self.assertEqual(list(self.manager.cache_dir.iterdir()), [])
        logs = (self.artifacts / 'environment.stderr.log').read_text()
        self.assertIn('unavailable-runner-package', logs)
        # A transient failed build does not poison the cache/retry path.
        self.requirements.write_text('runner-fixture==1.0\n')
        self.prepare()

    def test_incomplete_cache_and_timeout(self):
        environment = self.prepare()
        directory = Path(environment.python).parent.parent
        (directory / 'environment.json').unlink()
        with self.assertRaisesRegex(RuntimeError, 'incomplete'):
            self.prepare()
        with self.assertRaises(TimeoutError):
            self.manager.prepare(self.workspace, self.artifacts, time.monotonic() - 1)

    def test_cleanup_failure_preserves_original_and_records_leftover(self):
        original = subprocess.CalledProcessError(1, ['pip'], stderr=b'SECRET')
        with patch.object(self.manager, '_run', side_effect=['{}', original]), \
                patch('agent.sandbox.environment.shutil.rmtree', side_effect=PermissionError(13, 'locked')):
            with self.assertRaises(subprocess.CalledProcessError) as raised:
                self.manager.prepare(self.workspace, self.artifacts, time.monotonic() + 60, run_id='test-run')
        self.assertIs(raised.exception, original)
        records = [json.loads(line) for line in self.log_path.read_text().splitlines()]
        warning = next(r for r in records if r['event'] == 'environment.cleanup_failed')
        self.assertEqual(warning['run_id'], 'test-run')
        self.assertEqual(warning['level'], 'warning')
        self.assertEqual(warning['data']['cleanup_error_type'], 'PermissionError')
        self.assertEqual(warning['data']['original_error_type'], 'CalledProcessError')
        self.assertEqual(warning['data']['errno'], 13)
        leftover = Path(warning['data']['directory'])
        self.assertTrue(leftover.is_dir())
        self.assertFalse((leftover / 'environment.json').exists())
        self.assertNotIn('SECRET', self.log_path.read_text())
        with patch.object(self.manager, '_run', return_value='{}'):
            with self.assertRaisesRegex(RuntimeError, 'incomplete'):
                self.prepare()

    def test_cleanup_and_logging_failure_still_preserve_original(self):
        # The log destination is a directory: writing events fails too.
        self.manager.logger = RunLogger(self.root)
        original = TimeoutError('original provisioning timeout')
        with patch.object(self.manager, '_run', side_effect=['{}', original]), \
                patch('agent.sandbox.environment.shutil.rmtree', side_effect=PermissionError('locked')), \
                patch('sys.stderr'):
            with self.assertRaises(TimeoutError) as raised:
                self.prepare()
        self.assertIs(raised.exception, original)

    def test_stdlib_candidate_and_dependency_resume_guard(self):
        for name in ('config.py', 'features.py'):
            (self.workspace / name).write_text('# no additional dependencies\n')
        (self.workspace / 'train.py').write_text('''
import importlib.util
import json
from pathlib import Path
from agent.sandbox.protocol import evaluate
def train(train_rows, valid_rows, checkpoint_path, overrides, context):
    assert importlib.util.find_spec('numpy') is None
    assert importlib.util.find_spec('litellm') is None
    evaluate(['user'], [1], [0.5])
    path = Path(checkpoint_path)
    if path.exists():
        assert json.loads(path.read_text()) == context, 'incompatible environment'
    else:
        path.write_text(json.dumps(context))
''')
        (self.workspace / 'model.py').write_text('''
from runner_fixture import VALUE
class Predictor:
    def predict(self, rows):
        return [VALUE * row[5] for row in rows]
def load_predictor(path):
    return Predictor()
''')
        runner = Runner(self.root / 'runs', self.root / 'checkpoints',
                        environment_dir=self.manager.cache_dir, wheelhouse=self.wheels,
                        log_path=self.log_path)
        rows = [(20220408, 'u', 'v', 'a', 't', 1.0, 1),
                (20220408, 'u', 'v', 'a', 't', 0.0, 0)]
        kwargs = dict(splits={'train': rows, 'valid': rows}, timeout_s=60)
        first = runner.run(self.workspace, **kwargs)
        self.assertEqual(first.status, 'success', first.error)
        metadata = json.loads((Path(first.artifact_dir) / 'result.json').read_text())
        self.assertEqual(metadata['environment']['packages']['runner-fixture'], '1.0')
        before = Path(first.checkpoint_path).read_bytes()
        resumed = runner.run(self.workspace, checkpoint_path=first.checkpoint_path, **kwargs)
        self.assertEqual(resumed.status, 'success', resumed.error)
        self.requirements.write_text('# changed dependency lock\nrunner-fixture==1.0\n')
        failed = runner.run(self.workspace, checkpoint_path=first.checkpoint_path, **kwargs)
        self.assertEqual(failed.status, 'failed')
        self.assertEqual(Path(first.checkpoint_path).read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
