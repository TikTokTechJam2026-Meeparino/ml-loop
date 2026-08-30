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
  before training. Fail clearly on corrupt or incompatible files; do not
  silently ignore or overwrite them. Do not search other paths for checkpoints.
- Save the selected model, fitted preprocessing state, and effective config
  needed to reproduce inference together in that single checkpoint file.
- Keep any resumable training state consistent with its corresponding weights;
  if latest and best states differ, store both within the same checkpoint file.

Constraints:
- Fit model parameters on training data only; never tune against test scores.
- Do not modify the fixed splits, target definition, or evaluation rules.
- The supplied checkpoint file is the ONLY file execution may create or modify.
  Do not write logs, predictions, sidecars, temporary files, caches, or additional
  checkpoints; do not create directories. The caller prepares the parent folder.
- Apply this write restriction to imported modules and ML libraries as well:
  disable filesystem caches, Python bytecode writes, and automatic log writers.
- Send diagnostics to stdout/stderr; the runner owns any log persistence.
- Surface failures to the runner; do not fabricate metrics or hide exceptions.
- Training logs are diagnostic; the runner independently verifies final scores.
- Importing this module must not start training; use a main guard for execution.

CLI arguments and function signatures await the runner contract.
"""
