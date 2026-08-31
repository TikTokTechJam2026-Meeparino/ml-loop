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


def FM_predict_with(model, weights, X):
    V0, W0, b0 = model.V, model.W, model.b
    try:
        model.V, model.W, model.b = weights['V'], weights['W'], weights['b']
        return model.predict(X)
    finally:
        model.V, model.W, model.b = V0, W0, b0


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
    n_members = config['members']
    rngs = [np.random.default_rng([config['seed'], m]) for m in range(n_members)]
    if Path(checkpoint_path).exists():
        payload = read_checkpoint(checkpoint_path)
        if payload['config'] != config or payload['context'] != context:
            raise ValueError('checkpoint incompatible with config, source, data, protocol, or environment')
        Predictor(payload)  # Validate inference weights before resuming.
        features = payload['features_state']
        state = payload['training_state']
        if len(state['latest']) != n_members:
            raise ValueError('incomplete optimizer/model state')
        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + m)
                  for m in range(n_members)]
        for m, model in enumerate(models):
            entry = state['latest'][m]
            if set(entry) != set(vars(model)):
                raise ValueError('incomplete optimizer/model state')
            for key, value in entry.items():
                if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
                    raise ValueError('incompatible or nonfinite latest state: ' + key)
                setattr(model, key, value)
        for m, r in enumerate(rngs):
            r.bit_generator.state = state['rng'][m]
        best_list, bad_list, epoch = state['best'], state['bad'], state['epoch']
        if len(best_list) != n_members or len(bad_list) != n_members:
            raise ValueError('invalid checkpoint training progress/settings')
        for m, model in enumerate(models):
            best, bad = best_list[m], bad_list[m]
            if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
                    or type(bad) is not int or not 0 <= bad <= config['patience']
                    or not np.isfinite(best) or not 0 <= best <= 1
                    or model.lr != config['lr'] or model.l2 != config['l2']
                    or type(model.t) is not int or model.t < 1):
                raise ValueError('invalid checkpoint training progress/settings')
        best_weights = payload.get('model_state', {}).get('members') if 'model_state' in payload else None
        best = list(best_list)
        bad = list(bad_list)
        print(f'resume: completed epoch={epoch}', flush=True)
    else:
        features = fit(train_rows)
        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + m)
                  for m in range(n_members)]
        best = [-1.0] * n_members
        bad = [0] * n_members
        epoch = 0
        payload = dict(version=1, config=config, features_state=features, context=context)
        best_weights = None
        print('fresh training', flush=True)
    if best_weights is None:
        best_weights = [None] * n_members
    else:
        best_weights = [copy.deepcopy(w) for w in best_weights]
    Xtr = transform(train_rows, features)
    ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
    Xva = transform(valid_rows, features)

    user_pos = {}
    user_neg = {}
    for i, row in enumerate(train_rows):
        uid = row[1]
        if ytr[i] == 1:
            user_pos.setdefault(uid, []).append(i)
        else:
            user_neg.setdefault(uid, []).append(i)
    eligible_users = [u for u in user_pos if u in user_neg and len(user_neg[u]) > 0]
    pos_idx_list = []
    map_start = []
    map_count = []
    neg_flat_list = []
    offset = 0
    for u in eligible_users:
        negs = user_neg[u]
        neg_flat_list.extend(negs)
        for p in user_pos[u]:
            pos_idx_list.append(p)
            map_start.append(offset)
            map_count.append(len(negs))
        offset += len(negs)
    pos_idx = np.asarray(pos_idx_list, dtype=np.int64)
    neg_start = np.asarray(map_start, dtype=np.int64)
    neg_count = np.asarray(map_count, dtype=np.int64)
    neg_flat = np.asarray(neg_flat_list, dtype=np.int64)

    best_epoch = payload.get('best_epoch', 0)
    valid_uids = [r[1] for r in valid_rows]
    valid_y = [r[6] for r in valid_rows]

    for epoch in range(epoch + 1, config['epochs'] + 1):
        if all(b >= config['patience'] for b in bad):
            break
        log_parts = []
        for m in range(n_members):
            if bad[m] >= config['patience']:
                continue
            model = models[m]
            r = rngs[m]
            if len(pos_idx) > 0:
                M = config['negs']
                rel = np.minimum((r.random((len(pos_idx), M)) * neg_count[:, None]).astype(np.int64),
                                  (neg_count - 1)[:, None])
                neg_choice = neg_flat[neg_start[:, None] + rel]
                order = r.permutation(len(pos_idx))
                pos_ord = pos_idx[order]
                neg_ord = neg_choice[order]
                losses = []
                for i in range(0, len(pos_ord), config['bs']):
                    loss = model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]],
                                            config['tau'])
                    losses.append(loss)
                    model.update_ema(config['ema'])
            else:
                order = r.permutation(len(ytr))
                losses = []
                for i in range(0, len(order), config['bs']):
                    loss = model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
                    losses.append(loss)
                    model.update_ema(config['ema'])
            validation_raw = evaluate(valid_uids, valid_y, model.predict(Xva))
            validation_ema = evaluate(valid_uids, valid_y, model.predict_ema(Xva, config['ema']))
            if validation_ema['primary'] > validation_raw['primary']:
                validation, variant = validation_ema, 'ema'
            else:
                validation, variant = validation_raw, 'raw'
            if validation['primary'] > best[m] + 1e-5:
                best[m], bad[m] = validation['primary'], 0
                if variant == 'ema':
                    best_weights[m] = copy.deepcopy(model.ema_weights(config['ema']))
                else:
                    best_weights[m] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
                best_epoch = epoch
            else:
                bad[m] += 1
            if not all(np.isfinite(getattr(model, key)).all()
                       for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'eV', 'eW', 'eb')):
                raise ValueError('nonfinite training state; keeping last valid checkpoint')
            log_parts.append(f'member={m} loss={np.mean(losses):.6f} primary_raw={validation_raw["primary"]:.6f} '
                              f'primary_ema={validation_ema["primary"]:.6f} selected={variant}')

        current_weights = [best_weights[m] if best_weights[m] is not None
                            else {key: copy.deepcopy(getattr(models[m], key)) for key in ('V', 'W', 'b')}
                            for m in range(n_members)]
        ensemble_scores = np.mean([FM_predict_with(models[m], current_weights[m], Xva) for m in range(n_members)],
                                   axis=0)
        ensemble_validation = evaluate(valid_uids, valid_y, ensemble_scores)

        payload['model_state'] = {'members': [copy.deepcopy(w) for w in current_weights]}
        payload['best_epoch'] = best_epoch
        payload['validation'] = ensemble_validation
        payload['training_state'] = dict(epoch=epoch, best=list(best), bad=list(bad),
            rng=[r.bit_generator.state for r in rngs],
            latest=[copy.deepcopy(vars(m)) for m in models])
        save_checkpoint(checkpoint_path, payload)
        print(f'epoch={epoch} ' + ' | '.join(log_parts) +
              f' | ensemble_primary={ensemble_validation["primary"]:.6f} checkpoint saved', flush=True)
