"""Execute candidate training and independent inference with a shared timeout.

Only trusted local pipelines/checkpoints may be executed. Subprocesses are not
an OS sandbox. No automatic repair or retry: rerun with the returned checkpoint
path to recover. A new invocation gets a fresh checkpoint unless explicitly set.
"""
from dataclasses import asdict, dataclass
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import uuid

import numpy as np

from agent.graph.node import MetricResult
from agent.log import RunLogger
from agent.sandbox.protocol import evaluate, load, STARTER
from agent.sandbox.environment import EnvironmentManager, clean_environment


@dataclass(frozen=True)
class RunResult:
    status: str
    checkpoint_path: str
    artifact_dir: str
    metrics: MetricResult | None
    scores: dict | None
    elapsed_s: float
    error: str | None = None
    failure_kind: str | None = None


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


class Runner:
    def __init__(self, storage_dir='storage/runs', checkpoint_dir='checkpoints', python=None,
                 environment_dir='storage/environments', wheelhouse=None,
                 log_path='storage/run_log.jsonl'):
        self.storage_dir = Path(storage_dir).resolve()
        self.checkpoint_dir = Path(checkpoint_dir).resolve()
        self.python = str(Path(python or sys.executable).resolve())
        self.logger = RunLogger(log_path)
        self.environments = EnvironmentManager(environment_dir, self.python, wheelhouse, self.logger)

    def run(self, workspace_dir, *, data_dir=None, splits=None, overrides=None,
            checkpoint_path=None, timeout_s=3600, split='valid', train=True, attempt_id=None):
        """Train on train/valid, then score valid (or explicitly requested test).

        Supply either raw data_dir or preloaded splits. Timeout covers environment
        provisioning and workers;
        data loading/scoring are synchronous and count toward elapsed time.
        Explicit checkpoint reuse requires identical source, data, config and environment.
        Each attempt persists result.json, logs, and successful predictions.npy.
        """
        if split not in ('valid', 'test') or not np.isfinite(timeout_s) or timeout_s <= 0:
            raise ValueError('invalid split or timeout')
        if (data_dir is None) == (splits is None):
            raise ValueError('provide exactly one of data_dir or splits')
        workspace = Path(workspace_dir).resolve()
        if not all((workspace / name).is_file() for name in ('config.py', 'features.py', 'model.py', 'train.py')):
            raise ValueError('workspace must contain all four pipeline modules')
        if attempt_id is not None and (not isinstance(attempt_id, str)
                                      or re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', attempt_id) is None):
            raise ValueError('invalid attempt_id')
        run_id = attempt_id if attempt_id is not None else uuid.uuid4().hex
        artifacts = self.storage_dir / run_id
        artifacts.mkdir(parents=True)
        checkpoint = Path(checkpoint_path).resolve() if checkpoint_path else self.checkpoint_dir / (run_id + '.pkl')
        if checkpoint == workspace or workspace in checkpoint.parents:
            raise ValueError('checkpoint must live outside candidate source workspace')
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        deadline = started + timeout_s
        scores = metrics = error = None
        status = 'failed'
        context = None
        environment = None
        error_type = None
        failure_kind = None
        phase = 'environment'
        self.logger.emit('run.started', component='runner', run_id=run_id,
                         workspace=str(workspace), artifact_dir=str(artifacts),
                         checkpoint_path=str(checkpoint), training=train, split=split)
        try:
            environment = self.environments.prepare(workspace, artifacts, deadline, run_id=run_id)
            phase = 'data'
            splits = load(data_dir) if splits is None else splits
            required = {'train', 'valid', split} if train else {split}
            for name in required:
                if not splits.get(name):
                    raise ValueError(f'empty or missing {name} split')
                for row in splits[name]:
                    if len(row) != 7 or row[6] not in (0, 1):
                        raise ValueError('expected seven-column rows with binary long_view')
            context = {
                'environment': environment.metadata,
                'source': _digest({str(p.relative_to(workspace)): p.read_text(encoding='utf-8')
                                   for p in sorted(workspace.rglob('*.py'))}),
                'protocol': _digest({n: (STARTER / n).read_text(encoding='utf-8')
                                     for n in ('data.py', 'evaluate.py')}),
            }
            if train:
                context['data'] = _digest({n: splits[n] for n in ('train', 'valid')})
            phase = 'candidate'
            with tempfile.TemporaryDirectory(prefix='runner-', dir=artifacts) as temporary:
                request = Path(temporary) / 'request.json'
                if train:
                    request.write_text(json.dumps({'train': splits['train'], 'valid': splits['valid'],
                        'overrides': overrides or {}, 'context': context}, allow_nan=False), encoding='utf-8')
                    self._worker('train', workspace, request, checkpoint, artifacts, deadline, environment)
                if not checkpoint.is_file():
                    raise ValueError('training did not produce the supplied checkpoint')
                checkpoint_hash = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
                request.write_text(json.dumps({'rows': [r[:6] for r in splits[split]]}, allow_nan=False), encoding='utf-8')
                self._worker('predict', workspace, request, checkpoint, artifacts, deadline, environment)
                if hashlib.sha256(checkpoint.read_bytes()).hexdigest() != checkpoint_hash:
                    raise ValueError('inference modified the checkpoint')
            current_source = _digest({str(p.relative_to(workspace)): p.read_text(encoding='utf-8')
                                      for p in sorted(workspace.rglob('*.py'))})
            if current_source != context['source']:
                raise ValueError('candidate modified its source during execution')
            predictions = np.asarray(json.loads((artifacts / 'predictions.json').read_text(encoding='utf-8')),
                                     dtype=np.float64)
            if predictions.shape != (len(splits[split]),) or not np.isfinite(predictions).all():
                raise ValueError('invalid prediction shape or nonfinite scores')
            np.save(artifacts / 'predictions.npy', predictions, allow_pickle=False)
            (artifacts / 'predictions.json').unlink()
            scores = evaluate([r[1] for r in splits[split]], [r[6] for r in splits[split]], predictions)
            elapsed = time.monotonic() - started
            if elapsed > timeout_s:
                raise TimeoutError('candidate wall-clock budget exhausted')
            if split == 'valid':
                metrics = MetricResult(scores['GAUC'], scores['nDCG@5'], scores['primary'], elapsed)
            status = 'success'
        except (subprocess.TimeoutExpired, TimeoutError) as exc:
            self.logger.exception('execution.failed', exc, component='runner', run_id=run_id,
                                  phase=phase, artifact_dir=str(artifacts))
            error_type = type(exc).__name__
            status, error = 'timeout', str(exc)
            scores = metrics = None
            failure_kind = 'timeout'
        except Exception as exc:
            self.logger.exception('execution.failed', exc, component='runner', run_id=run_id,
                                  phase=phase, artifact_dir=str(artifacts))
            error_type = type(exc).__name__
            error = f'{type(exc).__name__}: {exc}'
            scores = metrics = None
            failure_kind = ('infrastructure' if phase in ('environment', 'data')
                            or isinstance(exc, OSError) else 'candidate')
        result = RunResult(status, str(checkpoint), str(artifacts), metrics, scores,
                           time.monotonic() - started, error, failure_kind)
        report = {**asdict(result), 'context': context, 'split': split, 'training': train,
                  'environment': environment.metadata if environment else None,
                  'overrides': overrides or {}, 'checkpoint_exists': checkpoint.is_file(),
                  'checkpoint_sha256': hashlib.sha256(checkpoint.read_bytes()).hexdigest()
                      if checkpoint.is_file() else None}
        try:
            (artifacts / 'result.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        except Exception as exc:
            self.logger.exception('run.report_exception', exc, component='runner', run_id=run_id)
            self.logger.emit('run.report_failed', component='runner', run_id=run_id, level='error',
                             artifact_dir=str(artifacts), error_type=type(exc).__name__)
            raise
        self.logger.emit('run.finished', component='runner', run_id=run_id,
                         level='info' if status == 'success' else 'error', status=status,
                         elapsed_s=result.elapsed_s, error_type=error_type,
                         checkpoint_path=str(checkpoint), checkpoint_exists=report['checkpoint_exists'],
                         artifact_dir=str(artifacts), scores=scores)
        return result

    def _worker(self, mode, workspace, request, checkpoint, artifacts, deadline, environment):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('candidate wall-clock budget exhausted')
        env = clean_environment()
        env['VIRTUAL_ENV'] = str(Path(environment.python).parent.parent)
        env['PATH'] = str(Path(environment.python).parent) + os.pathsep + env.get('PATH', '')
        command = [environment.python, '-I', '-B', '-u', str(Path(__file__).with_name('worker.py')), mode,
                   str(workspace), str(request), str(checkpoint), str(artifacts / 'predictions.json')]
        self.logger.emit('worker.started', component='runner', run_id=Path(artifacts).name, mode=mode, command=command,
                         timeout_s=remaining, artifact_dir=str(artifacts))
        with (artifacts / (mode + '.stdout.log')).open('wb') as stdout, \
                (artifacts / (mode + '.stderr.log')).open('wb') as stderr:
            subprocess.run(command, cwd=workspace, env=env, stdout=stdout, stderr=stderr,
                           timeout=remaining, check=True)
        self.logger.emit('worker.finished', component='runner', run_id=Path(artifacts).name, mode=mode, returncode=0,
                         artifact_dir=str(artifacts))
        self.environments.verify(environment, artifacts, deadline)


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', default='workspace_template')
    parser.add_argument('--data-dir', required=True)
    parser.add_argument('--checkpoint', help='Explicit resume/inference file; omitted means fresh training')
    parser.add_argument('--config', default='{}', help='JSON hyperparameter overrides')
    parser.add_argument('--timeout', type=float, default=3600)
    parser.add_argument('--split', choices=('valid', 'test'), default='valid')
    parser.add_argument('--inference-only', action='store_true')
    parser.add_argument('--environment-dir', default='storage/environments')
    parser.add_argument('--wheelhouse', help='Offline directory of wheels; disables the package index')
    parser.add_argument('--log-path', default='storage/run_log.jsonl')
    args = parser.parse_args()
    if args.inference_only and not args.checkpoint:
        parser.error('--inference-only requires --checkpoint')
    result = Runner(environment_dir=args.environment_dir, wheelhouse=args.wheelhouse,
                    log_path=args.log_path).run(args.workspace, data_dir=args.data_dir,
        checkpoint_path=args.checkpoint, overrides=json.loads(args.config),
        timeout_s=args.timeout, split=args.split, train=not args.inference_only)
    print(json.dumps(asdict(result), indent=2))
    return 0 if result.status == 'success' else 1


if __name__ == '__main__':
    raise SystemExit(main())
