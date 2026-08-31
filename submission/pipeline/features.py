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
import bisect
import math
from collections import defaultdict

import numpy as np


def _bucket(c, cap):
    if c <= 0:
        return 0
    return min(int(math.log2(c)) + 1, cap)


def _build_table(rows, keyfunc, dates):
    groups = defaultdict(list)
    for row in rows:
        code = bisect.bisect_left(dates, row[0])
        groups[keyfunc(row)].append(code)
    codes_parts = []
    index = {}
    offset = 0
    for key, values in groups.items():
        values.sort()
        codes_parts.append(np.asarray(values, dtype=np.int32))
        index[key] = (offset, offset + len(values))
        offset += len(values)
    codes = np.concatenate(codes_parts) if codes_parts else np.empty(0, dtype=np.int32)
    return dict(codes=codes, index=index)


def _lookup(table, key, code):
    se = table['index'].get(key)
    if se is None:
        return 0
    start, end = se
    sub = table['codes'][start:end]
    return int(np.searchsorted(sub, code))


def raw(row, state):
    code = bisect.bisect_left(state['dates'], row[0])
    c_ua = _lookup(state['ua'], (row[1], row[3]), code)
    c_vid = _lookup(state['vid'], row[2], code)
    c_aut = _lookup(state['aut'], row[3], code)
    bin_idx = str(int(np.searchsorted(state['edges'], row[5])))
    return [row[1], row[2], row[3], row[4], bin_idx,
            'ua' + str(_bucket(c_ua, 6)),
            'vp' + str(_bucket(c_vid, 8)),
            'ap' + str(_bucket(c_aut, 8))]


def fit(rows):
    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
    dates = sorted(set(r[0] for r in rows))
    ua = _build_table(rows, lambda r: (r[1], r[3]), dates)
    vid = _build_table(rows, lambda r: r[2], dates)
    aut = _build_table(rows, lambda r: r[3], dates)

    partial_state = dict(edges=edges, dates=dates, ua=ua, vid=vid, aut=aut)

    vocabs = [{} for _ in range(8)]
    for row in rows:
        for i, value in enumerate(raw(row, partial_state)):
            if value not in vocabs[i]:
                vocabs[i][value] = len(vocabs[i])
    dims = [len(v) + 1 for v in vocabs]
    offsets = np.cumsum([0] + dims[:-1]).astype(np.int32)
    return dict(edges=edges, dates=dates, ua=ua, vid=vid, aut=aut,
                vocabs=vocabs, offsets=offsets, dim=sum(dims))


def transform(rows, state):
    result = np.empty((len(rows), 8), dtype=np.int32)
    for n, row in enumerate(rows):
        for i, value in enumerate(raw(row, state)):
            vocab = state['vocabs'][i]
            result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
    return result
