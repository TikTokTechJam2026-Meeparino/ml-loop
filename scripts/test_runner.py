"""Runner integration checks. Optional --real-data runs a bounded raw-data smoke test."""
import importlib.util
import json
import os
from pathlib import Path
import pickle
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent.sandbox.runner import Runner
from agent.sandbox.protocol import STARTER, load


def fixture():
    return {name: [(date, str(i % 8), str(i % 13), str(i % 3), str(i % 2),
                    float(i % 23), int((i * 7 + i // 8) % 5 < 2)) for i in range(160)]
            for name, date in [('train', 20220408), ('valid', 20220422), ('test', 20220429)]}


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'workspace'
        shutil.copytree(ROOT / 'workspace_template', self.workspace)
        self.runner = Runner(self.root / 'runs', self.root / 'checkpoints',
                             wheelhouse=os.environ.get('RUNNER_TEST_WHEELHOUSE'),
                             log_path=self.root / 'run_log.jsonl')
        self.splits = fixture()
        self.config = dict(epochs=4, bs=32, patience=4)

    def run_model(self, **kwargs):
        return self.runner.run(self.workspace, splits=self.splits, overrides=self.config, **kwargs)

    def assert_success(self, result):
        logs = '\n'.join(p.read_text() for p in Path(result.artifact_dir).glob('*.log'))
        self.assertEqual(result.status, 'success', str(result) + logs)

    def test_reference_parity_and_inference(self):
        result = self.run_model()
        self.assert_success(result)
        records = [json.loads(line) for line in self.runner.logger.path.read_text().splitlines()]
        self.assertEqual(records[0]['event'], 'run.started')
        self.assertEqual(records[-1]['event'], 'run.finished')
        self.assertEqual(records[-1]['data']['status'], 'success')
        self.assertTrue(all(r['run_id'] == Path(result.artifact_dir).name for r in records))
        with patch.dict(sys.modules):
            sys.path.insert(0, str(STARTER))
            try:
                spec = importlib.util.spec_from_file_location('reference_baseline', STARTER / 'baseline.py')
                baseline = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(baseline)
                captured = []
                original_evaluate = baseline.evaluate
                def capture(users, labels, scores):
                    captured.append(np.asarray(scores).copy())
                    return original_evaluate(users, labels, scores)
                baseline.evaluate = capture
                expected = baseline.run_fm(self.splits, **self.config, verbose=False)
            finally:
                sys.path.remove(str(STARTER))
        for key in ('GAUC', 'nDCG@5', 'primary'):
            self.assertAlmostEqual(result.scores[key], float(expected['valid'][key]), places=6)
        np.testing.assert_array_equal(np.load(Path(result.artifact_dir) / 'predictions.npy'), captured[-2])
        before = Path(result.checkpoint_path).read_bytes()
        test = self.run_model(train=False, split='test', checkpoint_path=result.checkpoint_path)
        self.assert_success(test)
        for key in ('GAUC', 'nDCG@5', 'primary'):
            self.assertAlmostEqual(test.scores[key], float(expected['test'][key]), places=6)
        np.testing.assert_array_equal(np.load(Path(test.artifact_dir) / 'predictions.npy'), captured[-1])
        self.assertIsNone(test.metrics)  # Test metrics never masquerade as validation.
        self.assertEqual(before, Path(result.checkpoint_path).read_bytes())
        again = self.run_model(checkpoint_path=result.checkpoint_path)
        self.assert_success(again)
        self.assertEqual(before, Path(result.checkpoint_path).read_bytes())

    def test_process_crash_then_exact_resume(self):
        # Test-only fault injection: kill the actual worker after atomic save.
        with (self.workspace / 'train.py').open('a') as stream:
            stream.write('''
_real_save = save_checkpoint
def save_checkpoint(path, payload):
    _real_save(path, payload)
    if os.environ.get('RUNNER_TEST_CRASH') == '1':
        os._exit(23)
''')
        uninterrupted = self.run_model()
        self.assert_success(uninterrupted)
        with patch.dict(os.environ, RUNNER_TEST_CRASH='1'):
            crashed = self.run_model()
        self.assertEqual(crashed.status, 'failed')
        with open(crashed.checkpoint_path, 'rb') as stream:
            self.assertEqual(pickle.load(stream)['training_state']['epoch'], 1)
        resumed = self.run_model(checkpoint_path=crashed.checkpoint_path)
        self.assert_success(resumed)
        self.assertEqual(resumed.scores, uninterrupted.scores)
        states = []
        for result in (uninterrupted, resumed):
            with open(result.checkpoint_path, 'rb') as stream:
                states.append(pickle.load(stream))
        for key in states[0]['training_state']['latest']:
            np.testing.assert_array_equal(states[0]['training_state']['latest'][key],
                                          states[1]['training_state']['latest'][key])
        self.assertEqual(states[0]['training_state']['rng'], states[1]['training_state']['rng'])
        for key in states[0]['model_state']:
            np.testing.assert_array_equal(states[0]['model_state'][key], states[1]['model_state'][key])
        np.testing.assert_array_equal(np.load(Path(uninterrupted.artifact_dir) / 'predictions.npy'),
                                      np.load(Path(resumed.artifact_dir) / 'predictions.npy'))

    def test_incompatible_and_corrupt_checkpoints_preserved(self):
        result = self.run_model()
        self.assert_success(result)
        path = Path(result.checkpoint_path)
        before = path.read_bytes()
        self.config['lr'] = 0.02
        self.assertEqual(self.run_model(checkpoint_path=path).status, 'failed')
        self.assertEqual(before, path.read_bytes())
        path.write_bytes(b'corrupt')
        self.assertEqual(self.run_model(checkpoint_path=path).status, 'failed')
        self.assertEqual(path.read_bytes(), b'corrupt')

    def test_timeout(self):
        with (self.workspace / 'train.py').open('a') as stream:
            stream.write('\ndef train(*args):\n    import time\n    time.sleep(30)\n')
        result = self.run_model(timeout_s=0.5)
        self.assertEqual(result.status, 'timeout')
        self.assertLess(result.elapsed_s, 5)
        terminal = json.loads(self.runner.logger.path.read_text().splitlines()[-1])
        self.assertEqual(terminal['data']['status'], 'timeout')

    def test_checkpoint_environment_identity_is_required(self):
        result = self.run_model()
        self.assert_success(result)
        path = Path(result.checkpoint_path)
        payload = pickle.loads(path.read_bytes())
        environment = payload['context']['environment']
        self.assertEqual(environment['packages']['numpy'], '2.5.2')
        self.assertNotIn('litellm', environment['packages'])
        environment['key'] = 'different-environment'
        path.write_bytes(pickle.dumps(payload))
        before = path.read_bytes()
        failed = self.run_model(checkpoint_path=path)
        self.assertEqual(failed.status, 'failed')
        self.assertEqual(path.read_bytes(), before)

    def test_data_and_source_mismatch(self):
        result = self.run_model()
        self.assert_success(result)
        before = Path(result.checkpoint_path).read_bytes()
        self.splits['train'][0] = (*self.splits['train'][0][:6], 1 - self.splits['train'][0][6])
        self.assertEqual(self.run_model(checkpoint_path=result.checkpoint_path).status, 'failed')
        self.splits = fixture()
        with (self.workspace / 'config.py').open('a') as stream:
            stream.write('\n# changed candidate\n')
        self.assertEqual(self.run_model(checkpoint_path=result.checkpoint_path).status, 'failed')
        self.assertEqual(before, Path(result.checkpoint_path).read_bytes())

    def test_failed_atomic_save_keeps_previous_epoch(self):
        with (self.workspace / 'train.py').open('a') as stream:
            stream.write('''
_real_dump = pickle.dump
_dump_count = 0
def broken_dump(payload, stream, **kwargs):
    global _dump_count
    _dump_count += 1
    if os.environ.get('RUNNER_TEST_SAVE_FAILURE') and _dump_count == 2:
        stream.write(b'incomplete payload')
        raise OSError('injected save failure')
    return _real_dump(payload, stream, **kwargs)
pickle.dump = broken_dump
''')
        with patch.dict(os.environ, RUNNER_TEST_SAVE_FAILURE='1'):
            failed = self.run_model()
        self.assertEqual(failed.status, 'failed')
        with open(failed.checkpoint_path, 'rb') as stream:
            self.assertEqual(pickle.load(stream)['training_state']['epoch'], 1)
        self.assertEqual(list(Path(failed.checkpoint_path).parent.glob('.checkpoint-*')), [])
        self.assert_success(self.run_model(checkpoint_path=failed.checkpoint_path))

    def test_prediction_contract(self):
        result = self.run_model()
        self.assert_success(result)
        original = (self.workspace / 'model.py').read_text()
        for expression in ('[0.0]', '[float("nan")] * len(rows)', '[[0.0]] * len(rows)'):
            (self.workspace / 'model.py').write_text(original + f'''
class BadPredictor:
    def predict(self, rows):
        assert all(len(row) == 6 for row in rows)
        return {expression}
def load_predictor(path):
    return BadPredictor()
''')
            failed = self.run_model(train=False, checkpoint_path=result.checkpoint_path)
            self.assertEqual(failed.status, 'failed')
            self.assertIsNone(failed.metrics)

    def test_empty_split_and_fresh_paths(self):
        first, second = self.run_model(), self.run_model()
        self.assert_success(first)
        self.assert_success(second)
        self.assertNotEqual(first.checkpoint_path, second.checkpoint_path)
        self.splits['valid'] = []
        self.assertEqual(self.run_model().status, 'failed')

    def test_early_stopped_checkpoint_is_not_retrained(self):
        self.config.update(epochs=8, lr=1e-20, patience=2)
        result = self.run_model()
        self.assert_success(result)
        before = Path(result.checkpoint_path).read_bytes()
        state = pickle.loads(before)
        self.assertEqual(state['best_epoch'], 1)
        self.assertEqual(state['training_state']['epoch'], 3)
        self.assertEqual(state['training_state']['bad'], 2)
        resumed = self.run_model(checkpoint_path=result.checkpoint_path)
        self.assert_success(resumed)
        self.assertEqual(before, Path(result.checkpoint_path).read_bytes())

    def test_training_success_without_checkpoint_is_failure(self):
        with (self.workspace / 'train.py').open('a') as stream:
            stream.write('\ndef train(*args):\n    pass\n')
        result = self.run_model()
        self.assertEqual(result.status, 'failed')
        self.assertIn('did not produce', result.error)
        terminal = json.loads(self.runner.logger.path.read_text().splitlines()[-1])
        self.assertEqual(terminal['data']['status'], 'failed')


def real_smoke():
    splits = load(ROOT / 'data/kuairand-pure/KuaiRand-Pure/data')
    # Deliberately bounded, ordered subset; NOT a full benchmark result.
    splits = {name: rows[:10000] for name, rows in splits.items()}
    result = Runner(ROOT / 'storage/runner-smoke', ROOT / 'checkpoints').run(
        ROOT / 'workspace_template', splits=splits, overrides=dict(epochs=3, bs=1024), timeout_s=180)
    print(result)
    if result.status != 'success':
        raise SystemExit(1)
    result = Runner(ROOT / 'storage/runner-smoke').run(
        ROOT / 'workspace_template', splits=splits, train=False, split='test',
        checkpoint_path=result.checkpoint_path, timeout_s=60)
    print(result)
    if result.status != 'success':
        raise SystemExit(1)


if __name__ == '__main__':
    if '--real-data' in sys.argv:
        real_smoke()
    else:
        unittest.main()
