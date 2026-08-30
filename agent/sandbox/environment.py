"""Provision trusted candidate dependencies, separately from the agent environment.

requirements.txt is a flat version lock: every runtime dependency must be pinned.
Binary wheels only; no implicit dependency resolution or source build execution.
Environments must not be modified by candidates. This is not a security sandbox.
"""
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

from agent.log import RunLogger


IDENTITY = """import json, platform, sys, sysconfig
print(json.dumps(dict(version=sys.version, implementation=sys.implementation.name,
    cache_tag=sys.implementation.cache_tag, platform=sysconfig.get_platform(),
    machine=platform.machine(), soabi=sysconfig.get_config_var('SOABI'))))
"""
PACKAGES = """import importlib.metadata, json, re
print(json.dumps(dict(sorted((re.sub(r'[-_.]+', '-', d.metadata['Name']).lower(),
    d.version) for d in importlib.metadata.distributions()))))
"""


def clean_environment():
    # Do not leak the agent's import path, activation, or pip configuration into
    # the candidate. -I also disables user site packages and PYTHON* settings.
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(('PYTHON', 'PIP_')) and k.upper() != 'VIRTUAL_ENV'}
    return {**env, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUNBUFFERED': '1'}


def pinned_requirements(text):
    pins = {}
    for line in text.splitlines():
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*==[A-Za-z0-9][A-Za-z0-9.!+_-]*', line):
            raise ValueError('requirements.txt must contain only exact name==version pins')
        name, version = line.split('==')
        name = re.sub(r'[-_.]+', '-', name).lower()
        if name in pins:
            raise ValueError('duplicate requirement: ' + name)
        pins[name] = version
    return pins


@dataclass(frozen=True)
class CandidateEnvironment:
    python: str
    metadata: dict


class EnvironmentManager:
    def __init__(self, cache_dir='storage/environments', python=None, wheelhouse=None, logger=None):
        self.cache_dir = Path(cache_dir).resolve()
        self.python = str(Path(python or sys.executable).resolve())
        # Optional offline wheel source. Without it pip uses its default index.
        self.wheelhouse = Path(wheelhouse).resolve() if wheelhouse else None
        self.logger = logger if logger is not None else RunLogger()

    def _run(self, command, artifacts, deadline):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('candidate budget exhausted during environment preparation')
        self.logger.emit('command.started', component='environment', run_id=Path(artifacts).name, command=command,
                         timeout_s=remaining, artifact_dir=str(artifacts))
        with (artifacts / 'environment.stderr.log').open('ab') as stderr:
            try:
                result = subprocess.run(command, env=clean_environment(), cwd=artifacts,
                    stdout=subprocess.PIPE, stderr=stderr, timeout=remaining, check=True)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
                self.logger.exception('command.failed', exc, component='environment', run_id=Path(artifacts).name, artifact_dir=str(artifacts))
                with (artifacts / 'environment.stdout.log').open('ab') as stdout:
                    stdout.write(exc.stdout or b'')
                raise
        with (artifacts / 'environment.stdout.log').open('ab') as stdout:
            stdout.write(result.stdout)
        self.logger.emit('command.finished', component='environment', run_id=Path(artifacts).name, returncode=result.returncode,
                         artifact_dir=str(artifacts))
        return result.stdout.decode('utf-8')

    def prepare(self, workspace, artifacts, deadline, run_id=None):
        workspace, artifacts = Path(workspace).resolve(), Path(artifacts).resolve()
        if self.cache_dir == workspace or workspace in self.cache_dir.parents:
            raise ValueError('environment cache must live outside candidate workspace')
        requirements = (workspace / 'requirements.txt').read_text(encoding='utf-8')
        pins = pinned_requirements(requirements)
        (artifacts / 'requirements.txt').write_text(requirements, encoding='utf-8')
        identity = json.loads(self._run([self.python, '-I', '-c', IDENTITY], artifacts, deadline))
        key_input = dict(format=1, requirements=requirements, runtime=identity,
                         policy='pinned-wheels-no-deps-v1')
        key = hashlib.sha256(json.dumps(key_input, sort_keys=True).encode()).hexdigest()
        directory = self.cache_dir / key
        python = directory / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        manifest = directory / 'environment.json'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if directory.exists():
            if not manifest.is_file():
                raise RuntimeError(f'environment is incomplete or being created: {directory}')
            metadata = json.loads(manifest.read_text(encoding='utf-8'))
            if metadata.get('key') != key or metadata.get('specification') != key_input:
                raise ValueError('cached environment manifest is incompatible')
            self.verify(CandidateEnvironment(str(python), metadata), artifacts, deadline)
            self.logger.emit('environment.reused', component='environment', run_id=run_id,
                             environment_key=key, directory=str(directory))
        else:
            directory.mkdir()  # Exclusive creation; no concurrent installation into a cache entry.
            self.logger.emit('environment.creating', component='environment', run_id=run_id,
                             environment_key=key, directory=str(directory))
            try:
                self._run([self.python, '-I', '-m', 'venv', str(directory)], artifacts, deadline)
                lock = directory / 'requirements.txt'
                lock.write_text(requirements, encoding='utf-8')
                if pins:
                    command = [str(python), '-I', '-m', 'pip', '--isolated', '--disable-pip-version-check',
                               'install', '--no-input', '--no-deps', '--only-binary=:all:',
                               '--no-cache-dir', '-r', str(lock)]
                    if self.wheelhouse:
                        command.extend(['--no-index', '--find-links', str(self.wheelhouse)])
                    self._run(command, artifacts, deadline)
                self._run([str(python), '-I', '-m', 'pip', '--isolated', 'check'], artifacts, deadline)
                packages = json.loads(self._run([str(python), '-I', '-c', PACKAGES], artifacts, deadline))
                if any(packages.get(name) != version for name, version in pins.items()):
                    raise ValueError('installed packages differ from the exact dependency pins')
                metadata = dict(key=key, specification=key_input, packages=packages)
                # Written last: a partial environment is never eligible for reuse.
                temporary = directory / 'environment.json.tmp'
                temporary.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
                temporary.replace(manifest)
            except BaseException as original:
                self.logger.emit('environment.failed', component='environment', run_id=run_id,
                                 level='error', environment_key=key, error_type=type(original).__name__,
                                 artifact_dir=str(artifacts))
                # Delete only this invocation's owned, exact cache entry, never
                # an existing environment or a broad/user-selected directory.
                try:
                    if directory.resolve().parent != self.cache_dir or directory.is_symlink():
                        raise ValueError('cleanup target is not the owned cache entry')
                    shutil.rmtree(directory)
                except Exception as cleanup_error:
                    self.logger.emit('environment.cleanup_failed', component='environment', run_id=run_id,
                                     level='warning', directory=str(directory), environment_key=key,
                                     original_error_type=type(original).__name__,
                                     cleanup_error_type=type(cleanup_error).__name__,
                                     errno=getattr(cleanup_error, 'errno', None))
                raise
            self.logger.emit('environment.created', component='environment', run_id=run_id,
                             environment_key=key, directory=str(directory))
        environment = CandidateEnvironment(str(python), metadata)
        (artifacts / 'environment.json').write_text(
            json.dumps(dict(python=str(python), **metadata), indent=2), encoding='utf-8')
        return environment

    def verify(self, environment, artifacts, deadline):
        identity = json.loads(self._run([environment.python, '-I', '-c', IDENTITY], artifacts, deadline))
        packages = json.loads(self._run([environment.python, '-I', '-c', PACKAGES], artifacts, deadline))
        if (identity != environment.metadata['specification']['runtime']
                or packages != environment.metadata['packages']):
            raise ValueError('cached environment changed; refusing execution/recovery')
