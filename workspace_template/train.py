"""Train and save a candidate model (editable pipeline module).

Responsibilities:
- Coordinate feature fitting, model construction, optimization, and loss.
- Use config.py for hyperparameters and seed stochastic components explicitly.
- Use the fixed validation evaluator for checkpoint selection or early stopping.
- Require an explicit checkpoint file path from the caller; do not infer one.
- Check that path before training: initialize a new model if the file is absent;
  otherwise load compatible saved weights or resume the saved training state.
- For full resume, restore optimizer/scheduler state, progress, random state,
  and best-validation tracking when present. Weights-only loading is a warm
  start, not an exact resume; report the selected mode through stdout/stderr.
- Validate checkpoint compatibility with the model, preprocessing, and config
  and runner-supplied dependency environment before training. Fail clearly on
  corrupt or incompatible files; do not
  silently ignore or overwrite them. Do not search other paths for checkpoints.
- Save the selected model, fitted preprocessing state, and effective config
  needed to reproduce inference together in that single checkpoint file.
- Keep any resumable training state consistent with its corresponding weights;
  if latest and best states differ, store both within the same checkpoint file.
- Every successful run must produce a self-contained inference artifact,
  whether training started fresh, warm-started, or resumed.
- The runner should supply a fresh path for a new candidate by default. Parent
  weights are an intentional warm start, recorded in checkpoint metadata;
  exact resumption is for continuing the same candidate and training settings.
- Save a single checkpoint dictionary (for example, with torch.save) containing
  config, features_state, model_state, and any state needed to resume training.
  Use a format appropriate to the model and shared with load_predictor.

Constraints:
- Fit model parameters on training data only; never tune against test scores.
- Do not modify the fixed splits, target definition, or evaluation rules.
- The supplied path identifies the final self-contained checkpoint file, not a
  directory. Temporary files needed for safe checkpoint saving are permitted.
- Save periodically: write a complete payload to a uniquely named temporary
  file in the checkpoint's directory, flush and close it, then atomically replace
  the destination. Never truncate the last valid checkpoint before the new
  payload is complete. Clean up owned temporary files on failure when possible.
- Atomic replacement protects against ordinary process interruption during
  saving; it does not guarantee durability across every storage or power failure.
  Resume from the last completed save; work since that save may be lost.
- The runner prepares the checkpoint's parent directory. Keep checkpoint writes
  within it and do not modify source files, datasets, or unrelated artifacts.
- Avoid unrelated file outputs and disable unnecessary library caches, Python
  bytecode writes, and automatic log writers. Inference remains read-only.
- Send diagnostics to stdout/stderr; the runner owns any log persistence.
- Surface failures to the runner; do not fabricate metrics or hide exceptions.
- Training logs are diagnostic; the runner independently verifies final scores.
- Importing this module must not start training; use a main guard for execution.

Runner worker calls train(train_rows, valid_rows, checkpoint_path, overrides,
context). Preserve this entry-point signature.

The specifications above are authoritative. The implementation below is a
replaceable reference FM training loop, not a required optimizer, loss, or
checkpoint format. Coordinate replacements with model.py and preserve the
runner contract. This reference supports fresh training and exact recovery at
completed epoch boundaries, not mid-batch recovery or parent warm starts.
"""

# Reference implementation: replaceable while preserving the contracts above.
import copy
import os
from pathlib import Path
import pickle
import tempfile

import numpy as np

from agent.sandbox.protocol import evaluate
from config import resolve
from features import fit, transform
from model import FM, Predictor, read_checkpoint


def save_checkpoint(path, payload):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=Path(path).parent, prefix='.checkpoint-', delete=False) as stream:
            temporary = stream.name
            pickle.dump(payload, stream, protocol=pickle.HIGHEST_PROTOCOL)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def train(train_rows, valid_rows, checkpoint_path, overrides, context):
    config = resolve(overrides)
    rng = np.random.default_rng(config['seed'])
    if Path(checkpoint_path).exists():
        payload = read_checkpoint(checkpoint_path)
        if payload['config'] != config or payload['context'] != context:
            raise ValueError('checkpoint incompatible with config, source, data, protocol, or environment')
        Predictor(payload)  # Validate inference weights before resuming.
        features = payload['features_state']
        state = payload['training_state']
        rng.bit_generator.state = state['rng']
        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
        if set(state['latest']) != set(vars(model)):
            raise ValueError('incomplete optimizer/model state')
        for key, value in state['latest'].items():
            if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
                raise ValueError('incompatible or nonfinite latest state: ' + key)
            setattr(model, key, value)
        best, bad, epoch = state['best'], state['bad'], state['epoch']
        if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
                or type(bad) is not int or not 0 <= bad <= config['patience']
                or not np.isfinite(best) or not 0 <= best <= 1
                or model.lr != config['lr'] or model.l2 != config['l2']
                or type(model.t) is not int or model.t < 1):
            raise ValueError('invalid checkpoint training progress/settings')
        print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
    else:
        features = fit(train_rows)
        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
        best, bad, epoch = -1.0, 0, 0
        payload = dict(version=1, config=config, features_state=features, context=context)
        print('fresh training', flush=True)
    Xtr = transform(train_rows, features)
    ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
    Xva = transform(valid_rows, features)
    for epoch in range(epoch + 1, config['epochs'] + 1):
        if bad >= config['patience']:
            break
        order = rng.permutation(len(ytr))
        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
                  for i in range(0, len(order), config['bs'])]
        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
        if validation['primary'] > best + 1e-5:
            best, bad = validation['primary'], 0
            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
            payload['best_epoch'] = epoch
        else:
            bad += 1
        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
            raise ValueError('nonfinite training state; keeping last valid checkpoint')
        payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
            rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
        payload['validation'] = validation
        save_checkpoint(checkpoint_path, payload)
        print(f'epoch={epoch} loss={np.mean(losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
