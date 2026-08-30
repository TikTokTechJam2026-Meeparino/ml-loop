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

Input rows are (date, user_id, video_id, author_id, tab, duration_ms),
optionally followed by long_view during training. Only the first six are read.

The specifications above are authoritative. The implementation below is
replaceable reference FM preprocessing, not a mandatory feature set or encoding.
Coordinate changes to fit/transform and fitted state with train.py and model.py
while preserving the input-row contract and leakage constraints.
"""

# Reference implementation: replaceable while preserving the contracts above.
import numpy as np


def raw(row, edges):
    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]


def fit(rows):
    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
    vocabs = [{} for _ in range(5)]
    for row in rows:
        for i, value in enumerate(raw(row, edges)):
            if value not in vocabs[i]:
                vocabs[i][value] = len(vocabs[i])
    dims = [len(v) + 1 for v in vocabs]
    return dict(edges=edges, vocabs=vocabs,
                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))


def transform(rows, state):
    result = np.empty((len(rows), 5), dtype=np.int32)
    for n, row in enumerate(rows):
        for i, value in enumerate(raw(row, state['edges'])):
            vocab = state['vocabs'][i]
            result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
    return result
