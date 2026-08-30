"""Build model inputs from dataset rows (editable pipeline module).

Responsibilities:
- Extract features, compute item/user statistics, and fit categorical encoders.
- Fit preprocessing on training data only; reuse it for validation and inference.
- Return serializable fitted preprocessing state for train.py to include inside
  the single checkpoint file; do not write separate encoder or statistics files.

Constraints:
- Preserve input row order and handle missing values and unseen users/items.
- Never use a row's target or post-outcome signals as prediction input features.
- Prevent target leakage in training statistics, using out-of-fold or strictly
  prior history when aggregating labels or user behavior.
- Do not redefine dataset splits, target definitions, or evaluation metrics.

Function signatures and serialization interfaces await the runner contract.
"""
