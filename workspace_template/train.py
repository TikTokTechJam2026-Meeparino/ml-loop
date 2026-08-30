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

CLI arguments and function signatures await the runner contract.
"""
