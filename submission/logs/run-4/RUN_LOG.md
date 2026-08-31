# Run log: run-4

Run id `6ccd59117c574288924889af24d3f65e` · evaluation protocol `cfe7881824a34480…` · schema 1

## Summary

| | |
|---|---|
| Candidate iterations | 19 of 50 permitted |
| Candidate outcomes | 19 success |
| Stop reason | `candidate_time_budget` |
| Baseline (`genesis`) | Primary 0.601469 |
| Selected (`node_019`) | Primary 0.603619 |
| Validation gain | +0.002150 |
| **Held-out test** | GAUC 0.664158 · nDCG@5 0.530261 · **Primary 0.597210** |
| Test coverage | 23,875 users · 170,588 rows |
| Model calls | 45 |
| Provider-reported tokens | 1,075,447 |
| Agent wall clock | 86.8 min |
| GPU hours | 0 (CPU only) |

## Manual interventions

**0** operator intervention(s) during this run.

Interventions are counted from the run's own event log: a provider or infrastructure failure pauses the run and records `run.failed`, and further orchestrator activity in the same log means an operator resumed it. Every intervention above is a resume of an unmodified run.

No manual edits were made to candidate code: every commit in the candidate workspace is authored by the agent identity (ML Loop <ml-loop@localhost>). Hypotheses, diffs, parent selection, and stopping were produced by the agent without human editing.

### Provider transport failures (4)

| Time (UTC) | Error | HTTP | Candidate | Attempt |
|---|---|---|---|---|
| 21:35:01 | `Timeout` | 408 | node_007 | 1 |
| 22:16:26 | `Timeout` | 408 | node_016 | 1 |
| 22:19:27 | `Timeout` | 408 | node_016 | 2 |
| 22:32:29 | `Timeout` | 408 | node_018 | 1 |

Transport failures are retried inside the client and do not count as experimental evidence. Only an exhausted retry budget pauses the run.

## Iteration index

| # | Candidate | GAUC | nDCG@5 | Primary | vs parent | Status | Repairs |
|---|---|---|---|---|---|---|---|
| baseline | `genesis` | 0.667133 | 0.535805 | 0.601469 | - | success | 0 |
| 1 | `node_001` | 0.665899 | 0.535813 | 0.600856 | -0.000612 | success | 0 |
| 2 | `node_002` | 0.668212 | 0.535527 | 0.601870 | +0.000401 | success | 0 |
| 3 | `node_003` | 0.667327 | 0.535196 | 0.601262 | -0.000608 | success | 0 |
| 4 | `node_004` | 0.668808 | 0.535755 | 0.602282 | +0.000412 | success | 0 |
| 5 | `node_005` | 0.667393 | 0.536149 | 0.601771 | -0.000511 | success | 0 |
| 6 | `node_006` | 0.667237 | 0.534521 | 0.600879 | -0.001402 | success | 0 |
| 7 | `node_007` | 0.667989 | 0.535506 | 0.601747 | -0.000534 | success | 0 |
| 8 | `node_008` | 0.668970 | 0.535930 | 0.602450 | +0.000169 | success | 0 |
| 9 | `node_009` | 0.668778 | 0.535731 | 0.602255 | -0.000196 | success | 0 |
| 10 | `node_010` | 0.633432 | 0.522731 | 0.578081 | -0.024369 | success | 0 |
| 11 | `node_011` | 0.660966 | 0.533436 | 0.597201 | -0.005249 | success | 0 |
| 12 | `node_012` | 0.669326 | 0.536702 | 0.603014 | +0.000564 | success | 0 |
| 13 | `node_013` | 0.669510 | 0.537000 | 0.603255 | +0.000241 | success | 0 |
| 14 | `node_014` | 0.668908 | 0.536566 | 0.602737 | -0.000518 | success | 0 |
| 15 | `node_015` | 0.670143 | 0.537091 | 0.603617 | +0.000363 | success | 0 |
| 16 | `node_016` | 0.670004 | 0.536951 | 0.603477 | -0.000140 | success | 0 |
| 17 | `node_017` | 0.668797 | 0.535873 | 0.602335 | -0.001283 | success | 0 |
| 18 | `node_018` | 0.669431 | 0.536873 | 0.603152 | -0.000465 | success | 0 |
| 19 | `node_019` | 0.670251 | 0.536986 | 0.603619 | +0.000001 | success | 0 |

---

## Baseline: `genesis`

**Status** `success` · **Parent** `none` · **Commit** `c7109a0d4325`

### Hypothesis

Supplied reference pipeline. No agent hypothesis; this is the baseline every candidate is measured against.

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667133 | 0.535805 | 0.601469 | - | 41 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py        |  39 +++++++++++++++
 features.py      |  51 ++++++++++++++++++++
 model.py         | 121 ++++++++++++++++++++++++++++++++++++++++++++++
 requirements.txt |   7 +++
 train.py         | 144 +++++++++++++++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 362 insertions(+)
```

Baseline pipeline as supplied; no parent to diff against.

---

## Iteration 1: `node_001`

**Status** `success` · **Parent** `genesis` · **Commit** `7bd02de7e819`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem, untouched so far: the genesis pipeline feeds the FM only 5 raw categorical fields — user_id, video_id, author_id, tab, and a coarse 10-bin duration quantile). Hypothesis: because GAUC and nDCG@5 are computed within per-user groups, only signals that vary across a user's candidate items can improve the score; adding label-free item/author popularity statistics, a finer duration resolution, and a tab×duration cross should give the FM much sharper within-user discrimination than user/video ID embeddings alone. This is distinct from the only supplied related memory item (a minimum-occurrence vocabulary threshold that pruned rare IDs, which regressed); here nothing is pruned and no label-derived statistic is used, so there is no leakage risk. No sibling experiments were supplied.

Implementation (edit features.py, plus the minimal coordination needed in model.py/train.py if any hard-coded field count exists):

1. In features.py, make the feature-field list data-driven instead of the fixed 5 columns. `fit(rows)` must (a) compute duration quantile edges with 32 bins: `np.quantile([r[5] for r in rows], np.linspace(0, 1, 33)[1:-1])`; (b) build three plain-dict occurrence counters over the training rows only — `video_counts[row[2]]`, `author_counts[row[3]]`, `user_counts[row[1]]` — and store them in the returned state dict together with `edges`; (c) build vocabs/offsets/dim over the expanded field list exactly as today.

2. Change the row-encoding helper (currently `raw(row, edges)`) to take the full fitted state (so it can read counts and edges) and emit these 9 string fields, in this order:
   - user_id (row[1]), video_id (row[2]), author_id (row[3]), tab (row[4])
   - duration bin: `'d' + str(int(np.searchsorted(edges, row[5])))` using the 32-bin edges
   - video popularity bucket: `'v' + str(int(np.log2(1.0 + video_counts.get(row[2], 0))))`
   - author popularity bucket: `'a' + str(int(np.log2(1.0 + author_counts.get(row[3], 0))))`
   - user activity bucket: `'u' + str(int(np.log2(1.0 + user_counts.get(row[1], 0))))`
   - tab×duration cross: `str(row[4]) + '|' + str(int(np.searchsorted(edges, row[5])))`
   Unseen categories at transform time keep the existing fallback (index `len(vocab)` within that field's block), and rows unseen in training simply get count 0 for the popularity buckets.

3. Update `transform` to allocate `np.empty((len(rows), n_fields), dtype=np.int32)` with `n_fields = len(state['offsets'])` (i.e., 9) rather than the hard-coded 5, so the FM's `logits`/`step` (which already handle arbitrary field counts) work unchanged. Ensure the fitted state (edges, vocabs, offsets, dim, and the three count dicts) stays picklable so it round-trips inside the existing single checkpoint and is reused unchanged by `Predictor.predict`.

4. Leave config.py hyperparameters (k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0), the training loop, checkpoint format, splits, target, and evaluation untouched. Expected runtime roughly 1.8–2x the 41 s baseline (well inside candidate_timeout_s=1800).

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.665899 | 0.535813 | 0.600856 | -0.000612 | 54 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 42 +++++++++++++++++++++++++++++++++---------
 1 file changed, 33 insertions(+), 9 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..9bbe381 100644
--- a/features.py
+++ b/features.py
@@ -26,26 +26,50 @@ while preserving the input-row contract and leakage constraints.
 import numpy as np
 
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+def raw(row, state):
+    edges = state['edges']
+    video_counts = state['video_counts']
+    author_counts = state['author_counts']
+    user_counts = state['user_counts']
+    dbin = int(np.searchsorted(edges, row[5]))
+    return [
+        row[1], row[2], row[3], row[4],
+        'd' + str(dbin),
+        'v' + str(int(np.log2(1.0 + video_counts.get(row[2], 0)))),
+        'a' + str(int(np.log2(1.0 + author_counts.get(row[3], 0)))),
+        'u' + str(int(np.log2(1.0 + user_counts.get(row[1], 0)))),
+        str(row[4]) + '|' + str(dbin),
+    ]
 
 
 def fit(rows):
-    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 33)[1:-1])
+    video_counts = {}
+    author_counts = {}
+    user_counts = {}
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
+        video_counts[row[2]] = video_counts.get(row[2], 0) + 1
+        author_counts[row[3]] = author_counts.get(row[3], 0) + 1
+        user_counts[row[1]] = user_counts.get(row[1], 0) + 1
+    n_fields = 9
+    vocabs = [{} for _ in range(n_fields)]
+    state = dict(edges=edges, video_counts=video_counts, author_counts=author_counts,
+                 user_counts=user_counts, vocabs=vocabs)
+    for row in rows:
+        for i, value in enumerate(raw(row, state)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
-    return dict(edges=edges, vocabs=vocabs,
-                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
+    state['offsets'] = np.cumsum([0] + dims[:-1]).astype(np.int32)
+    state['dim'] = sum(dims)
+    return state
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 5), dtype=np.int32)
+    n_fields = len(state['offsets'])
+    result = np.empty((len(rows), n_fields), dtype=np.int32)
     for n, row in enumerate(rows):
-        for i, value in enumerate(raw(row, state['edges'])):
+        for i, value in enumerate(raw(row, state)):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
     return result
```

---

## Iteration 2: `node_002`

**Status** `success` · **Parent** `genesis` · **Commit** `720da1d89079`

### Hypothesis

```text
SELECTED CHANGE
Change the training objective from pointwise binary cross-entropy to a within-user pairwise BPR ranking loss, keeping the FM backbone and features exactly as they are. Hypothesis: GAUC and nDCG@5 are computed strictly inside per-user candidate groups, so a loss that directly optimizes the ordering of a user's own positive vs. negative impressions should improve within-group discrimination more than the current global pointwise likelihood, which spends capacity on cross-user calibration that the metrics ignore. This is a loss-formulation experiment; the only supplied sibling from this parent (node_001) changed feature engineering (popularity buckets, finer duration bins, tab×duration cross) and slightly regressed, and no loss-formulation attempt has been made from this parent (the BPR mentions in memory come from a different run's deep lineage on a heavily modified baseline, not from plain pointwise FM).

Implementation:

1. model.py — add a new method `FM.step_pair(Xp, Xn)` alongside (and without removing) the existing `step`, implementing one Adam update on the BPR loss `L = mean(-log sigmoid(z_pos - z_neg))`:
   - compute `zp, Ep, Sp = self.logits(Xp)` and `zn, En, Sn = self.logits(Xn)`, `d = zp - zn`;
   - per-pair coefficient `c = (-sigmoid(-d) / B).astype(np.float32)` where `B = len(d)`;
   - accumulate gradients into fresh `gV`/`gW` with `np.add.at(gW, Xp, c[:, None])`, `np.add.at(gW, Xn, -c[:, None])`, `np.add.at(gV, Xp, c[:, None, None] * (Sp[:, None, :] - Ep))`, `np.add.at(gV, Xn, -c[:, None, None] * (Sn[:, None, :] - En))`;
   - add `self.l2 * self.V` and `self.l2 * self.W`, then reuse the exact same Adam update block (b1=0.9, b2=0.999, eps=1e-8, `self.t += 1`, same moment buffers mV/vV/mW/vW) as `step`;
   - do not update `self.b` (the global bias cancels in the score difference); leave it at 0.0 so predictions and the checkpoint weight shapes stay unchanged;
   - return `float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))` as the reported training loss.
   Do not add any new instance attributes to FM, so `set(state['latest']) == set(vars(model))` in train.py's resume check still holds, and keep `logits`/`predict`/`Predictor`/`load_predictor` unchanged.

2. train.py — replace the per-epoch pointwise batching with pairwise sampling built once before the epoch loop, from training rows only:
   - group training-row indices by `r[1]` (user_id) into positive indices (`r[6] == 1`) and negative indices; keep only users that have at least one of each;
   - build flat NumPy arrays: `pos_idx` (all eligible positives concatenated), `pos_user` (the eligible-user slot for each entry of `pos_idx`), `neg_flat` (all eligible users' negative indices concatenated), plus `neg_start` and `neg_count` per eligible user;
   - each epoch, draw `n_pairs = len(train_rows)` pairs: `sel = rng.integers(0, len(pos_idx), n_pairs)`; `u = pos_user[sel]`; `off = (rng.random(n_pairs) * neg_count[u]).astype(np.int64)`; `neg = neg_flat[neg_start[u] + off]`; then iterate in mini-batches of `config['bs']` pairs calling `model.step_pair(Xtr[pos_idx[sel][i:i+bs]], Xtr[neg[i:i+bs]])` and average the returned losses for the epoch log;
   - keep everything else identical: same `transform` usage, same per-epoch `evaluate(...)` on validation with `model.predict(Xva)`, same best-primary early stopping (patience) and best-weight capture, same finiteness checks, same single-file atomic checkpoint payload (version, config, features_state, model_state with V/W/b, training_state with epoch/best/bad/rng/latest, context), same resume path.
   - raise a clear error if no eligible user pairs exist.

3. config.py — raise `epochs` from 40 to 60 in DEFAULTS (leave k=16, lr=0.001, l2=1e-6, bs=8192, patience=4, seed=0 unchanged) so the slower-converging ranking loss has headroom; early stopping still governs actual length. Expected runtime is roughly 2–3x the 41 s baseline, far inside candidate_timeout_s=1800.

features.py stays exactly as supplied (5 raw fields, 10-bin duration quantiles); splits, long_view target, ranking groups, and evaluation are untouched.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668212 | 0.535527 | 0.601870 | +0.000401 | 36 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  2 +-
 model.py  | 20 ++++++++++++++++++++
 train.py  | 39 +++++++++++++++++++++++++++++++++++----
 3 files changed, 56 insertions(+), 5 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 147c6ac..75fc434 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0)
 
 
 def resolve(overrides):
diff --git a/model.py b/model.py
index 495d48e..f754fa1 100644
--- a/model.py
+++ b/model.py
@@ -65,6 +65,26 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
+    def step_pair(self, Xp, Xn):
+        B = len(Xp)
+        zp, Ep, Sp = self.logits(Xp)
+        zn, En, Sn = self.logits(Xn)
+        d = zp - zn
+        c = (-sigmoid(-d) / B).astype(np.float32)
+        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        np.add.at(gW, Xp, c[:, None])
+        np.add.at(gW, Xn, -c[:, None])
+        np.add.at(gV, Xp, c[:, None, None] * (Sp[:, None, :] - Ep))
+        np.add.at(gV, Xn, -c[:, None, None] * (Sn[:, None, :] - En))
+        gV += self.l2 * self.V; gW += self.l2 * self.W
+        self.t += 1
+        b1, b2, eps = 0.9, 0.999, 1e-8
+        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M *= b1; M += (1 - b1) * G
+            Vv *= b2; Vv += (1 - b2) * (G * G)
+            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index 0451b1a..db7e313 100644
--- a/train.py
+++ b/train.py
@@ -120,14 +120,45 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
     Xtr = transform(train_rows, features)
-    ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
+
+    users = {}
+    for i, r in enumerate(train_rows):
+        users.setdefault(r[1], [[], []])[r[6] == 1].append(i)
+    # users[uid] = [neg_list, pos_list]
+    eligible = [(neg, pos) for neg, pos in users.values() if neg and pos]
+    if not eligible:
+        raise ValueError('no eligible users with both positive and negative impressions')
+
+    pos_idx_list = []
+    pos_user_list = []
+    neg_flat_list = []
+    neg_start = np.zeros(len(eligible), dtype=np.int64)
+    neg_count = np.zeros(len(eligible), dtype=np.int64)
+    offset = 0
+    for uidx, (neg, pos) in enumerate(eligible):
+        pos_idx_list.extend(pos)
+        pos_user_list.extend([uidx] * len(pos))
+        neg_start[uidx] = offset
+        neg_count[uidx] = len(neg)
+        neg_flat_list.extend(neg)
+        offset += len(neg)
+    pos_idx = np.asarray(pos_idx_list, dtype=np.int64)
+    pos_user = np.asarray(pos_user_list, dtype=np.int64)
+    neg_flat = np.asarray(neg_flat_list, dtype=np.int64)
+
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
-        order = rng.permutation(len(ytr))
-        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                  for i in range(0, len(order), config['bs'])]
+        n_pairs = len(train_rows)
+        sel = rng.integers(0, len(pos_idx), n_pairs)
+        u = pos_user[sel]
+        off = (rng.random(n_pairs) * neg_count[u]).astype(np.int64)
+        neg = neg_flat[neg_start[u] + off]
+        pos_sel = pos_idx[sel]
+        bs = config['bs']
+        losses = [model.step_pair(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])
+                  for i in range(0, n_pairs, bs)]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

---

## Iteration 3: `node_003`

**Status** `success` · **Parent** `node_002` · **Commit** `262e1b10349e`

### Hypothesis

```text
SELECTED CHANGE
Experiment: replace the plain FM interaction term with a Field-weighted FM (FwFM) backbone — i.e., learn a symmetric matrix of field-pair interaction weights on top of the existing pairwise-BPR training. Hypothesis: with only 5 fields (user_id, video_id, author_id, tab, duration-bin) the current FM sums all 10 field-pair dot products with equal weight, so noisy pairs (e.g. tab x duration-bin, author x duration-bin) dilute the informative user x video / user x author signals; letting the model learn one scalar weight per field pair is a strict generalization of the current FM (it reduces to it when all off-diagonal weights equal 1) and should sharpen within-user ranking at negligible compute cost. This is a model-backbone change; the only supplied prior attempts from this lineage were feature engineering (node_001, slight regression) and the loss switch to pairwise BPR (node_002, current parent); no backbone/architecture change has been attempted here.

Implementation (edit model.py, train.py, config.py only; keep features.py, splits, long_view target, ranking groups, and evaluation untouched):

1. model.py — FM:
   - `__init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, fields=5, lr_r=0.005)`: add `self.R` as a float32 (fields, fields) array initialized to 1.0 off-diagonal and 0.0 on the diagonal, plus Adam buffers `self.mR`, `self.vR` (zeros_like(R)), and `self.lr_r = float(lr_r)`. Keep all existing attributes/shapes for V, W, b, mV, vV, mW, vW, t.
   - `logits(X)`: `E = self.V[X]` (B,F,k); `M = np.einsum('fg,bgk->bfk', self.R, E)`; `inter = 0.5 * (E * M).sum((1, 2))`; return `self.b + self.W[X].sum(1) + inter, E, M` (the third returned value is now M, replacing S).
   - `step(X, y)`: unchanged except the embedding gradient scatter uses M in place of `(S[:, None, :] - E)`, i.e. `np.add.at(gV, X, g[:, None, None] * M)`, and additionally accumulate `gR = 0.5 * np.einsum('b,bfk,bgk->fg', g, E, E) + self.l2 * self.R`, zero its diagonal.
   - `step_pair(Xp, Xn)`: unchanged except use `Mp`/`Mn` in the two `np.add.at(gV, ...)` calls in place of `(Sp[:, None, :] - Ep)` and `(Sn[:, None, :] - En)`, and accumulate `gR = 0.5 * (np.einsum('b,bfk,bgk->fg', c, Ep, Ep) - np.einsum('b,bfk,bgk->fg', c, En, En)) + self.l2 * self.R`, zero its diagonal. Continue to leave `self.b` untouched in step_pair and return the same BPR loss value.
   - In both step methods, after the existing Adam loop over (V, W) with `self.lr`, apply the same Adam update (b1=0.9, b2=0.999, eps=1e-8, shared `self.t` bias correction) to `self.R` with `self.mR`, `self.vR` using learning rate `self.lr_r`, then force `np.fill_diagonal(self.R, 0.0)` so the diagonal stays exactly zero.
   - `Predictor.__init__`: restore weights for the tuple `('V', 'W', 'b', 'R')` (same shape/finiteness validation as now) and construct FM with the config's k/lr/l2/seed (lr_r may come from config or the default; it does not affect inference).

2. train.py: construct FM with `lr_r=config['lr_r']` in both the resume and fresh branches; include `'R'` in the `payload['model_state']` deep-copy key tuple; include `'R'`, `'mR'`, `'vR'` in the per-epoch finiteness check tuple. Leave the pairwise BPR sampling, early stopping, checkpoint payload/atomic-save, and resume logic exactly as they are (the `set(state['latest']) == set(vars(model))` check keeps working because latest is `vars(model)`).

3. config.py: add `lr_r=0.005` to DEFAULTS (keep k=16, lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0) and validate it alongside `lr` as a finite float strictly greater than 0.

Expected runtime is essentially unchanged (~40-60 s, far inside candidate_timeout_s=1800) since the added einsums operate on (B, 5, 16) tensors and a 5x5 weight matrix.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667327 | 0.535196 | 0.601262 | -0.000608 | 41 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 model.py  | 53 +++++++++++++++++++++++++++++++++++------------------
 train.py  | 10 ++++++----
 3 files changed, 44 insertions(+), 23 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 75fc434..fa93994 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0, lr_r=0.005)
 
 
 def resolve(overrides):
@@ -36,4 +36,6 @@ def resolve(overrides):
     for key in ('lr', 'l2'):
         if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
             raise ValueError(f'invalid {key}')
+    if not math.isfinite(config['lr_r']) or config['lr_r'] <= 0:
+        raise ValueError('invalid lr_r')
     return config
diff --git a/model.py b/model.py
index f754fa1..31638b6 100644
--- a/model.py
+++ b/model.py
@@ -32,7 +32,7 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, fields=5, lr_r=0.005):
         rng = np.random.default_rng(seed)
         self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
@@ -40,49 +40,65 @@ class FM:
         self.lr, self.l2 = lr, l2
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
+        self.R = np.ones((fields, fields), dtype=np.float32)
+        np.fill_diagonal(self.R, 0.0)
+        self.mR = np.zeros_like(self.R); self.vR = np.zeros_like(self.R)
+        self.lr_r = float(lr_r)
         self.t = 0
 
     def logits(self, X):
         E = self.V[X]                                   # (B,F,k)
-        S = E.sum(1)                                    # (B,k)
-        inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        M = np.einsum('fg,bgk->bfk', self.R, E)
+        inter = 0.5 * (E * M).sum((1, 2))
+        return self.b + self.W[X].sum(1) + inter, E, M
 
     def step(self, X, y):
         B = len(y)
-        z, E, S = self.logits(X)
+        z, E, M = self.logits(X)
         g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
+        np.add.at(gV, X, g[:, None, None] * M)
         gV += self.l2 * self.V; gW += self.l2 * self.W
+        gR = 0.5 * np.einsum('b,bfk,bgk->fg', g, E, E) + self.l2 * self.R
+        np.fill_diagonal(gR, 0.0)
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M *= b1; M += (1 - b1) * G
+        for P, G, M2, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M2 *= b1; M2 += (1 - b1) * G
             Vv *= b2; Vv += (1 - b2) * (G * G)
-            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+            P -= self.lr * (M2 / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        self.mR *= b1; self.mR += (1 - b1) * gR
+        self.vR *= b2; self.vR += (1 - b2) * (gR * gR)
+        self.R -= self.lr_r * (self.mR / (1 - b1 ** self.t)) / (np.sqrt(self.vR / (1 - b2 ** self.t)) + eps)
+        np.fill_diagonal(self.R, 0.0)
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
     def step_pair(self, Xp, Xn):
         B = len(Xp)
-        zp, Ep, Sp = self.logits(Xp)
-        zn, En, Sn = self.logits(Xn)
+        zp, Ep, Mp = self.logits(Xp)
+        zn, En, Mn = self.logits(Xn)
         d = zp - zn
         c = (-sigmoid(-d) / B).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, Xp, c[:, None])
         np.add.at(gW, Xn, -c[:, None])
-        np.add.at(gV, Xp, c[:, None, None] * (Sp[:, None, :] - Ep))
-        np.add.at(gV, Xn, -c[:, None, None] * (Sn[:, None, :] - En))
+        np.add.at(gV, Xp, c[:, None, None] * Mp)
+        np.add.at(gV, Xn, -c[:, None, None] * Mn)
         gV += self.l2 * self.V; gW += self.l2 * self.W
+        gR = 0.5 * (np.einsum('b,bfk,bgk->fg', c, Ep, Ep) - np.einsum('b,bfk,bgk->fg', c, En, En)) + self.l2 * self.R
+        np.fill_diagonal(gR, 0.0)
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M *= b1; M += (1 - b1) * G
+        for P, G, M2, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M2 *= b1; M2 += (1 - b1) * G
             Vv *= b2; Vv += (1 - b2) * (G * G)
-            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+            P -= self.lr * (M2 / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        self.mR *= b1; self.mR += (1 - b1) * gR
+        self.vR *= b2; self.vR += (1 - b2) * (gR * gR)
+        self.R -= self.lr_r * (self.mR / (1 - b1 ** self.t)) / (np.sqrt(self.vR / (1 - b2 ** self.t)) + eps)
+        np.fill_diagonal(self.R, 0.0)
         return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
 
     def predict(self, X, bs=200_000):
@@ -105,9 +121,10 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'],
+                         lr_r=config.get('lr_r', 0.005))
         weights = state['model_state']
-        for name in ('V', 'W', 'b'):
+        for name in ('V', 'W', 'b', 'R'):
             value = weights[name]
             if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
                 raise ValueError('incompatible or nonfinite model weights: ' + name)
diff --git a/train.py b/train.py
index db7e313..b94fef7 100644
--- a/train.py
+++ b/train.py
@@ -98,7 +98,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'],
+                   lr_r=config['lr_r'])
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +116,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'],
+                   lr_r=config['lr_r'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -162,11 +164,11 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b', 'R')}
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'R', 'mR', 'vR')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
             rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
```

---

## Iteration 4: `node_004`

**Status** `success` · **Parent** `node_002` · **Commit** `f0cf8f7e725d`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature engineering — leakage-safe historical label statistics): add strictly-prior-date item-quality features to the FM input, keeping the pairwise-BPR training loop, backbone, and all hyperparameters exactly as they are. Hypothesis: GAUC/nDCG@5 are computed inside per-user groups, so only item-side signal (video, author, tab, duration) can reorder a user's candidates; the current 5 raw ID fields force the model to learn each video's quality from scratch through its own embedding/bias, which is weak for sparse and cold videos. A smoothed historical long-view rate for the video and its author, computed only from training rows with strictly earlier dates and crossed with an exposure-confidence level, gives the model a generalizable quality prior (and lets it interact with user_id, tab and duration bins) without any self-row leakage. Distinction from the closest prior attempt: node_001 (from the pointwise genesis parent) added raw popularity/count buckets, finer duration bins and a tab x duration cross with no label-derived statistics; this experiment uses label-based prior-day target statistics with time-causal construction on the pairwise-BPR parent, and adds only two new fields.

Implement entirely in features.py (no changes to model.py, train.py, config.py or requirements.txt are required, since FM.logits/predict already handle an arbitrary number of fields via X of shape (B, F) and features['dim']/offsets are generic):

1. fit(rows) (called on training rows only, which carry long_view at index 6):
   - Keep the existing 10-bin duration quantile edges and the existing vocab/offsets/dim machinery.
   - Build a sorted list of unique training dates `dates` (rows[i][0], any orderable type) and store it in the state; map each row's date to `t = bisect_left(dates, date)`.
   - Build time-causal history tables for two keys, video_id (index 2) and author_id (index 3). For each key store three parallel plain Python lists: the increasing date indices at which the key occurs, and the inclusive cumulative impression count and cumulative long_view-positive count up to and including each of those date indices. A lookup for query date index t uses `j = bisect_left(date_idx_list, t)` and returns `(cum_cnt[j-1], cum_pos[j-1])` if j > 0 else (0, 0), i.e. strictly earlier dates only.
   - Store the global training long_view rate `g`.
   - Compute, for every training row, the smoothed rates rv = (pos_v + 20*g)/(cnt_v + 20) and ra = (pos_a + 50*g)/(cnt_a + 50); from the rows with cnt_v > 0 derive up to 15 interior quantile edges (16 bins) for rv and, from rows with cnt_a > 0, up to 15 interior quantile edges for ra; deduplicate edges with np.unique and store both edge arrays in the state (handle the degenerate case of zero usable rows or empty edges by storing an empty edge array).
2. Token generation shared by fit and transform (a single helper reading only row indices 0..5, so inference rows without labels work): emit 7 string tokens per row — the existing 5 (user_id, video_id, author_id, tab, duration bin) plus:
   - field 6 = video prior token: 'n' if cnt_v == 0, else f"{bin(rv)}_{conf(cnt_v)}" where bin() is np.searchsorted on the stored video rate edges and conf(c) is 'a' for 1-4, 'b' for 5-19, 'c' for 20-99, 'd' for >=100;
   - field 7 = author prior token: 'n' if cnt_a == 0, else f"{bin(ra)}_{conf(cnt_a)}" using the author rate edges and the same confidence buckets.
3. transform(rows, state): allocate `np.empty((len(rows), len(state['vocabs'])), dtype=np.int32)` instead of the hardcoded 5 columns, and encode all 7 tokens with the existing per-field vocab lookup and offsets (unseen token -> len(vocab), as today). Validation and inference rows use exactly the same fitted history tables and date list; a date at or after the last training date maps to t = len(dates) and therefore uses the full training history, and unseen videos/authors fall into the 'n' token. Never read index 6 inside transform.

Keep fit/transform signatures, the checkpoint payload, the splits, the long_view target, ranking groups, and GAUC/nDCG@5 evaluation unchanged. Use the `bisect` module on plain Python lists for the per-row lookups to keep transform fast; expected added wall clock is well under a minute, far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668808 | 0.535755 | 0.602282 | +0.000412 | 54 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 112 +++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 1 file changed, 104 insertions(+), 8 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..1735925 100644
--- a/features.py
+++ b/features.py
@@ -23,29 +23,125 @@ while preserving the input-row contract and leakage constraints.
 """
 
 # Reference implementation: replaceable while preserving the contracts above.
+from bisect import bisect_left
+
 import numpy as np
 
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+def build_history(rows, key_idx, date_map):
+    tmp = {}
+    for r in rows:
+        t = date_map[r[0]]
+        k = r[key_idx]
+        d = tmp.setdefault(k, {})
+        e = d.setdefault(t, [0, 0])
+        e[0] += 1
+        e[1] += 1 if r[6] == 1 else 0
+    history = {}
+    for k, d in tmp.items():
+        ts = sorted(d.keys())
+        cum_cnt = []
+        cum_pos = []
+        c = 0
+        p = 0
+        for t in ts:
+            c += d[t][0]
+            p += d[t][1]
+            cum_cnt.append(c)
+            cum_pos.append(p)
+        history[k] = (ts, cum_cnt, cum_pos)
+    return history
+
+
+def lookup(history, key, t):
+    entry = history.get(key)
+    if entry is None:
+        return 0, 0
+    ts, cum_cnt, cum_pos = entry
+    j = bisect_left(ts, t)
+    if j > 0:
+        return cum_cnt[j - 1], cum_pos[j - 1]
+    return 0, 0
+
+
+def conf(c):
+    if c < 5:
+        return 'a'
+    if c < 20:
+        return 'b'
+    if c < 100:
+        return 'c'
+    return 'd'
+
+
+def tokens_for(row, state):
+    dur_bin = str(int(np.searchsorted(state['edges'], row[5])))
+    t = bisect_left(state['dates'], row[0])
+    g = state['g']
+    cnt_v, pos_v = lookup(state['video_hist'], row[2], t)
+    cnt_a, pos_a = lookup(state['author_hist'], row[3], t)
+    if cnt_v == 0:
+        tv = 'n'
+    else:
+        rv = (pos_v + 20 * g) / (cnt_v + 20)
+        tv = f"{int(np.searchsorted(state['rv_edges'], rv))}_{conf(cnt_v)}"
+    if cnt_a == 0:
+        ta = 'n'
+    else:
+        ra = (pos_a + 50 * g) / (cnt_a + 50)
+        ta = f"{int(np.searchsorted(state['ra_edges'], ra))}_{conf(cnt_a)}"
+    return [row[1], row[2], row[3], row[4], dur_bin, tv, ta]
 
 
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    dates = sorted(set(r[0] for r in rows))
+    date_map = {d: i for i, d in enumerate(dates)}
+    video_hist = build_history(rows, 2, date_map)
+    author_hist = build_history(rows, 3, date_map)
+    g = float(np.mean([1.0 if r[6] == 1 else 0.0 for r in rows])) if rows else 0.0
+
+    state = dict(dates=dates, video_hist=video_hist, author_hist=author_hist, g=g, edges=edges)
+
+    rv_list = []
+    ra_list = []
+    for r in rows:
+        t = date_map[r[0]]
+        cnt_v, pos_v = lookup(video_hist, r[2], t)
+        cnt_a, pos_a = lookup(author_hist, r[3], t)
+        if cnt_v > 0:
+            rv_list.append((pos_v + 20 * g) / (cnt_v + 20))
+        if cnt_a > 0:
+            ra_list.append((pos_a + 50 * g) / (cnt_a + 50))
+
+    if rv_list:
+        rv_edges = np.unique(np.quantile(rv_list, np.linspace(0, 1, 16)[1:-1]))
+    else:
+        rv_edges = np.array([])
+    if ra_list:
+        ra_edges = np.unique(np.quantile(ra_list, np.linspace(0, 1, 16)[1:-1]))
+    else:
+        ra_edges = np.array([])
+
+    state['rv_edges'] = rv_edges
+    state['ra_edges'] = ra_edges
+
+    vocabs = [{} for _ in range(7)]
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
+        for i, value in enumerate(tokens_for(row, state)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
-    return dict(edges=edges, vocabs=vocabs,
-                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
+    state['vocabs'] = vocabs
+    state['offsets'] = np.cumsum([0] + dims[:-1]).astype(np.int32)
+    state['dim'] = sum(dims)
+    return state
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 5), dtype=np.int32)
+    result = np.empty((len(rows), len(state['vocabs'])), dtype=np.int32)
     for n, row in enumerate(rows):
-        for i, value in enumerate(raw(row, state['edges'])):
+        for i, value in enumerate(tokens_for(row, state)):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
     return result
```

---

## Iteration 5: `node_005`

**Status** `success` · **Parent** `node_004` · **Commit** `25cb04abbca3`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss formulation — listwise sampled-softmax ranking instead of 1-negative pairwise BPR): keep the FM backbone, the leakage-safe prior-date feature set, and all evaluation/checkpoint contracts exactly as they are, and replace the single-negative BPR logistic objective with a within-user sampled softmax (InfoNCE-style listwise) objective that scores each positive against M=4 negatives drawn from the same user's impressions. Hypothesis: GAUC and especially nDCG@5 depend on getting the few true positives above the strongest competitors inside a user's candidate list; a softmax normalized over a positive plus several same-user negatives puts explicit competitive pressure on the top of each list and yields lower-variance, better-scaled gradients than the current one-pair-at-a-time logistic loss, which treats each sampled negative independently. Distinction from the closest supplied prior attempt: node_002 introduced pairwise BPR (one negative, logistic loss) from the pointwise genesis parent; this is a materially different, listwise multi-negative normalized objective applied on top of node_004's feature-enriched code, and no sampled-softmax attempt exists in this lineage or in any supplied sibling (the sampled-softmax mention in memory comes from a different run's deep lineage on a different code state, so this is a transfer experiment).

Implementation:

1. model.py — add a new method `FM.step_group(self, Xp, Xn)` alongside the existing `step` and `step_pair` (leave both in place, and do NOT add any new instance attributes, so train.py's `set(state['latest']) == set(vars(model))` resume check still holds and `logits`/`predict`/`Predictor`/`load_predictor` stay unchanged):
   - `Xp` has shape (B, F) int32 and `Xn` has shape (B, M, F) int32. Build `Xall = np.concatenate([Xp[:, None, :], Xn], axis=1).reshape(B * (1 + M), F)`.
   - Compute `z, E, S = self.logits(Xall)`; reshape `zg = z.reshape(B, 1 + M)`; subtract the per-row max for stability, `p = exp(zg - max) / sum(exp(zg - max))` (float32); loss per group = `-log(p[:, 0] + 1e-12)`.
   - Coefficients: `c = p / B` with `c[:, 0] -= 1.0 / B`, flattened to shape (B*(1+M),) float32.
   - Accumulate into fresh `gV`/`gW`: `np.add.at(gW, Xall, c[:, None])` and `np.add.at(gV, Xall, c[:, None, None] * (S[:, None, :] - E))`; then add `self.l2 * self.V` and `self.l2 * self.W`.
   - Reuse the exact same Adam block as `step_pair` (b1=0.9, b2=0.999, eps=1e-8, `self.t += 1`, same mV/vV/mW/vW buffers, same bias-corrected update) and do not update `self.b` (it cancels inside the softmax; leave it at 0.0 so checkpoint shapes are unchanged).
   - Return `float(np.mean(-np.log(p[:, 0] + 1e-12)))` as the reported training loss.

2. train.py — keep the existing eligible-user index structures (`pos_idx`, `pos_user`, `neg_flat`, `neg_start`, `neg_count`) exactly as built today, and change only the per-epoch sampling and inner loop:
   - `M = config['n_neg']`; `n_groups = len(train_rows)`; `sel = rng.integers(0, len(pos_idx), n_groups)`; `u = pos_user[sel]`; `off = (rng.random((n_groups, M)) * neg_count[u][:, None]).astype(np.int64)`; `neg = neg_flat[neg_start[u][:, None] + off]` (shape (n_groups, M), sampling with replacement so users with fewer than M negatives are handled); `pos_sel = pos_idx[sel]`.
   - Iterate in mini-batches of `config['bs']` groups: `model.step_group(Xtr[pos_sel[i:i+bs]], Xtr[neg[i:i+bs]])`, averaging returned losses for the epoch log.
   - Leave everything else byte-for-byte equivalent in behavior: same `transform` usage, same per-epoch `evaluate(...)` on validation with `model.predict(Xva)`, same best-primary early stopping and best-weight capture, same finiteness checks, same atomic single-file checkpoint payload and resume path, same error when no eligible users exist.

3. config.py — add `n_neg=4` to DEFAULTS and include `'n_neg'` in the integer validation tuple (must be int >= 1); change `bs` from 8192 to 4096 (groups per update, so each update now covers 4096*5 = 20480 scored rows, comparable to the current 8192 pairs = 16384 rows, while doubling updates per epoch). Keep k=16, lr=0.001, l2=1e-6, epochs=60, patience=4, seed=0 unchanged.

features.py and requirements.txt stay exactly as supplied; splits, long_view target, ranking groups, and GAUC/nDCG@5 evaluation are untouched. Expected runtime is roughly 3x the 54 s parent (~150–250 s), far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667393 | 0.536149 | 0.601771 | -0.000511 | 79 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 24 ++++++++++++++++++++++++
 train.py  | 13 +++++++------
 3 files changed, 33 insertions(+), 8 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 75fc434..e309323 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=4, seed=0, n_neg=4)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'n_neg'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index f754fa1..c3fae3a 100644
--- a/model.py
+++ b/model.py
@@ -85,6 +85,30 @@ class FM:
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
 
+    def step_group(self, Xp, Xn):
+        B, F = Xp.shape
+        M = Xn.shape[1]
+        Xall = np.concatenate([Xp[:, None, :], Xn], axis=1).reshape(B * (1 + M), F)
+        z, E, S = self.logits(Xall)
+        zg = z.reshape(B, 1 + M).astype(np.float32)
+        m = zg.max(axis=1, keepdims=True)
+        ez = np.exp(zg - m)
+        p = (ez / ez.sum(axis=1, keepdims=True)).astype(np.float32)
+        c = (p / B).astype(np.float32)
+        c[:, 0] -= 1.0 / B
+        c = c.reshape(-1).astype(np.float32)
+        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        np.add.at(gW, Xall, c[:, None])
+        np.add.at(gV, Xall, c[:, None, None] * (S[:, None, :] - E))
+        gV += self.l2 * self.V; gW += self.l2 * self.W
+        self.t += 1
+        b1, b2, eps = 0.9, 0.999, 1e-8
+        for P, G, M_, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M_ *= b1; M_ += (1 - b1) * G
+            Vv *= b2; Vv += (1 - b2) * (G * G)
+            P -= self.lr * (M_ / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        return float(np.mean(-np.log(p[:, 0] + 1e-12)))
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index db7e313..c4d74c0 100644
--- a/train.py
+++ b/train.py
@@ -150,15 +150,16 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
-        n_pairs = len(train_rows)
-        sel = rng.integers(0, len(pos_idx), n_pairs)
+        M = config['n_neg']
+        n_groups = len(train_rows)
+        sel = rng.integers(0, len(pos_idx), n_groups)
         u = pos_user[sel]
-        off = (rng.random(n_pairs) * neg_count[u]).astype(np.int64)
-        neg = neg_flat[neg_start[u] + off]
+        off = (rng.random((n_groups, M)) * neg_count[u][:, None]).astype(np.int64)
+        neg = neg_flat[neg_start[u][:, None] + off]
         pos_sel = pos_idx[sel]
         bs = config['bs']
-        losses = [model.step_pair(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])
-                  for i in range(0, n_pairs, bs)]
+        losses = [model.step_group(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])
+                  for i in range(0, n_groups, bs)]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

---

## Iteration 6: `node_006`

**Status** `success` · **Parent** `node_004` · **Commit** `0be8dd2f0bf0`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature engineering — leakage-safe, user-conditioned label statistics that vary WITHIN a user's candidate list): extend features.py only, keeping the pairwise-BPR training loop (train.py), the FM backbone (model.py), and all hyperparameters (config.py) exactly as supplied. Hypothesis: GAUC/nDCG@5 are computed inside per-user groups, so only signals that differ across a user's own candidates can change the score; node_004 added item-side priors (video/author long-view rates), which help globally but carry no personalization, and the model must still learn each user's taste for long vs. short videos and for each tab from scratch through the user_id embedding's interactions. Strictly-prior-date statistics of the user's own long-view rate conditioned on the candidate's duration bin and tab, expressed as a deviation from that user's overall prior rate, give a compact, generalizable personalization signal that varies across candidates in the same group. Distinction from the closest supplied prior attempts: node_004 (this parent) added item-side video/author prior-date rate tokens only; node_001 added label-free popularity/duration/tab-cross tokens; node_005 changed the loss. No supplied experiment uses user-conditioned prior-date label statistics.

Implementation (features.py only; do not touch model.py, train.py, config.py, requirements.txt):
1. Generalize `build_history(rows, key_idx, date_map)` to `build_history(rows, key_fn, date_map)` where `key_fn(row)` returns the grouping key, and update the existing video/author calls to `lambda r: r[2]` and `lambda r: r[3]`. Keep the existing cumulative-by-date structure and the existing `lookup(history, key, t)` (strictly earlier dates only) unchanged.
2. Add a small helper `dur_bin(row, edges) -> int(np.searchsorted(edges, row[5]))` and reuse it for the existing duration-bin token (as a string) so the bin definition is shared.
3. In `fit(rows)`, after computing `edges`, `dates`, `date_map`, and the global rate `g`, build three additional histories on training rows only: `user_hist` keyed by `r[1]`, `user_dur_hist` keyed by `(r[1], dur_bin(r, edges))`, and `user_tab_hist` keyed by `(r[1], r[4])`. Store them in the state alongside the existing `video_hist`/`author_hist`.
4. In `tokens_for(row, state)`, after the existing 7 tokens, compute (never reading index 6): `t = bisect_left(state['dates'], row[0])`; `cnt_u, pos_u = lookup(state['user_hist'], row[1], t)` and the user's smoothed prior rate `g_u = (pos_u + 20 * g) / (cnt_u + 20)`; then
   - field 8 (user x duration): `cnt_ud, pos_ud = lookup(state['user_dur_hist'], (row[1], dur_bin(row, state['edges'])), t)`; token `'n'` if `cnt_ud == 0`, else `delta = (pos_ud + 10 * g_u) / (cnt_ud + 10) - g_u` and token `f"{int(np.searchsorted(state['ud_edges'], delta))}_{conf(cnt_ud)}"`;
   - field 9 (user x tab): `cnt_ut, pos_ut = lookup(state['user_tab_hist'], (row[1], row[4]), t)`; token `'n'` if `cnt_ut == 0`, else `delta = (pos_ut + 10 * g_u) / (cnt_ut + 10) - g_u` and token `f"{int(np.searchsorted(state['ut_edges'], delta))}_{conf(cnt_ut)}"`.
   Reuse the existing `conf()` confidence buckets ('a' <5, 'b' <20, 'c' <100, 'd' >=100). `tokens_for` now returns 9 tokens.
5. In `fit`, before building vocabs, derive the two new binning edge arrays from training rows with nonzero counts, using 8 quantile bins each: `ud_edges = np.unique(np.quantile(ud_deltas, np.linspace(0, 1, 9)[1:-1]))` and likewise `ut_edges`, falling back to `np.array([])` when the delta list is empty; store both in the state before the vocab pass so `tokens_for` can be reused there.
6. Change the vocab construction to `vocabs = [{} for _ in range(9)]`; keep the existing dims/offsets/dim computation and leave `transform` as is (it already allocates `len(state['vocabs'])` columns and handles unseen tokens via `vocab.get(value, len(vocab))`).

All statistics come from training rows with strictly earlier dates than the row being encoded, so validation/inference rows reuse the fitted tables with no self-row or same-date leakage; unseen users/keys fall into the 'n' token. Preserve fit/transform signatures, the checkpoint payload, the frozen splits, the long_view target, ranking groups, and GAUC/nDCG@5 evaluation. Expected runtime is roughly 70-110 s (parent 54 s), far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667237 | 0.534521 | 0.600879 | -0.001402 | 81 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 67 +++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 1 file changed, 59 insertions(+), 8 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 1735925..f8f6cb5 100644
--- a/features.py
+++ b/features.py
@@ -28,11 +28,11 @@ from bisect import bisect_left
 import numpy as np
 
 
-def build_history(rows, key_idx, date_map):
+def build_history(rows, key_fn, date_map):
     tmp = {}
     for r in rows:
         t = date_map[r[0]]
-        k = r[key_idx]
+        k = key_fn(r)
         d = tmp.setdefault(k, {})
         e = d.setdefault(t, [0, 0])
         e[0] += 1
@@ -64,6 +64,10 @@ def lookup(history, key, t):
     return 0, 0
 
 
+def dur_bin(row, edges):
+    return int(np.searchsorted(edges, row[5]))
+
+
 def conf(c):
     if c < 5:
         return 'a'
@@ -75,7 +79,7 @@ def conf(c):
 
 
 def tokens_for(row, state):
-    dur_bin = str(int(np.searchsorted(state['edges'], row[5])))
+    dbin = str(dur_bin(row, state['edges']))
     t = bisect_left(state['dates'], row[0])
     g = state['g']
     cnt_v, pos_v = lookup(state['video_hist'], row[2], t)
@@ -90,18 +94,41 @@ def tokens_for(row, state):
     else:
         ra = (pos_a + 50 * g) / (cnt_a + 50)
         ta = f"{int(np.searchsorted(state['ra_edges'], ra))}_{conf(cnt_a)}"
-    return [row[1], row[2], row[3], row[4], dur_bin, tv, ta]
+
+    cnt_u, pos_u = lookup(state['user_hist'], row[1], t)
+    g_u = (pos_u + 20 * g) / (cnt_u + 20)
+
+    cnt_ud, pos_ud = lookup(state['user_dur_hist'], (row[1], dur_bin(row, state['edges'])), t)
+    if cnt_ud == 0:
+        tud = 'n'
+    else:
+        delta = (pos_ud + 10 * g_u) / (cnt_ud + 10) - g_u
+        tud = f"{int(np.searchsorted(state['ud_edges'], delta))}_{conf(cnt_ud)}"
+
+    cnt_ut, pos_ut = lookup(state['user_tab_hist'], (row[1], row[4]), t)
+    if cnt_ut == 0:
+        tut = 'n'
+    else:
+        delta = (pos_ut + 10 * g_u) / (cnt_ut + 10) - g_u
+        tut = f"{int(np.searchsorted(state['ut_edges'], delta))}_{conf(cnt_ut)}"
+
+    return [row[1], row[2], row[3], row[4], dbin, tv, ta, tud, tut]
 
 
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
     dates = sorted(set(r[0] for r in rows))
     date_map = {d: i for i, d in enumerate(dates)}
-    video_hist = build_history(rows, 2, date_map)
-    author_hist = build_history(rows, 3, date_map)
+    video_hist = build_history(rows, lambda r: r[2], date_map)
+    author_hist = build_history(rows, lambda r: r[3], date_map)
+    user_hist = build_history(rows, lambda r: r[1], date_map)
+    user_dur_hist = build_history(rows, lambda r: (r[1], dur_bin(r, edges)), date_map)
+    user_tab_hist = build_history(rows, lambda r: (r[1], r[4]), date_map)
     g = float(np.mean([1.0 if r[6] == 1 else 0.0 for r in rows])) if rows else 0.0
 
-    state = dict(dates=dates, video_hist=video_hist, author_hist=author_hist, g=g, edges=edges)
+    state = dict(dates=dates, video_hist=video_hist, author_hist=author_hist,
+                 user_hist=user_hist, user_dur_hist=user_dur_hist, user_tab_hist=user_tab_hist,
+                 g=g, edges=edges)
 
     rv_list = []
     ra_list = []
@@ -123,10 +150,34 @@ def fit(rows):
     else:
         ra_edges = np.array([])
 
+    ud_deltas = []
+    ut_deltas = []
+    for r in rows:
+        t = date_map[r[0]]
+        cnt_u, pos_u = lookup(user_hist, r[1], t)
+        g_u = (pos_u + 20 * g) / (cnt_u + 20)
+        cnt_ud, pos_ud = lookup(user_dur_hist, (r[1], dur_bin(r, edges)), t)
+        if cnt_ud > 0:
+            ud_deltas.append((pos_ud + 10 * g_u) / (cnt_ud + 10) - g_u)
+        cnt_ut, pos_ut = lookup(user_tab_hist, (r[1], r[4]), t)
+        if cnt_ut > 0:
+            ut_deltas.append((pos_ut + 10 * g_u) / (cnt_ut + 10) - g_u)
+
+    if ud_deltas:
+        ud_edges = np.unique(np.quantile(ud_deltas, np.linspace(0, 1, 9)[1:-1]))
+    else:
+        ud_edges = np.array([])
+    if ut_deltas:
+        ut_edges = np.unique(np.quantile(ut_deltas, np.linspace(0, 1, 9)[1:-1]))
+    else:
+        ut_edges = np.array([])
+
     state['rv_edges'] = rv_edges
     state['ra_edges'] = ra_edges
+    state['ud_edges'] = ud_edges
+    state['ut_edges'] = ut_edges
 
-    vocabs = [{} for _ in range(7)]
+    vocabs = [{} for _ in range(9)]
     for row in rows:
         for i, value in enumerate(tokens_for(row, state)):
             if value not in vocabs[i]:
```

---

## Iteration 7: `node_007`

**Status** `success` · **Parent** `node_004` · **Commit** `073c211e938d`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model backbone — replace the plain factorization machine with a field-aware factorization machine, FFM): keep the pairwise-BPR training loop, the leakage-safe prior-date feature set, and all evaluation/checkpoint contracts exactly as supplied, and change only the interaction structure of the scorer. Hypothesis: GAUC/nDCG@5 are computed inside per-user candidate groups, so ranking quality depends on how well the model represents user×video, user×author, user×tab, user×duration-bin and user×prior-quality interactions; plain FM forces one shared embedding per feature for all of these very different interaction types, so a strong user×duration signal and a weak user×author signal must be encoded in the same vector. Field-aware embeddings give each feature a separate latent vector per interacting field, which typically improves within-list discrimination on small-field, high-cardinality CTR data. Distinction from the closest supplied prior attempts: every experiment in this lineage and both siblings changed either the loss (node_002 pairwise BPR, node_005 listwise sampled softmax) or the features (node_001, node_004 item priors, node_006 user-conditioned priors); no supplied experiment has changed the model architecture, and k/lr/l2 have never been altered.

Implementation:

1. model.py — convert the existing FM class (keep the class name FM so train.py and Predictor imports are unchanged) into an FFM:
   - `__init__(self, dim, fields, k=4, lr=0.001, l2=1e-6, seed=0)`: `self.V = rng.normal(0, 0.01, (dim, fields, k)).astype(np.float32)` (per-feature, per-interacting-field embeddings), `self.W = np.zeros(dim, np.float32)`, `self.b = np.float32(0.0)`, and the same Adam buffers `mV`/`vV` (shaped like V), `mW`/`vW`, `self.t = 0`, `self.lr`, `self.l2`. Add no other instance attributes, so train.py's `set(state['latest']) == set(vars(model))` resume check still holds.
   - `logits(self, X)` with X of shape (B, F) int32: `Vx = self.V[X]` of shape (B, F, F, k) where `Vx[b, i, j]` is the embedding of the feature in field i used for interactions with field j; compute pair indices locally each call with `I, J = np.triu_indices(X.shape[1], 1)` (do not store them as attributes); `pairs = Vx[:, I, J, :] * Vx[:, J, I, :]` of shape (B, P, k); `z = self.b + self.W[X].sum(1) + pairs.sum((1, 2))`; return `(z, Vx)`.
   - Delete the now-unused pointwise `step` method (train.py does not call it) and update `step_pair(self, Xp, Xn)` to the FFM gradients while keeping the identical BPR objective and Adam block: `zp, Vp = self.logits(Xp)`, `zn, Vn = self.logits(Xn)`, `d = zp - zn`, `c = (-sigmoid(-d) / B).astype(np.float32)`; `np.add.at(gW, Xp, c[:, None])`, `np.add.at(gW, Xn, -c[:, None])`; with `I, J = np.triu_indices(Xp.shape[1], 1)` accumulate four scatters into `gV = np.zeros_like(self.V)`: `np.add.at(gV, (Xp[:, I], J), c[:, None, None] * Vp[:, J, I, :])`, `np.add.at(gV, (Xp[:, J], I), c[:, None, None] * Vp[:, I, J, :])`, `np.add.at(gV, (Xn[:, I], J), -c[:, None, None] * Vn[:, J, I, :])`, `np.add.at(gV, (Xn[:, J], I), -c[:, None, None] * Vn[:, I, J, :])`; then `gV += self.l2 * self.V`, `gW += self.l2 * self.W`, `self.t += 1`, and the exact same bias-corrected Adam update (b1=0.9, b2=0.999, eps=1e-8) over (V, gV, mV, vV) and (W, gW, mW, vW); do not update `self.b` (it cancels in the score difference); return `float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))`.
   - `predict` stays `np.concatenate([self.logits(X[i:i+bs])[0] for i in ...])` (index 0 of the new 2-tuple).
   - `Predictor.__init__`: construct `FM(self.features['dim'], fields=len(self.features['offsets']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])`; keep the existing V/W/b shape and finiteness validation (V now validates against shape (dim, F, k)).

2. train.py — only change the two FM constructions (resume path and fresh path) to pass `fields=len(features['offsets'])` alongside the existing k/lr/l2/seed arguments. Leave the pair sampling, per-epoch `evaluate(...)`, early stopping, finiteness checks, atomic single-file checkpoint payload (version, config, features_state, model_state with V/W/b, training_state, context) and resume logic byte-for-byte equivalent in behavior.

3. config.py — set `k=4` in DEFAULTS (per-field embedding width, keeping total latent parameters per feature at 7×4=28, comparable to the previous 16) and leave lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0 unchanged; keep the existing validation rules.

features.py and requirements.txt stay exactly as supplied; splits, long_view target, ranking groups, and GAUC/nDCG@5 evaluation are untouched. Expected runtime is roughly 2–3x the 54 s parent (~110–180 s), far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667989 | 0.535506 | 0.601747 | -0.000534 | 88 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  2 +-
 model.py  | 43 +++++++++++++++----------------------------
 train.py  |  4 ++--
 3 files changed, 18 insertions(+), 31 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 75fc434..f2a03f3 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=4, lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0)
 
 
 def resolve(overrides):
diff --git a/model.py b/model.py
index f754fa1..a058107 100644
--- a/model.py
+++ b/model.py
@@ -32,9 +32,9 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, fields, k=4, lr=0.001, l2=1e-6, seed=0):
         rng = np.random.default_rng(seed)
-        self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
+        self.V = rng.normal(0, 0.01, (dim, fields, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
         self.b = np.float32(0.0)
         self.lr, self.l2 = lr, l2
@@ -43,39 +43,26 @@ class FM:
         self.t = 0
 
     def logits(self, X):
-        E = self.V[X]                                   # (B,F,k)
-        S = E.sum(1)                                    # (B,k)
-        inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
-
-    def step(self, X, y):
-        B = len(y)
-        z, E, S = self.logits(X)
-        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
-        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
-        np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
-        gV += self.l2 * self.V; gW += self.l2 * self.W
-        self.t += 1
-        b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M *= b1; M += (1 - b1) * G
-            Vv *= b2; Vv += (1 - b2) * (G * G)
-            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
-        self.b -= self.lr * g.sum()
-        return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
+        Vx = self.V[X]                                   # (B,F,F,k)
+        I, J = np.triu_indices(X.shape[1], 1)
+        pairs = Vx[:, I, J, :] * Vx[:, J, I, :]           # (B,P,k)
+        z = self.b + self.W[X].sum(1) + pairs.sum((1, 2))
+        return z, Vx
 
     def step_pair(self, Xp, Xn):
         B = len(Xp)
-        zp, Ep, Sp = self.logits(Xp)
-        zn, En, Sn = self.logits(Xn)
+        zp, Vp = self.logits(Xp)
+        zn, Vn = self.logits(Xn)
         d = zp - zn
         c = (-sigmoid(-d) / B).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, Xp, c[:, None])
         np.add.at(gW, Xn, -c[:, None])
-        np.add.at(gV, Xp, c[:, None, None] * (Sp[:, None, :] - Ep))
-        np.add.at(gV, Xn, -c[:, None, None] * (Sn[:, None, :] - En))
+        I, J = np.triu_indices(Xp.shape[1], 1)
+        np.add.at(gV, (Xp[:, I], J), c[:, None, None] * Vp[:, J, I, :])
+        np.add.at(gV, (Xp[:, J], I), c[:, None, None] * Vp[:, I, J, :])
+        np.add.at(gV, (Xn[:, I], J), -c[:, None, None] * Vn[:, J, I, :])
+        np.add.at(gV, (Xn[:, J], I), -c[:, None, None] * Vn[:, I, J, :])
         gV += self.l2 * self.V; gW += self.l2 * self.W
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
@@ -105,7 +92,7 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        self.model = FM(self.features['dim'], fields=len(self.features['offsets']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         weights = state['model_state']
         for name in ('V', 'W', 'b'):
             value = weights[name]
diff --git a/train.py b/train.py
index db7e313..4e7e46e 100644
--- a/train.py
+++ b/train.py
@@ -98,7 +98,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], fields=len(features['offsets']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +115,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], fields=len(features['offsets']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
```

---

## Iteration 8: `node_008`

**Status** `success` · **Parent** `node_004` · **Commit** `5d3a7914ae00`

### Hypothesis

```text
SELECTED CHANGE
Experiment (optimizer/regularization mechanics of the FM backbone — a subsystem never touched in this lineage): replace the dense Adam + L2-in-gradient update in `FM.step_pair` with a sparse "lazy" Adam update restricted to the embedding rows that actually appear in the mini-batch, plus decoupled multiplicative weight decay on those same rows. Keep the pairwise-BPR objective, the feature set, the FM interaction form, and all train.py logic exactly as supplied.

Hypothesis (grounded in the supplied code): today `step_pair` builds full-size `gV`/`gW`, adds `self.l2 * self.V` / `self.l2 * self.W` densely, and then runs a dense Adam update over the entire embedding table on every mini-batch. For any row that received no data gradient, its gradient is the constant `l2*P`, so Adam's normalization makes the step size roughly `lr * g/(sqrt(g^2)+eps) ≈ lr = 1e-3` per step regardless of how tiny `l2` is. With embeddings initialized at N(0, 0.01), a row that is not touched for ~10–20 consecutive steps is driven to (and then oscillates around) zero. Since a mini-batch of 8192 pairs touches only a small fraction of the user/video/author vocabulary, this silently erases the embeddings of all but the most frequent features, which is exactly the cold/mid-frequency item signal that within-user GAUC/nDCG@5 ranking depends on. Making the update sparse should let moderately frequent video/author/user embeddings survive between their updates, and should also cut per-step cost sharply (no dense O(dim×k) moment math), leaving headroom inside the epochs=60 / patience=4 budget.

Implementation:

1. model.py — rewrite the body of `FM.step_pair(Xp, Xn)` only (leave `__init__`, `logits`, `predict`, the unused pointwise `step`, `Predictor`, `read_checkpoint`, and `load_predictor` unchanged, and add no new instance attributes so train.py's `set(state['latest']) == set(vars(model))` resume check still holds):
   - Keep the current forward/BPR math: `zp, Ep, Sp = self.logits(Xp)`, `zn, En, Sn = self.logits(Xn)`, `d = zp - zn`, `B = len(Xp)`, `c = (-sigmoid(-d) / B).astype(np.float32)`, and return `float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))`. Do not update `self.b`.
   - Compress indices: `flat = np.concatenate((Xp.ravel(), Xn.ravel()))`; `idx, inv = np.unique(flat, return_inverse=True)`; `loc_p = inv[:Xp.size].reshape(Xp.shape)`; `loc_n = inv[Xp.size:].reshape(Xn.shape)`.
   - Allocate compact gradient buffers `gV = np.zeros((len(idx), self.V.shape[1]), np.float32)` and `gW = np.zeros(len(idx), np.float32)` and scatter exactly the same gradients as today but into the local index space: `np.add.at(gW, loc_p, c[:, None])`, `np.add.at(gW, loc_n, -c[:, None])`, `np.add.at(gV, loc_p, c[:, None, None] * (Sp[:, None, :] - Ep))`, `np.add.at(gV, loc_n, -c[:, None, None] * (Sn[:, None, :] - En))`. Do NOT add any dense `l2 * V` / `l2 * W` term to the gradient.
   - Lazy Adam on the touched rows only, with the same constants (b1=0.9, b2=0.999, eps=1e-8) and the same global step counter `self.t += 1` used for bias correction: read `mV_i = self.mV[idx]`, `vV_i = self.vV[idx]`; compute `mV_i = b1*mV_i + (1-b1)*gV`, `vV_i = b2*vV_i + (1-b2)*(gV*gV)`; write them back with `self.mV[idx] = mV_i`, `self.vV[idx] = vV_i`; then `self.V[idx] = self.V[idx] * (1.0 - self.l2) - self.lr * (mV_i/(1-b1**self.t)) / (np.sqrt(vV_i/(1-b2**self.t)) + eps)`. Apply the identical procedure to `self.W`/`self.mW`/`self.vW` with `gW`. `idx` is unique, so fancy-index assignment is safe. Keep all arrays float32.
   - Note in a short comment that `self.l2` is now interpreted as a decoupled per-touch multiplicative shrink factor rather than an added gradient penalty.

2. config.py — change `l2` in DEFAULTS from `1e-6` to `1e-4` (its meaning is now a per-touch decoupled decay rate; 1e-4 gives ~1% shrink per 100 updates of a row, replacing the implicit regularization that the removed dense decay used to provide). Leave k=16, lr=0.001, epochs=60, bs=8192, patience=4, seed=0 and the existing validation rules unchanged.

3. train.py, features.py, requirements.txt — unchanged. Splits, the long_view target, ranking groups, GAUC/nDCG@5 evaluation, the checkpoint payload (version/config/features_state/model_state with V/W/b/training_state/context) and the resume path stay exactly as supplied.

Distinction from prior attempts: the supplied siblings from this same parent changed the loss (node_005 listwise sampled softmax), the features (node_006 user-conditioned prior stats), and the interaction structure (node_007 FFM); nothing in this lineage has altered the optimizer/regularization mechanics. This is not a hyperparameter sweep of k/lr/epochs but a change to how updates are applied (sparse lazy Adam + decoupled decay). Expected runtime is at or below the 54 s parent, far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668970 | 0.535930 | 0.602450 | +0.000169 | 62 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  2 +-
 model.py  | 40 ++++++++++++++++++++++++++++++----------
 2 files changed, 31 insertions(+), 11 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 75fc434..8dd5c0e 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0)
 
 
 def resolve(overrides):
diff --git a/model.py b/model.py
index f754fa1..f1627a2 100644
--- a/model.py
+++ b/model.py
@@ -66,23 +66,43 @@ class FM:
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
     def step_pair(self, Xp, Xn):
+        # self.l2 is a decoupled per-touch multiplicative shrink factor, not
+        # an added gradient penalty.
         B = len(Xp)
         zp, Ep, Sp = self.logits(Xp)
         zn, En, Sn = self.logits(Xn)
         d = zp - zn
         c = (-sigmoid(-d) / B).astype(np.float32)
-        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
-        np.add.at(gW, Xp, c[:, None])
-        np.add.at(gW, Xn, -c[:, None])
-        np.add.at(gV, Xp, c[:, None, None] * (Sp[:, None, :] - Ep))
-        np.add.at(gV, Xn, -c[:, None, None] * (Sn[:, None, :] - En))
-        gV += self.l2 * self.V; gW += self.l2 * self.W
+
+        flat = np.concatenate((Xp.ravel(), Xn.ravel()))
+        idx, inv = np.unique(flat, return_inverse=True)
+        loc_p = inv[:Xp.size].reshape(Xp.shape)
+        loc_n = inv[Xp.size:].reshape(Xn.shape)
+
+        gV = np.zeros((len(idx), self.V.shape[1]), np.float32)
+        gW = np.zeros(len(idx), np.float32)
+        np.add.at(gW, loc_p, c[:, None])
+        np.add.at(gW, loc_n, -c[:, None])
+        np.add.at(gV, loc_p, c[:, None, None] * (Sp[:, None, :] - Ep))
+        np.add.at(gV, loc_n, -c[:, None, None] * (Sn[:, None, :] - En))
+
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M *= b1; M += (1 - b1) * G
-            Vv *= b2; Vv += (1 - b2) * (G * G)
-            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+
+        mV_i = self.mV[idx]; vV_i = self.vV[idx]
+        mV_i = b1 * mV_i + (1 - b1) * gV
+        vV_i = b2 * vV_i + (1 - b2) * (gV * gV)
+        self.mV[idx] = mV_i; self.vV[idx] = vV_i
+        self.V[idx] = self.V[idx] * (1.0 - self.l2) - self.lr * (mV_i / (1 - b1 ** self.t)) / (
+            np.sqrt(vV_i / (1 - b2 ** self.t)) + eps)
+
+        mW_i = self.mW[idx]; vW_i = self.vW[idx]
+        mW_i = b1 * mW_i + (1 - b1) * gW
+        vW_i = b2 * vW_i + (1 - b2) * (gW * gW)
+        self.mW[idx] = mW_i; self.vW[idx] = vW_i
+        self.W[idx] = self.W[idx] * (1.0 - self.l2) - self.lr * (mW_i / (1 - b1 ** self.t)) / (
+            np.sqrt(vW_i / (1 - b2 ** self.t)) + eps)
+
         return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
 
     def predict(self, X, bs=200_000):
```

---

## Iteration 9: `node_009`

**Status** `success` · **Parent** `node_008` · **Commit** `e35793ad792f`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model backbone — field-weighted factorization machine, FwFM): generalize the FM interaction term in model.py from the uniform sum-trick to a learned symmetric field-pair weight matrix R, keeping the pairwise-BPR loop, the sparse lazy-Adam/decoupled-decay update, the leakage-safe prior-date features, and all config values exactly as supplied. Hypothesis: with 7 fields (user_id, video_id, author_id, tab, duration bin, video prior token, author prior token) the current FM sums all 21 pairwise dot products with equal weight, even though several pairs are largely redundant or noisy (video_id x author_id are near-deterministic duplicates, video prior x author prior overlap heavily), which dilutes the informative user x item and duration x item interactions that drive within-user ordering. Letting the model learn 21 scalar pair weights should sharpen the useful interactions at negligible parameter cost. Distinction from the closest supplied prior attempt: node_007 from node_004 replaced FM with FFM (a separate embedding per feature per target field, a huge parameter blowup) and regressed by 0.0005; FwFM keeps exactly one embedding vector per feature and adds only F*(F-1)/2 = 21 scalars, and it is initialized to reproduce the parent model exactly, so it is a strict, low-variance generalization rather than a capacity explosion.

Implementation:

1. model.py — FM.__init__: add a keyword argument `fields` (int, default 7) and store `self.F = fields` plus a new parameter `self.R = np.ones((fields, fields), dtype=np.float32)` with `np.fill_diagonal(self.R, 0.0)`, and Adam moment buffers `self.mR = np.zeros_like(self.R)`, `self.vR = np.zeros_like(self.R)`. Keep every existing attribute (V, W, b, lr, l2, mV, vV, mW, vW, t) unchanged so train.py's `set(state['latest']) == set(vars(model))` resume check still passes for models built the same way.

2. model.py — FM.logits(X): compute `E = self.V[X]` (B,F,k), `P = np.einsum('ij,bjk->bik', self.R, E)` (B,F,k), `inter = 0.5 * np.einsum('bik,bik->b', E, P)`, and return `self.b + self.W[X].sum(1) + inter, E, P` (i.e. the third returned array now carries the R-weighted partner sum instead of the plain field sum S). Because R starts at all-ones with zero diagonal, this is numerically identical to the supplied FM at initialization.

3. model.py — FM.step_pair(Xp, Xn): keep the BPR math, the unique-index compression (flat/idx/inv/loc_p/loc_n), the compact gV/gW scatter, the sparse lazy Adam on the touched rows, the decoupled multiplicative shrink `* (1.0 - self.l2)` on V and W, the shared `self.t` bias correction, no update to self.b, and the same returned loss. Only substitute the embedding gradient to use the new third return value: `np.add.at(gV, loc_p, c[:, None, None] * Pp)` and `np.add.at(gV, loc_n, -c[:, None, None] * Pn)` where `zp, Ep, Pp = self.logits(Xp)` and `zn, En, Pn = self.logits(Xn)`. Add the field-weight gradient `gR = 0.5 * (np.einsum('b,bik,bjk->ij', c, Ep, Ep) - np.einsum('b,bik,bjk->ij', c, En, En))` as float32, then `np.fill_diagonal(gR, 0.0)`, and update R with a dense Adam step using the same constants (b1=0.9, b2=0.999, eps=1e-8) and the same `self.t`: `self.mR = b1*self.mR + (1-b1)*gR`, `self.vR = b2*self.vR + (1-b2)*(gR*gR)`, `self.R -= self.lr * (self.mR/(1-b1**self.t)) / (np.sqrt(self.vR/(1-b2**self.t)) + eps)`, then `np.fill_diagonal(self.R, 0.0)`. Do not apply the decoupled l2 shrink to R (it must be free to stay near its 1.0 baseline). gR is symmetric by construction, so R stays symmetric.

4. model.py — keep the unused pointwise `step` consistent with the new logits return by scattering `g[:, None, None] * P` into gV (rename its unpacked third variable accordingly); leave everything else in it alone.

5. model.py — Predictor.__init__: build the model as `FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], fields=len(self.features['vocabs']))` and restore/validate the weight names `('V', 'W', 'b', 'R')` with the existing shape and finiteness checks. read_checkpoint and load_predictor stay unchanged.

6. train.py — pass `fields=len(features['vocabs'])` to both FM constructions (resume branch and fresh branch); change the best-weight capture to `for key in ('V', 'W', 'b', 'R')`; extend the nonfinite guard tuple to `('V', 'W', 'b', 'R', 'mV', 'vV', 'mW', 'vW', 'mR', 'vR')`. Everything else in train.py (pairwise sampling arrays, epoch loop, per-epoch evaluate on validation, patience/early stopping, atomic single-file checkpoint payload, resume path) stays exactly as supplied.

7. config.py, features.py, requirements.txt — unchanged (k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0).

Splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, and test isolation are untouched. The added einsums are O(B*F*F*k) with F=7, k=16, so expected wall clock is roughly 2-3x the 62 s parent, far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668778 | 0.535731 | 0.602255 | -0.000196 | 80 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
model.py | 38 ++++++++++++++++++++++++++------------
 train.py |  8 ++++----
 2 files changed, 30 insertions(+), 16 deletions(-)
```

```diff
diff --git a/model.py b/model.py
index f1627a2..c9a5515 100644
--- a/model.py
+++ b/model.py
@@ -32,7 +32,7 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, fields=7):
         rng = np.random.default_rng(seed)
         self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
@@ -40,21 +40,25 @@ class FM:
         self.lr, self.l2 = lr, l2
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
+        self.F = fields
+        self.R = np.ones((fields, fields), dtype=np.float32)
+        np.fill_diagonal(self.R, 0.0)
+        self.mR = np.zeros_like(self.R); self.vR = np.zeros_like(self.R)
         self.t = 0
 
     def logits(self, X):
         E = self.V[X]                                   # (B,F,k)
-        S = E.sum(1)                                    # (B,k)
-        inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        P = np.einsum('ij,bjk->bik', self.R, E)          # (B,F,k)
+        inter = 0.5 * np.einsum('bik,bik->b', E, P)
+        return self.b + self.W[X].sum(1) + inter, E, P
 
     def step(self, X, y):
         B = len(y)
-        z, E, S = self.logits(X)
+        z, E, P = self.logits(X)
         g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
+        np.add.at(gV, X, g[:, None, None] * P)
         gV += self.l2 * self.V; gW += self.l2 * self.W
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
@@ -69,8 +73,8 @@ class FM:
         # self.l2 is a decoupled per-touch multiplicative shrink factor, not
         # an added gradient penalty.
         B = len(Xp)
-        zp, Ep, Sp = self.logits(Xp)
-        zn, En, Sn = self.logits(Xn)
+        zp, Ep, Pp = self.logits(Xp)
+        zn, En, Pn = self.logits(Xn)
         d = zp - zn
         c = (-sigmoid(-d) / B).astype(np.float32)
 
@@ -83,8 +87,12 @@ class FM:
         gW = np.zeros(len(idx), np.float32)
         np.add.at(gW, loc_p, c[:, None])
         np.add.at(gW, loc_n, -c[:, None])
-        np.add.at(gV, loc_p, c[:, None, None] * (Sp[:, None, :] - Ep))
-        np.add.at(gV, loc_n, -c[:, None, None] * (Sn[:, None, :] - En))
+        np.add.at(gV, loc_p, c[:, None, None] * Pp)
+        np.add.at(gV, loc_n, -c[:, None, None] * Pn)
+
+        gR = 0.5 * (np.einsum('b,bik,bjk->ij', c, Ep, Ep) -
+                     np.einsum('b,bik,bjk->ij', c, En, En)).astype(np.float32)
+        np.fill_diagonal(gR, 0.0)
 
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
@@ -103,6 +111,12 @@ class FM:
         self.W[idx] = self.W[idx] * (1.0 - self.l2) - self.lr * (mW_i / (1 - b1 ** self.t)) / (
             np.sqrt(vW_i / (1 - b2 ** self.t)) + eps)
 
+        self.mR = b1 * self.mR + (1 - b1) * gR
+        self.vR = b2 * self.vR + (1 - b2) * (gR * gR)
+        self.R -= self.lr * (self.mR / (1 - b1 ** self.t)) / (
+            np.sqrt(self.vR / (1 - b2 ** self.t)) + eps)
+        np.fill_diagonal(self.R, 0.0)
+
         return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
 
     def predict(self, X, bs=200_000):
@@ -125,9 +139,9 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], fields=len(self.features['vocabs']))
         weights = state['model_state']
-        for name in ('V', 'W', 'b'):
+        for name in ('V', 'W', 'b', 'R'):
             value = weights[name]
             if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
                 raise ValueError('incompatible or nonfinite model weights: ' + name)
diff --git a/train.py b/train.py
index db7e313..963f08b 100644
--- a/train.py
+++ b/train.py
@@ -98,7 +98,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], fields=len(features['vocabs']))
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +115,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], fields=len(features['vocabs']))
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -162,11 +162,11 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b', 'R')}
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'R', 'mV', 'vV', 'mW', 'vW', 'mR', 'vR')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
             rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
```

---

## Iteration 10: `node_010`

**Status** `success` · **Parent** `node_008` · **Commit** `d19b2dcebc17`

### Hypothesis

```text
SELECTED CHANGE
Experiment (negative-sampling / loss subsystem — dynamic hard-negative selection for the pairwise BPR objective): keep the FM backbone, the leakage-safe prior-date features, and the sparse lazy-Adam + decoupled-decay update exactly as supplied, but replace the single uniformly sampled in-user negative with a max-score selection out of a small pool of uniformly sampled in-user negatives (DNS / "max-of-M").

Hypothesis: every negative here is a genuinely observed non-long-view impression from the same user's candidate set, so hard negatives are true negatives (no false-negative risk as in implicit-feedback item sampling), and they are exactly the rows the evaluator ranks against the positives. Uniform in-user negatives are mostly already well separated after a few epochs, so almost all sampled pairs contribute near-zero BPR gradient; selecting the highest-scoring candidate concentrates the gradient on the top of each user's ranking, which is precisely what GAUC and the top-heavy nDCG@5 reward. Distinction from the closest supplied prior attempts: node_005 (from node_004) changed the objective to a listwise sampled softmax on a different parent, node_009 (same parent) changed the interaction form (FwFM), and nothing in this lineage has changed how the negative in each training pair is chosen — the parent still draws one uniform negative per pair.

Implementation:

1. config.py — add `neg_pool=5` to DEFAULTS (keep k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0) and include `'neg_pool'` in the integer validation tuple in `resolve` so it is validated as an int >= 1 and serialized into the checkpoint config.

2. model.py — add one new method `FM.step_pair_hard(self, Xp, Xnc)` next to the existing `step_pair` (do not delete or otherwise modify `__init__`, `logits`, `step`, `step_pair`, `predict`, `Predictor`, `read_checkpoint`, or `load_predictor`, and add no new instance attributes so train.py's `set(state['latest']) == set(vars(model))` resume check still holds):
   - `Xnc` has shape (B, M, F). Compute candidate scores with a single forward pass: `zn_all = self.logits(Xnc.reshape(-1, Xnc.shape[2]))[0].reshape(Xnc.shape[0], Xnc.shape[1])` (no parameter updates in this pass).
   - Select the hardest negative per pair: `j = zn_all.argmax(1)`, `Xn = Xnc[np.arange(Xnc.shape[0]), j]` (contiguous int32 array of shape (B, F)).
   - Return `self.step_pair(Xp, Xn)` so the BPR gradient math, unique-index compression, compact scatter, sparse lazy Adam with shared `self.t`, decoupled `(1 - self.l2)` shrink, unchanged `self.b`, and the returned loss value stay exactly as supplied.

3. train.py — keep the eligible-user construction (pos_idx, pos_user, neg_flat, neg_start, neg_count), the epoch loop, per-epoch `evaluate` on validation, best-primary early stopping with patience, finiteness guard, atomic single-file checkpoint payload, and resume path exactly as they are. Only change the per-epoch negative draw and the batch call:
   - `M = config['neg_pool']`; after computing `sel`, `u = pos_user[sel]`, and `pos_sel = pos_idx[sel]`, draw a pool: `off = (rng.random((n_pairs, M)) * neg_count[u][:, None]).astype(np.int64)` and `neg = neg_flat[neg_start[u][:, None] + off]` (shape (n_pairs, M), duplicates allowed).
   - In the mini-batch loop call `model.step_pair_hard(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])`, where `Xtr[neg[i:i+bs]]` has shape (b, M, F); keep averaging the returned losses for the epoch log.

features.py and requirements.txt are unchanged. Splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, and test isolation are untouched. The extra cost is one additional forward pass over 5x negatives per batch (no extra scatter/update work), so expected wall clock is roughly 1.2–1.5x the 62 s parent, far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.633432 | 0.522731 | 0.578081 | -0.024369 | 81 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py | 4 ++--
 model.py  | 6 ++++++
 train.py  | 7 ++++---
 3 files changed, 12 insertions(+), 5 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 8dd5c0e..b73509f 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, neg_pool=5)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'neg_pool'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index f1627a2..688d324 100644
--- a/model.py
+++ b/model.py
@@ -105,6 +105,12 @@ class FM:
 
         return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
 
+    def step_pair_hard(self, Xp, Xnc):
+        zn_all = self.logits(Xnc.reshape(-1, Xnc.shape[2]))[0].reshape(Xnc.shape[0], Xnc.shape[1])
+        j = zn_all.argmax(1)
+        Xn = np.ascontiguousarray(Xnc[np.arange(Xnc.shape[0]), j]).astype(np.int32)
+        return self.step_pair(Xp, Xn)
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index db7e313..fff6842 100644
--- a/train.py
+++ b/train.py
@@ -153,11 +153,12 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         n_pairs = len(train_rows)
         sel = rng.integers(0, len(pos_idx), n_pairs)
         u = pos_user[sel]
-        off = (rng.random(n_pairs) * neg_count[u]).astype(np.int64)
-        neg = neg_flat[neg_start[u] + off]
+        M = config['neg_pool']
+        off = (rng.random((n_pairs, M)) * neg_count[u][:, None]).astype(np.int64)
+        neg = neg_flat[neg_start[u][:, None] + off]
         pos_sel = pos_idx[sel]
         bs = config['bs']
-        losses = [model.step_pair(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])
+        losses = [model.step_pair_hard(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])
                   for i in range(0, n_pairs, bs)]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
```

---

## Iteration 11: `node_011`

**Status** `success` · **Parent** `node_008` · **Commit** `ce9e7bfdf9ff`

### Hypothesis

```text
SELECTED CHANGE
Experiment (training-distribution / pair-sampling subsystem — metric-aligned per-user uniform sampling of BPR pairs): keep the FM backbone, the leakage-safe prior-date features, the pairwise-BPR loss with one uniformly drawn in-user negative, and the sparse lazy-Adam + decoupled-decay update exactly as supplied; change only how a training pair's user is chosen, so that every eligible user contributes the same expected number of pairs per epoch instead of a number proportional to that user's positive count.

Hypothesis: GAUC is the mean of per-user AUCs and nDCG@5 is averaged per ranking group, so each user counts equally in the objective. The current sampler draws `sel = rng.integers(0, len(pos_idx), n_pairs)` over the flat concatenation of all positives, which weights a user proportionally to how many long-view impressions they have; heavy users therefore dominate the gradient while the metric weights them the same as a user with one positive. Re-weighting the pair distribution to be uniform over eligible users should align the training distribution with the evaluation weighting and improve mid/low-activity users' within-group ordering, where most of the unexploited GAUC headroom lies. This is orthogonal to negative hardness: node_010 (same parent) changed which negative is picked (max-of-M) and regressed sharply, which suggests concentrating gradient on the top of each list hurts; here negatives stay uniformly drawn and only the user marginal changes. No supplied sibling or ancestor has altered the user-level sampling distribution.

Implementation (train.py only; model.py, features.py, config.py, requirements.txt unchanged):

1. In the pre-epoch setup, keep the existing eligible-user construction (`users` dict keyed by `r[1]` with [neg_list, pos_list], `eligible` = users having both) and keep `neg_flat`, `neg_start`, `neg_count` exactly as built today. Replace the `pos_idx` / `pos_user` pair of arrays with per-user flat positive arrays built in the same loop over `eligible`: `pos_flat` (all eligible users' positive row indices concatenated in eligible-user order, dtype int64), `pos_start` (int64, offset of each user's block) and `pos_count` (int64, number of positives per user). Retain the `raise ValueError('no eligible users with both positive and negative impressions')` guard.

2. Inside the epoch loop, replace the current draw with a user-uniform draw, keeping `n_pairs = len(train_rows)` and the same `rng`:
   - `u = rng.integers(0, len(eligible), n_pairs)`
   - `poff = (rng.random(n_pairs) * pos_count[u]).astype(np.int64)`; `pos_sel = pos_flat[pos_start[u] + poff]`
   - `noff = (rng.random(n_pairs) * neg_count[u]).astype(np.int64)`; `neg = neg_flat[neg_start[u] + noff]`
   - keep the identical mini-batch loop `model.step_pair(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])` with `bs = config['bs']` and the same epoch-loss averaging for the log line.

3. Everything else in train.py stays byte-for-byte equivalent in behavior: same `transform` usage for Xtr/Xva, same per-epoch `evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))`, same best-primary tracking with `patience` early stopping, same best-weight capture for ('V','W','b'), same nonfinite guard, same atomic single-file checkpoint payload (version, config, features_state, model_state, training_state with epoch/best/bad/rng/latest, validation, context) and the same resume path (the saved RNG bit-generator state keeps resume exact under the new draw sequence).

Config stays k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0. The number of sampled pairs per epoch and all per-batch work are unchanged, so expected wall clock stays near the 62 s parent, far inside candidate_timeout_s=1800. Splits, the long_view target, ranking groups, GAUC/nDCG@5 evaluation, and test isolation are untouched.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.660966 | 0.533436 | 0.597201 | -0.005249 | 67 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
train.py | 31 +++++++++++++++++--------------
 1 file changed, 17 insertions(+), 14 deletions(-)
```

```diff
diff --git a/train.py b/train.py
index db7e313..411b237 100644
--- a/train.py
+++ b/train.py
@@ -130,32 +130,35 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     if not eligible:
         raise ValueError('no eligible users with both positive and negative impressions')
 
-    pos_idx_list = []
-    pos_user_list = []
+    pos_flat_list = []
     neg_flat_list = []
+    pos_start = np.zeros(len(eligible), dtype=np.int64)
+    pos_count = np.zeros(len(eligible), dtype=np.int64)
     neg_start = np.zeros(len(eligible), dtype=np.int64)
     neg_count = np.zeros(len(eligible), dtype=np.int64)
-    offset = 0
+    poffset = 0
+    noffset = 0
     for uidx, (neg, pos) in enumerate(eligible):
-        pos_idx_list.extend(pos)
-        pos_user_list.extend([uidx] * len(pos))
-        neg_start[uidx] = offset
+        pos_start[uidx] = poffset
+        pos_count[uidx] = len(pos)
+        pos_flat_list.extend(pos)
+        poffset += len(pos)
+        neg_start[uidx] = noffset
         neg_count[uidx] = len(neg)
         neg_flat_list.extend(neg)
-        offset += len(neg)
-    pos_idx = np.asarray(pos_idx_list, dtype=np.int64)
-    pos_user = np.asarray(pos_user_list, dtype=np.int64)
+        noffset += len(neg)
+    pos_flat = np.asarray(pos_flat_list, dtype=np.int64)
     neg_flat = np.asarray(neg_flat_list, dtype=np.int64)
 
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
         n_pairs = len(train_rows)
-        sel = rng.integers(0, len(pos_idx), n_pairs)
-        u = pos_user[sel]
-        off = (rng.random(n_pairs) * neg_count[u]).astype(np.int64)
-        neg = neg_flat[neg_start[u] + off]
-        pos_sel = pos_idx[sel]
+        u = rng.integers(0, len(eligible), n_pairs)
+        poff = (rng.random(n_pairs) * pos_count[u]).astype(np.int64)
+        pos_sel = pos_flat[pos_start[u] + poff]
+        noff = (rng.random(n_pairs) * neg_count[u]).astype(np.int64)
+        neg = neg_flat[neg_start[u] + noff]
         bs = config['bs']
         losses = [model.step_pair(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])
                   for i in range(0, n_pairs, bs)]
```

---

## Iteration 12: `node_012`

**Status** `success` · **Parent** `node_008` · **Commit** `f7ff125f089d`

### Hypothesis

```text
SELECTED CHANGE
Experiment (prediction aggregation / model ensembling — a subsystem never touched in this lineage): replace the single FM with a lockstep-trained bag of 3 independently seeded FM replicas whose validation and inference scores are averaged, keeping the pairwise-BPR objective, the leakage-safe prior-date features, the sparse lazy-Adam + decoupled-decay update, and all other hyperparameters exactly as supplied. Hypothesis: per-user GAUC and top-5 nDCG on this data are dominated by variance in the learned embeddings of sparse users/videos/authors (single-run deltas across the whole lineage are only ~0.0002–0.0008), so averaging the scores of several models that differ only in initialization and pair-sampling noise should cancel that variance and produce a larger, more reliable within-group ordering gain than another structural or sampling tweak. Distinction from the closest supplied prior attempts: siblings from this same parent changed the interaction form (node_009 FwFM), the negative selection rule (node_010 max-of-M hard negatives), and the user marginal of the pair sampler (node_011); none trained or aggregated multiple models, and nothing in the lineage has altered how predictions are produced at inference.

Implementation:

1. config.py — add `n_models=3` to DEFAULTS (keep k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0) and include `'n_models'` in the integer validation tuple in `resolve` so it is checked as an int >= 1 and serialized into the checkpoint config.

2. model.py — leave the `FM` class (including `logits`, `step`, `step_pair`, `predict`) and `read_checkpoint` unchanged. Change only `Predictor`: `state['model_state']` is now a list of per-replica weight dicts with keys ('V','W','b'). Build `self.models = [FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i) for i in range(len(state['model_state']))]`, restore each replica's weights with the existing shape and finiteness validation (raise ValueError on mismatch or nonfinite values), and make `predict(rows)` transform the rows once and return `np.mean([m.predict(X) for m in self.models], axis=0)` as a finite float array in input order (still returning `np.empty(0, dtype=np.float32)` for empty input). `load_predictor(checkpoint_path)` keeps its signature and behavior.

3. train.py — keep the `train(train_rows, valid_rows, checkpoint_path, overrides, context)` signature, the eligible-user construction (pos_idx, pos_user, neg_flat, neg_start, neg_count with the existing ValueError guard), the activity-weighted uniform-negative pair draw, `n_pairs = len(train_rows)`, the mini-batch loop over `config['bs']` calling `model.step_pair(...)`, per-epoch `evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], scores)`, best-primary early stopping with `patience`, the atomic temp-file-then-os.replace save, and the resume path. Generalize them to N = config['n_models'] replicas:
   - Construct `models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i) for i in range(N)]` in both the fresh and resume branches, and keep one independent sampling RNG per replica, `rngs = [np.random.default_rng(config['seed'] + 1000 + i) for i in range(N)]`, so replicas differ in both initialization and sampled pairs.
   - Each epoch, for every replica i draw its own `sel/u/off/neg/pos_sel` from `rngs[i]` exactly as the current code does and run its mini-batch `step_pair` updates; average all replicas' per-batch losses for the log line.
   - Compute the ensemble validation score as `scores = np.mean([m.predict(Xva) for m in models], axis=0)` and use it for `evaluate`, for the `> best + 1e-5` early-stopping test, and for best-weight capture: `payload['model_state'] = [{key: copy.deepcopy(getattr(m, key)) for key in ('V','W','b')} for m in models]`, plus `payload['best_epoch'] = epoch`.
   - Extend the nonfinite guard to every replica's ('V','W','b','mV','vV','mW','vW') and store `payload['training_state'] = dict(epoch=epoch, best=best, bad=bad, rng=[r.bit_generator.state for r in rngs], latest=[copy.deepcopy(vars(m)) for m in models])`.
   - In the resume branch, restore `rngs[i].bit_generator.state` from the saved list, require `len(state['latest']) == N`, check `set(state['latest'][i]) == set(vars(models[i]))` and per-key shape/finiteness for each replica, restore each replica's attributes, and apply the existing epoch/bad/best/lr/l2/t validity checks using each replica's `lr`, `l2` and integer `t >= 1`. Raise clear errors on incompatibility; do not search other paths.

4. features.py and requirements.txt — unchanged. Splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, and test isolation are untouched; no test data is read. Expected wall clock is roughly 3x the 62 s parent (~200 s), far inside candidate_timeout_s=1800 and affordable within the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669326 | 0.536702 | 0.603014 | +0.000564 | 138 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 20 ++++++++++--------
 train.py  | 70 +++++++++++++++++++++++++++++++++++++++------------------------
 3 files changed, 57 insertions(+), 37 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 8dd5c0e..bfad404 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'n_models'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index f1627a2..1f8ab13 100644
--- a/model.py
+++ b/model.py
@@ -125,13 +125,15 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
-        weights = state['model_state']
-        for name in ('V', 'W', 'b'):
-            value = weights[name]
-            if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
-                raise ValueError('incompatible or nonfinite model weights: ' + name)
-            setattr(self.model, name, value)
+        weights_list = state['model_state']
+        self.models = [FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'],
+                           seed=config['seed'] + i) for i in range(len(weights_list))]
+        for model, weights in zip(self.models, weights_list):
+            for name in ('V', 'W', 'b'):
+                value = weights[name]
+                if np.shape(value) != np.shape(getattr(model, name)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite model weights: ' + name)
+                setattr(model, name, value)
 
     def predict(self, rows):
         """Return one finite real-valued score per row, preserving input order.
@@ -142,7 +144,9 @@ class Predictor:
         """
         if not len(rows):
             return np.empty(0, dtype=np.float32)
-        return self.model.predict(transform(rows, self.features))
+        X = transform(rows, self.features)
+        scores = np.mean([m.predict(X) for m in self.models], axis=0)
+        return scores.astype(np.float32)
 
 
 def load_predictor(checkpoint_path):
diff --git a/train.py b/train.py
index db7e313..a0a89ca 100644
--- a/train.py
+++ b/train.py
@@ -89,7 +89,8 @@ def save_checkpoint(path, payload):
 
 def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     config = resolve(overrides)
-    rng = np.random.default_rng(config['seed'])
+    N = config['n_models']
+    rngs = [np.random.default_rng(config['seed'] + 1000 + i) for i in range(N)]
     if Path(checkpoint_path).exists():
         payload = read_checkpoint(checkpoint_path)
         if payload['config'] != config or payload['context'] != context:
@@ -97,25 +98,33 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         Predictor(payload)  # Validate inference weights before resuming.
         features = payload['features_state']
         state = payload['training_state']
-        rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
-        if set(state['latest']) != set(vars(model)):
-            raise ValueError('incomplete optimizer/model state')
-        for key, value in state['latest'].items():
-            if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
-                raise ValueError('incompatible or nonfinite latest state: ' + key)
-            setattr(model, key, value)
+        if len(state['latest']) != N or len(state['rng']) != N:
+            raise ValueError('checkpoint replica count incompatible with config')
+        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i)
+                  for i in range(N)]
+        for i, r in enumerate(rngs):
+            r.bit_generator.state = state['rng'][i]
+        for i, model in enumerate(models):
+            latest = state['latest'][i]
+            if set(latest) != set(vars(model)):
+                raise ValueError('incomplete optimizer/model state')
+            for key, value in latest.items():
+                if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite latest state: ' + key)
+                setattr(model, key, value)
+            if (model.lr != config['lr'] or model.l2 != config['l2']
+                    or type(model.t) is not int or model.t < 1):
+                raise ValueError('invalid checkpoint training progress/settings')
         best, bad, epoch = state['best'], state['bad'], state['epoch']
         if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
                 or type(bad) is not int or not 0 <= bad <= config['patience']
-                or not np.isfinite(best) or not 0 <= best <= 1
-                or model.lr != config['lr'] or model.l2 != config['l2']
-                or type(model.t) is not int or model.t < 1):
+                or not np.isfinite(best) or not 0 <= best <= 1):
             raise ValueError('invalid checkpoint training progress/settings')
-        print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
+        print(f'resume: completed epoch={epoch}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i)
+                  for i in range(N)]
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -147,29 +156,36 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     pos_user = np.asarray(pos_user_list, dtype=np.int64)
     neg_flat = np.asarray(neg_flat_list, dtype=np.int64)
 
+    bs = config['bs']
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
         n_pairs = len(train_rows)
-        sel = rng.integers(0, len(pos_idx), n_pairs)
-        u = pos_user[sel]
-        off = (rng.random(n_pairs) * neg_count[u]).astype(np.int64)
-        neg = neg_flat[neg_start[u] + off]
-        pos_sel = pos_idx[sel]
-        bs = config['bs']
-        losses = [model.step_pair(Xtr[pos_sel[i:i + bs]], Xtr[neg[i:i + bs]])
-                  for i in range(0, n_pairs, bs)]
-        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
+        all_losses = []
+        for i, model in enumerate(models):
+            r = rngs[i]
+            sel = r.integers(0, len(pos_idx), n_pairs)
+            u = pos_user[sel]
+            off = (r.random(n_pairs) * neg_count[u]).astype(np.int64)
+            neg = neg_flat[neg_start[u] + off]
+            pos_sel = pos_idx[sel]
+            losses = [model.step_pair(Xtr[pos_sel[j:j + bs]], Xtr[neg[j:j + bs]])
+                      for j in range(0, n_pairs, bs)]
+            all_losses.extend(losses)
+        scores = np.mean([m.predict(Xva) for m in models], axis=0)
+        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], scores)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            payload['model_state'] = [{key: copy.deepcopy(getattr(m, key)) for key in ('V', 'W', 'b')}
+                                       for m in models]
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+        if not all(np.isfinite(getattr(m, key)).all() for m in models
+                   for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
-            rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
+            rng=[r.bit_generator.state for r in rngs], latest=[copy.deepcopy(vars(m)) for m in models])
         payload['validation'] = validation
         save_checkpoint(checkpoint_path, payload)
-        print(f'epoch={epoch} loss={np.mean(losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
+        print(f'epoch={epoch} loss={np.mean(all_losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
```

---

## Iteration 13: `node_013`

**Status** `success` · **Parent** `node_012` · **Commit** `8787fdaecba3`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature engineering — change the estimation scheme of the existing item-quality target statistics from strictly-prior-day to leave-one-day-out over the full training window). Hypothesis: the current prior tokens in features.py are built only from strictly earlier training dates, so a large share of training rows (every row on a video's/author's first active day, and all rows on the earliest dates) fall into the cold 'n' bucket, while every validation/inference row sees the full training history. That train/serve coverage mismatch under-trains exactly the weights (and their FM interactions with user_id, tab and duration bins) that carry item-quality signal at scoring time. Estimating each row's video/author long-view statistics from all training days except the row's own day (day-level out-of-fold, explicitly permitted by the leakage constraint and never using the row's own label or any validation/test label) should give near-full coverage and a training feature distribution that matches inference, improving within-user ordering. Distinction from the closest supplied prior attempts: node_004 introduced these prior features with strictly-prior lookups (this changes how they are estimated, not what fields exist), node_006 added user-conditioned prior stats (different key), and no sibling of the selected parent node_012 was supplied; the current source still uses strictly-prior cumulative lookups.

Edit features.py only (model.py, train.py, config.py, requirements.txt unchanged; keep fit(rows)/transform(rows, state) signatures, the 7 token fields, the vocab/offsets/dim machinery, the 10-bin duration quantiles, and the rule that transform never reads row[6]):

1. In fit, replace the cumulative-by-date history tables with, for each key field (video_id at index 2, author_id at index 3): (a) a totals dict key -> (cnt_total, pos_total) over all training rows, and (b) a per-day dict key -> {date_index: (cnt_day, pos_day)}. Also store date_map = {date: index} for the sorted unique training dates, and the global training long-view rate g. Store all of these (plain dicts/lists, picklable) in the returned state.
2. Replace the lookup helper with one that, given the tables, a key and a row date, returns cnt = cnt_total - cnt_day and pos = pos_total - pos_day when the row's date is a known training date (cnt_day/pos_day = 0 if the key has no rows that day), and the untouched totals when the date is not in date_map (i.e. validation/test dates after the training window). Return (0, 0) for unseen keys.
3. Keep the token construction otherwise identical: rv = (pos_v + 20*g)/(cnt_v + 20), ra = (pos_a + 50*g)/(cnt_a + 50); token 'n' when cnt == 0, else f"{bin}_{conf(cnt)}" with the same conf buckets ('a' 1-4, 'b' 5-19, 'c' 20-99, 'd' >=100) and 16 quantile bins whose interior edges are refit in fit from the new leave-one-day-out training rates (np.unique on np.quantile with np.linspace(0, 1, 16)[1:-1], empty array fallback when no usable rows).
4. Keep vocab fitting over the 7 tokens and transform's per-field vocab lookup with unseen-token -> len(vocab) exactly as supplied.

Splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, the pairwise-BPR loop, the 3-replica ensemble and the checkpoint payload stay unchanged; no test data is read. Expected wall clock is close to the parent's ~138 s, far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669510 | 0.537000 | 0.603255 | +0.000241 | 108 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 72 ++++++++++++++++++++++++++++++-------------------------------
 1 file changed, 35 insertions(+), 37 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 1735925..af2f602 100644
--- a/features.py
+++ b/features.py
@@ -28,40 +28,39 @@ from bisect import bisect_left
 import numpy as np
 
 
-def build_history(rows, key_idx, date_map):
-    tmp = {}
+def build_tables(rows, key_idx, date_map):
+    totals = {}
+    per_day = {}
     for r in rows:
         t = date_map[r[0]]
         k = r[key_idx]
-        d = tmp.setdefault(k, {})
+        pos = 1 if r[6] == 1 else 0
+        tot = totals.setdefault(k, [0, 0])
+        tot[0] += 1
+        tot[1] += pos
+        d = per_day.setdefault(k, {})
         e = d.setdefault(t, [0, 0])
         e[0] += 1
-        e[1] += 1 if r[6] == 1 else 0
-    history = {}
-    for k, d in tmp.items():
-        ts = sorted(d.keys())
-        cum_cnt = []
-        cum_pos = []
-        c = 0
-        p = 0
-        for t in ts:
-            c += d[t][0]
-            p += d[t][1]
-            cum_cnt.append(c)
-            cum_pos.append(p)
-        history[k] = (ts, cum_cnt, cum_pos)
-    return history
-
-
-def lookup(history, key, t):
-    entry = history.get(key)
-    if entry is None:
+        e[1] += pos
+    return totals, per_day
+
+
+def lookup(tables, key, date, date_map):
+    totals, per_day = tables
+    tot = totals.get(key)
+    if tot is None:
         return 0, 0
-    ts, cum_cnt, cum_pos = entry
-    j = bisect_left(ts, t)
-    if j > 0:
-        return cum_cnt[j - 1], cum_pos[j - 1]
-    return 0, 0
+    cnt_total, pos_total = tot
+    t = date_map.get(date)
+    if t is None:
+        return cnt_total, pos_total
+    cnt_day, pos_day = 0, 0
+    d = per_day.get(key)
+    if d is not None:
+        e = d.get(t)
+        if e is not None:
+            cnt_day, pos_day = e
+    return cnt_total - cnt_day, pos_total - pos_day
 
 
 def conf(c):
@@ -76,10 +75,9 @@ def conf(c):
 
 def tokens_for(row, state):
     dur_bin = str(int(np.searchsorted(state['edges'], row[5])))
-    t = bisect_left(state['dates'], row[0])
     g = state['g']
-    cnt_v, pos_v = lookup(state['video_hist'], row[2], t)
-    cnt_a, pos_a = lookup(state['author_hist'], row[3], t)
+    cnt_v, pos_v = lookup(state['video_tables'], row[2], row[0], state['date_map'])
+    cnt_a, pos_a = lookup(state['author_tables'], row[3], row[0], state['date_map'])
     if cnt_v == 0:
         tv = 'n'
     else:
@@ -97,18 +95,18 @@ def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
     dates = sorted(set(r[0] for r in rows))
     date_map = {d: i for i, d in enumerate(dates)}
-    video_hist = build_history(rows, 2, date_map)
-    author_hist = build_history(rows, 3, date_map)
+    video_tables = build_tables(rows, 2, date_map)
+    author_tables = build_tables(rows, 3, date_map)
     g = float(np.mean([1.0 if r[6] == 1 else 0.0 for r in rows])) if rows else 0.0
 
-    state = dict(dates=dates, video_hist=video_hist, author_hist=author_hist, g=g, edges=edges)
+    state = dict(dates=dates, date_map=date_map, video_tables=video_tables,
+                 author_tables=author_tables, g=g, edges=edges)
 
     rv_list = []
     ra_list = []
     for r in rows:
-        t = date_map[r[0]]
-        cnt_v, pos_v = lookup(video_hist, r[2], t)
-        cnt_a, pos_a = lookup(author_hist, r[3], t)
+        cnt_v, pos_v = lookup(video_tables, r[2], r[0], date_map)
+        cnt_a, pos_a = lookup(author_tables, r[3], r[0], date_map)
         if cnt_v > 0:
             rv_list.append((pos_v + 20 * g) / (cnt_v + 20))
         if cnt_a > 0:
```

---

## Iteration 14: `node_014`

**Status** `success` · **Parent** `node_013` · **Commit** `ac257a4617a2`

### Hypothesis

```text
SELECTED CHANGE
Experiment (FM backbone input contract + feature representation — give the factorization machine real-valued feature support and feed the item-quality/popularity/duration signals as continuous values instead of only as quantile buckets). Hypothesis: within-user GAUC/nDCG are driven by item-side quality signal, but the current pipeline exposes the leave-one-day-out video/author long-view rates only as 16-quantile x 4-confidence categorical tokens, discarding magnitude and forcing each bucket to learn its own embedding; a value-weighted FM lets a single 'video quality' embedding/weight carry the full-resolution prior and, through the second-order term, gives every user embedding a personalized sensitivity to item quality, exposure volume and video length. Distinction from the closest supplied prior attempts: node_004 and node_013 changed WHICH label statistics are computed and how they are estimated, both still emitting bucketed categorical tokens; node_001 (different, pointwise parent) added categorical popularity/duration buckets. No experiment in this lineage has changed the FM from pure index (implicit value 1.0) inputs to indexed real-valued inputs, and this adds continuous fields, not new buckets.

Implementation:

1. features.py — keep the existing leave-one-day-out totals/per-day tables, the `lookup`, `conf`, `tokens_for` helpers, the 10-bin duration quantiles, the 7 categorical tokens, the vocab/offsets machinery, and the rule that nothing outside `fit` reads row[6]. Add a `numeric_for(row, state)` helper that returns 4 raw floats computed from the same LOO lookups used by `tokens_for`: (a) `logit(rv) - logit(g)` where `rv = (pos_v + 20*g)/(cnt_v + 20)` (cnt_v==0 -> rv = g so the value is 0), (b) `logit(ra) - logit(g)` with `ra = (pos_a + 50*g)/(cnt_a + 50)`, (c) `log1p(cnt_v)`, (d) `log1p(max(row[5], 0))`; define `logit(p) = log(p/(1-p))` on `p` clipped to [1e-6, 1-1e-6]. In `fit`, after the rate edges are built, compute these 4 raw values over all training rows and store `num_mean` and `num_std` (std floored at 1e-6) in the state; `numeric_for` must return the standardized values clipped to [-5, 5]. Set `state['cat_dim'] = sum(dims)` (the current categorical dim) and `state['dim'] = cat_dim + 4`, and store `state['num_offsets'] = np.arange(cat_dim, cat_dim + 4, dtype=np.int32)`. Change `transform(rows, state)` to return a tuple `(idx, val)`: `idx` is int32 of shape (n, 11) whose first 7 columns are exactly today's categorical indices and whose last 4 columns are the constant `num_offsets`; `val` is float32 of shape (n, 11) with 1.0 in the first 7 columns and the standardized numeric values in the last 4.

2. model.py — make `FM` value-aware without adding any new instance attributes (train.py's `set(latest) == set(vars(model))` resume check must still hold). `logits(self, X, val)`: `E = self.V[X] * val[:, :, None]`, `S = E.sum(1)`, `inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))`, return `self.b + (self.W[X] * val).sum(1) + inter, E, S`. `predict(self, X, val, bs=200_000)` slices both arrays consistently. Rewrite `step_pair(self, Xp, Vp, Xn, Vn)` keeping the BPR loss, the unique-index compression, the sparse lazy Adam with b1=0.9, b2=0.999, eps=1e-8, the shared `self.t += 1` bias correction, and the decoupled multiplicative decay `* (1.0 - self.l2)`; only the scattered gradients change to include the value factor: `np.add.at(gW, loc_p, c[:, None] * Vp)`, `np.add.at(gW, loc_n, -c[:, None] * Vn)`, `np.add.at(gV, loc_p, c[:, None, None] * Vp[:, :, None] * (Sp[:, None, :] - Ep))`, `np.add.at(gV, loc_n, -c[:, None, None] * Vn[:, :, None] * (Sn[:, None, :] - En))` (Ep/En already carry the value scaling). Keep the returned loss `float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))` and do not update `self.b`. Delete the now-unused pointwise `step` method. In `Predictor.predict`, unpack `X, val = transform(rows, self.features)` and return `np.mean([m.predict(X, val) for m in self.models], axis=0).astype(np.float32)`; keep the empty-input behavior, the per-replica shape/finiteness validation, `read_checkpoint`, and `load_predictor(checkpoint_path)` unchanged.

3. train.py — keep the `train(train_rows, valid_rows, checkpoint_path, overrides, context)` signature, the 3-replica ensemble, the eligible-user pair construction, the activity-weighted uniform-negative sampling, early stopping on ensemble validation primary, the atomic checkpoint save, and the resume path. Only adapt to the new transform contract: `Xtr, Vtr = transform(train_rows, features)`, `Xva, Vva = transform(valid_rows, features)`, call `model.step_pair(Xtr[pos_sel[j:j+bs]], Vtr[pos_sel[j:j+bs]], Xtr[neg[j:j+bs]], Vtr[neg[j:j+bs]])`, and score with `np.mean([m.predict(Xva, Vva) for m in models], axis=0)`.

4. config.py and requirements.txt — unchanged (k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3).

Splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, and test isolation are untouched; no test data is read and no row's own label enters its features. Field count goes from 7 to 11, so expected wall clock is roughly 1.5x the parent's ~108 s (~170 s), far inside candidate_timeout_s=1800 and affordable within the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668908 | 0.536566 | 0.602737 | -0.000518 | 183 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 58 +++++++++++++++++++++++++++++++++++++++++++++++++++-------
 model.py    | 47 +++++++++++++++--------------------------------
 train.py    |  9 +++++----
 3 files changed, 71 insertions(+), 43 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index af2f602..aaff5c7 100644
--- a/features.py
+++ b/features.py
@@ -91,6 +91,30 @@ def tokens_for(row, state):
     return [row[1], row[2], row[3], row[4], dur_bin, tv, ta]
 
 
+def _numeric_raw(row, state):
+    g = state['g']
+
+    def logit(p):
+        p = min(max(p, 1e-6), 1 - 1e-6)
+        return np.log(p / (1 - p))
+
+    cnt_v, pos_v = lookup(state['video_tables'], row[2], row[0], state['date_map'])
+    cnt_a, pos_a = lookup(state['author_tables'], row[3], row[0], state['date_map'])
+    rv = g if cnt_v == 0 else (pos_v + 20 * g) / (cnt_v + 20)
+    ra = g if cnt_a == 0 else (pos_a + 50 * g) / (cnt_a + 50)
+    v1 = logit(rv) - logit(g)
+    v2 = logit(ra) - logit(g)
+    v3 = np.log1p(cnt_v)
+    v4 = np.log1p(max(row[5], 0))
+    return np.array([v1, v2, v3, v4], dtype=np.float64)
+
+
+def numeric_for(row, state):
+    vals = _numeric_raw(row, state)
+    vals = (vals - state['num_mean']) / state['num_std']
+    return np.clip(vals, -5, 5).astype(np.float32)
+
+
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
     dates = sorted(set(r[0] for r in rows))
@@ -124,6 +148,17 @@ def fit(rows):
     state['rv_edges'] = rv_edges
     state['ra_edges'] = ra_edges
 
+    raw_numeric = np.stack([_numeric_raw(row, state) for row in rows], axis=0) if rows \
+        else np.zeros((0, 4), dtype=np.float64)
+    if len(raw_numeric):
+        num_mean = raw_numeric.mean(axis=0)
+        num_std = np.maximum(raw_numeric.std(axis=0), 1e-6)
+    else:
+        num_mean = np.zeros(4, dtype=np.float64)
+        num_std = np.ones(4, dtype=np.float64)
+    state['num_mean'] = num_mean
+    state['num_std'] = num_std
+
     vocabs = [{} for _ in range(7)]
     for row in rows:
         for i, value in enumerate(tokens_for(row, state)):
@@ -132,14 +167,23 @@ def fit(rows):
     dims = [len(v) + 1 for v in vocabs]
     state['vocabs'] = vocabs
     state['offsets'] = np.cumsum([0] + dims[:-1]).astype(np.int32)
-    state['dim'] = sum(dims)
+    cat_dim = sum(dims)
+    state['cat_dim'] = cat_dim
+    state['dim'] = cat_dim + 4
+    state['num_offsets'] = np.arange(cat_dim, cat_dim + 4, dtype=np.int32)
     return state
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), len(state['vocabs'])), dtype=np.int32)
-    for n, row in enumerate(rows):
-        for i, value in enumerate(tokens_for(row, state)):
-            vocab = state['vocabs'][i]
-            result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
-    return result
+    n = len(rows)
+    idx = np.empty((n, 11), dtype=np.int32)
+    val = np.empty((n, 11), dtype=np.float32)
+    num_offsets = state['num_offsets']
+    for i, row in enumerate(rows):
+        for j, value in enumerate(tokens_for(row, state)):
+            vocab = state['vocabs'][j]
+            idx[i, j] = vocab.get(value, len(vocab)) + state['offsets'][j]
+        val[i, :7] = 1.0
+        idx[i, 7:] = num_offsets
+        val[i, 7:] = numeric_for(row, state)
+    return idx, val
diff --git a/model.py b/model.py
index 1f8ab13..85efbf7 100644
--- a/model.py
+++ b/model.py
@@ -42,35 +42,18 @@ class FM:
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
         self.t = 0
 
-    def logits(self, X):
-        E = self.V[X]                                   # (B,F,k)
+    def logits(self, X, val):
+        E = self.V[X] * val[:, :, None]                 # (B,F,k)
         S = E.sum(1)                                    # (B,k)
         inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
-
-    def step(self, X, y):
-        B = len(y)
-        z, E, S = self.logits(X)
-        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
-        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
-        np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
-        gV += self.l2 * self.V; gW += self.l2 * self.W
-        self.t += 1
-        b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M *= b1; M += (1 - b1) * G
-            Vv *= b2; Vv += (1 - b2) * (G * G)
-            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
-        self.b -= self.lr * g.sum()
-        return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
-
-    def step_pair(self, Xp, Xn):
+        return self.b + (self.W[X] * val).sum(1) + inter, E, S
+
+    def step_pair(self, Xp, Vp, Xn, Vn):
         # self.l2 is a decoupled per-touch multiplicative shrink factor, not
         # an added gradient penalty.
         B = len(Xp)
-        zp, Ep, Sp = self.logits(Xp)
-        zn, En, Sn = self.logits(Xn)
+        zp, Ep, Sp = self.logits(Xp, Vp)
+        zn, En, Sn = self.logits(Xn, Vn)
         d = zp - zn
         c = (-sigmoid(-d) / B).astype(np.float32)
 
@@ -81,10 +64,10 @@ class FM:
 
         gV = np.zeros((len(idx), self.V.shape[1]), np.float32)
         gW = np.zeros(len(idx), np.float32)
-        np.add.at(gW, loc_p, c[:, None])
-        np.add.at(gW, loc_n, -c[:, None])
-        np.add.at(gV, loc_p, c[:, None, None] * (Sp[:, None, :] - Ep))
-        np.add.at(gV, loc_n, -c[:, None, None] * (Sn[:, None, :] - En))
+        np.add.at(gW, loc_p, c[:, None] * Vp)
+        np.add.at(gW, loc_n, -c[:, None] * Vn)
+        np.add.at(gV, loc_p, c[:, None, None] * Vp[:, :, None] * (Sp[:, None, :] - Ep))
+        np.add.at(gV, loc_n, -c[:, None, None] * Vn[:, :, None] * (Sn[:, None, :] - En))
 
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
@@ -105,8 +88,8 @@ class FM:
 
         return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
 
-    def predict(self, X, bs=200_000):
-        return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
+    def predict(self, X, val, bs=200_000):
+        return np.concatenate([self.logits(X[i:i + bs], val[i:i + bs])[0] for i in range(0, len(X), bs)])
 
 def read_checkpoint(path):
     with open(path, 'rb') as stream:
@@ -144,8 +127,8 @@ class Predictor:
         """
         if not len(rows):
             return np.empty(0, dtype=np.float32)
-        X = transform(rows, self.features)
-        scores = np.mean([m.predict(X) for m in self.models], axis=0)
+        X, val = transform(rows, self.features)
+        scores = np.mean([m.predict(X, val) for m in self.models], axis=0)
         return scores.astype(np.float32)
 
 
diff --git a/train.py b/train.py
index a0a89ca..3be11dd 100644
--- a/train.py
+++ b/train.py
@@ -128,8 +128,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
-    Xtr = transform(train_rows, features)
-    Xva = transform(valid_rows, features)
+    Xtr, Vtr = transform(train_rows, features)
+    Xva, Vva = transform(valid_rows, features)
 
     users = {}
     for i, r in enumerate(train_rows):
@@ -169,10 +169,11 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             off = (r.random(n_pairs) * neg_count[u]).astype(np.int64)
             neg = neg_flat[neg_start[u] + off]
             pos_sel = pos_idx[sel]
-            losses = [model.step_pair(Xtr[pos_sel[j:j + bs]], Xtr[neg[j:j + bs]])
+            losses = [model.step_pair(Xtr[pos_sel[j:j + bs]], Vtr[pos_sel[j:j + bs]],
+                                       Xtr[neg[j:j + bs]], Vtr[neg[j:j + bs]])
                       for j in range(0, n_pairs, bs)]
             all_losses.extend(losses)
-        scores = np.mean([m.predict(Xva) for m in models], axis=0)
+        scores = np.mean([m.predict(Xva, Vva) for m in models], axis=0)
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], scores)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

---

## Iteration 15: `node_015`

**Status** `success` · **Parent** `node_013` · **Commit** `fa861d63ad4c`

### Hypothesis

```text
SELECTED CHANGE
Experiment (training-mechanics / temporal weight averaging — a subsystem never touched in this lineage): add bias-corrected exponential moving averaging (EMA) of each ensemble replica's FM weights across epoch boundaries, and use the averaged weights for validation scoring, early-stopping selection, and the saved inference checkpoint. Hypothesis: every recent improvement in this lineage is on the order of 0.0002–0.0006 Primary, and the 3-replica seed ensemble (node_012, +0.0006) was the largest single gain, which indicates that residual error is dominated by stochastic noise in the sparsely-updated embeddings (each mini-batch of 8192 sampled BPR pairs touches only a small slice of the user/video/author tables, so end-of-epoch weights are a noisy sample of the trajectory). Averaging the iterates in weight space over the last few epochs is a variance-reduction mechanism that is complementary to averaging scores across independently seeded replicas, and it costs essentially nothing per epoch. Distinction from the closest supplied prior attempts: node_012 averaged scores across seeds at inference (kept unchanged here), node_008 changed the per-step update rule (sparse lazy Adam + decoupled decay, kept unchanged here), and the only supplied sibling of this parent, node_014, changed the FM input contract to real-valued features (regressed, not repeated). No prior experiment averaged model weights over time.

Implementation:

1. config.py — add `ema=0.7` to DEFAULTS (keep k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3). In `resolve`, validate `ema` as a real number with `math.isfinite(config['ema'])` and `0 <= config['ema'] < 1`, raising `ValueError('invalid ema')` otherwise; leave the existing integer and lr/l2 checks unchanged so the value is serialized into the checkpoint config.

2. model.py — keep `sigmoid`, `step`, `step_pair` (its BPR math, unique-index compression, sparse lazy Adam and decoupled decay), `read_checkpoint`, `Predictor` and `load_predictor` exactly as supplied, and add no attributes outside `FM.__init__` so train.py's `set(latest) == set(vars(model))` resume check still holds:
   - In `FM.__init__`, after the existing buffers, create `self.eV = np.zeros_like(self.V)`, `self.eW = np.zeros_like(self.W)`, `self.et = 0`.
   - Give `logits` optional weight overrides: `def logits(self, X, V=None, W=None)` with `V = self.V if V is None else V`, `W = self.W if W is None else W`, and use those in the existing embedding/interaction math (`E = V[X]`, `S = E.sum(1)`, `inter = 0.5*((S**2).sum(1) - (E**2).sum((1,2)))`, `return self.b + W[X].sum(1) + inter, E, S`). `step_pair` keeps calling `self.logits(Xp)` / `self.logits(Xn)` with defaults, so its behavior is unchanged.
   - Give `predict` the same pass-through: `def predict(self, X, bs=200_000, V=None, W=None)` forwarding V and W to `logits`.
   - Add `def ema_update(self, decay)`: `self.et += 1; self.eV *= decay; self.eV += (1 - decay) * self.V; self.eW *= decay; self.eW += (1 - decay) * self.W` (keep float32).
   - Add `def ema_weights(self, decay)`: return `(self.V, self.W)` when `self.et == 0`, else the bias-corrected pair `(self.eV / (1 - decay ** self.et), self.eW / (1 - decay ** self.et))` cast to float32.

3. train.py — keep the `train(train_rows, valid_rows, checkpoint_path, overrides, context)` signature, the eligible-user pair construction, the activity-weighted uniform-negative sampling, `n_pairs = len(train_rows)`, the per-replica RNGs, patience-based early stopping, the atomic temp-file-then-`os.replace` save, and the resume path. Only change how epoch-end weights are aggregated and scored:
   - After a replica finishes its mini-batch `step_pair` loop for the epoch, call `model.ema_update(config['ema'])`.
   - Compute `ema_pairs = [m.ema_weights(config['ema']) for m in models]` and score validation with `scores = np.mean([m.predict(Xva, V=Vh, W=Wh) for m, (Vh, Wh) in zip(models, ema_pairs)], axis=0)`, then call `evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], scores)` exactly as now.
   - On improvement (`validation['primary'] > best + 1e-5`), store the EMA weights as the inference weights: `payload['model_state'] = [dict(V=np.asarray(Vh, dtype=np.float32).copy(), W=np.asarray(Wh, dtype=np.float32).copy(), b=copy.deepcopy(m.b)) for m, (Vh, Wh) in zip(models, ema_pairs)]`, plus `payload['best_epoch'] = epoch`, so `Predictor` (unchanged) serves the averaged model.
   - Extend the nonfinite guard key tuple to `('V','W','b','mV','vV','mW','vW','eV','eW')`.
   - Leave `payload['training_state']` as `dict(epoch=..., best=..., bad=..., rng=[...], latest=[copy.deepcopy(vars(m)) for m in models])`; because eV/eW/et are created in `FM.__init__`, the existing per-key shape/finiteness resume validation covers them automatically (add an optional `type(model.et) is not int or model.et < 0` check alongside the existing `model.t` check).

4. features.py and requirements.txt — unchanged. Frozen splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, and test isolation are untouched; no test data is read. Expected wall clock stays close to the parent's ~108 s (one dense O(dim×k) EMA blend per replica per epoch), far inside candidate_timeout_s=1800 and affordable within the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670143 | 0.537091 | 0.603617 | +0.000363 | 140 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 model.py  | 29 +++++++++++++++++++++++------
 train.py  | 15 ++++++++++-----
 3 files changed, 36 insertions(+), 12 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index bfad404..d7cce0c 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7)
 
 
 def resolve(overrides):
@@ -36,4 +36,6 @@ def resolve(overrides):
     for key in ('lr', 'l2'):
         if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
             raise ValueError(f'invalid {key}')
+    if not math.isfinite(config['ema']) or not (0 <= config['ema'] < 1):
+        raise ValueError('invalid ema')
     return config
diff --git a/model.py b/model.py
index 1f8ab13..f793463 100644
--- a/model.py
+++ b/model.py
@@ -41,12 +41,29 @@ class FM:
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
         self.t = 0
-
-    def logits(self, X):
-        E = self.V[X]                                   # (B,F,k)
+        self.eV = np.zeros_like(self.V)
+        self.eW = np.zeros_like(self.W)
+        self.et = 0
+
+    def logits(self, X, V=None, W=None):
+        V = self.V if V is None else V
+        W = self.W if W is None else W
+        E = V[X]                                   # (B,F,k)
         S = E.sum(1)                                    # (B,k)
         inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        return self.b + W[X].sum(1) + inter, E, S
+
+    def ema_update(self, decay):
+        self.et += 1
+        self.eV *= decay
+        self.eV += (1 - decay) * self.V
+        self.eW *= decay
+        self.eW += (1 - decay) * self.W
+
+    def ema_weights(self, decay):
+        if self.et == 0:
+            return self.V, self.W
+        return (self.eV / (1 - decay ** self.et)).astype(np.float32), (self.eW / (1 - decay ** self.et)).astype(np.float32)
 
     def step(self, X, y):
         B = len(y)
@@ -105,8 +122,8 @@ class FM:
 
         return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
 
-    def predict(self, X, bs=200_000):
-        return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
+    def predict(self, X, bs=200_000, V=None, W=None):
+        return np.concatenate([self.logits(X[i:i + bs], V=V, W=W)[0] for i in range(0, len(X), bs)])
 
 def read_checkpoint(path):
     with open(path, 'rb') as stream:
diff --git a/train.py b/train.py
index a0a89ca..8dd2506 100644
--- a/train.py
+++ b/train.py
@@ -113,7 +113,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
                     raise ValueError('incompatible or nonfinite latest state: ' + key)
                 setattr(model, key, value)
             if (model.lr != config['lr'] or model.l2 != config['l2']
-                    or type(model.t) is not int or model.t < 1):
+                    or type(model.t) is not int or model.t < 1
+                    or type(model.et) is not int or model.et < 0):
                 raise ValueError('invalid checkpoint training progress/settings')
         best, bad, epoch = state['best'], state['bad'], state['epoch']
         if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
@@ -172,17 +173,21 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             losses = [model.step_pair(Xtr[pos_sel[j:j + bs]], Xtr[neg[j:j + bs]])
                       for j in range(0, n_pairs, bs)]
             all_losses.extend(losses)
-        scores = np.mean([m.predict(Xva) for m in models], axis=0)
+            model.ema_update(config['ema'])
+        ema_pairs = [m.ema_weights(config['ema']) for m in models]
+        scores = np.mean([m.predict(Xva, V=Vh, W=Wh) for m, (Vh, Wh) in zip(models, ema_pairs)], axis=0)
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], scores)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = [{key: copy.deepcopy(getattr(m, key)) for key in ('V', 'W', 'b')}
-                                       for m in models]
+            payload['model_state'] = [dict(V=np.asarray(Vh, dtype=np.float32).copy(),
+                                            W=np.asarray(Wh, dtype=np.float32).copy(),
+                                            b=copy.deepcopy(m.b))
+                                       for m, (Vh, Wh) in zip(models, ema_pairs)]
             payload['best_epoch'] = epoch
         else:
             bad += 1
         if not all(np.isfinite(getattr(m, key)).all() for m in models
-                   for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+                   for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'eV', 'eW')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
             rng=[r.bit_generator.state for r in rngs], latest=[copy.deepcopy(vars(m)) for m in models])
```

---

## Iteration 16: `node_016`

**Status** `success` · **Parent** `node_015` · **Commit** `18c9b86bf043`

### Hypothesis

```text
SELECTED CHANGE
Experiment (input regularization / cold-start backoff -- a subsystem never touched in this lineage): add per-field categorical feature dropout to the pairwise-BPR training batches, replacing dropped field indices with each field's existing 'unseen token' slot, so that slot is actually trained as a learned backoff embedding. Keep the 3-replica ensemble, EMA weight averaging, sparse lazy Adam with decoupled decay, leave-one-day-out prior features, and all other hyperparameters exactly as supplied.

Hypothesis (grounded in the supplied code): features.transform maps any token missing from a fitted vocab to index `offsets[i] + len(vocabs[i])`, but under the current training loop that slot never receives a gradient, so every validation row containing an unseen user_id / video_id / author_id / prior token is scored with the untouched N(0, 0.01) initialization for V and 0 for W -- effectively noise inside per-user candidate groups. Randomly masking fields during training both (a) trains those backoff slots to a sensible average representation used at inference for cold users/videos/authors, and (b) reduces co-adaptation so item-quality priors, tab and duration must carry ranking signal when the sparse video/user embedding is unreliable. It also adds per-replica input noise, which should increase ensemble diversity on top of the existing seed/sampling diversity.

Implementation:

1. config.py -- add `drop=0.1` to DEFAULTS (keep k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7). In `resolve`, validate it as a real number with `math.isfinite(config['drop'])` and `0 <= config['drop'] < 1`, raising `ValueError('invalid drop')`; leave the existing integer, lr/l2 and ema checks unchanged so the value is serialized into the checkpoint config and enforced on resume.

2. train.py -- only change how each mini-batch's index matrices are built; keep the `train(train_rows, valid_rows, checkpoint_path, overrides, context)` signature, the eligible-user pair construction, the activity-weighted uniform-negative pair draw, `n_pairs = len(train_rows)`, per-replica RNGs, per-epoch `model.ema_update(config['ema'])`, EMA-scored validation, `evaluate(...)`, best-primary early stopping with patience, the nonfinite guard, the atomic temp-file-then-os.replace save, and the resume path exactly as supplied. After `Xtr = transform(train_rows, features)`, precompute the per-field backoff indices once: `unk = np.asarray([int(features['offsets'][i]) + len(features['vocabs'][i]) for i in range(Xtr.shape[1])], dtype=np.int32)`. Inside the per-replica mini-batch loop, build `Xp = Xtr[pos_sel[j:j + bs]]` and `Xn = Xtr[neg[j:j + bs]]`, and when `config['drop'] > 0` draw one shared mask per pair with the replica's own RNG, `mask = r.random(Xp.shape) < config['drop']`, then pass `np.where(mask, unk, Xp).astype(np.int32)` and `np.where(mask, unk, Xn).astype(np.int32)` to `model.step_pair`. Use the same mask for the positive and the negative row of a pair so the shared user field (and any commonly dropped field) stays consistent across the pair and the BPR difference remains a clean item-side comparison. Apply dropout to training batches only -- validation scoring (`m.predict(Xva, V=Vh, W=Wh)`) and the saved inference weights must use untouched, fully-featured inputs.

3. model.py, features.py, requirements.txt -- unchanged. Frozen splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, checkpoint payload structure and test isolation are untouched; no test data is read.

Distinction from prior attempts: no supplied lineage node or sibling has regularized or perturbed the model inputs -- earlier feature work changed which tokens exist (node_004 prior tokens, node_006 user-conditioned stats, node_013 leave-one-day-out estimation) or the input contract (node_014 real-valued features, regressed), while node_008 changed the update rule and node_012/node_015 changed prediction aggregation and temporal weight averaging. Runtime should stay near the parent's ~139 s (only extra RNG draws and two np.where per batch), far inside candidate_timeout_s=1800 and affordable within the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670004 | 0.536951 | 0.603477 | -0.000140 | 142 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 train.py  | 18 ++++++++++++++++--
 2 files changed, 19 insertions(+), 3 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index d7cce0c..51b83e6 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7, drop=0.1)
 
 
 def resolve(overrides):
@@ -38,4 +38,6 @@ def resolve(overrides):
             raise ValueError(f'invalid {key}')
     if not math.isfinite(config['ema']) or not (0 <= config['ema'] < 1):
         raise ValueError('invalid ema')
+    if not math.isfinite(config['drop']) or not (0 <= config['drop'] < 1):
+        raise ValueError('invalid drop')
     return config
diff --git a/train.py b/train.py
index 8dd2506..2dd653a 100644
--- a/train.py
+++ b/train.py
@@ -131,6 +131,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print('fresh training', flush=True)
     Xtr = transform(train_rows, features)
     Xva = transform(valid_rows, features)
+    unk = np.asarray([int(features['offsets'][i]) + len(features['vocabs'][i]) for i in range(Xtr.shape[1])],
+                      dtype=np.int32)
 
     users = {}
     for i, r in enumerate(train_rows):
@@ -170,8 +172,20 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             off = (r.random(n_pairs) * neg_count[u]).astype(np.int64)
             neg = neg_flat[neg_start[u] + off]
             pos_sel = pos_idx[sel]
-            losses = [model.step_pair(Xtr[pos_sel[j:j + bs]], Xtr[neg[j:j + bs]])
-                      for j in range(0, n_pairs, bs)]
+
+            def build(j):
+                Xp = Xtr[pos_sel[j:j + bs]]
+                Xn = Xtr[neg[j:j + bs]]
+                if config['drop'] > 0:
+                    mask = r.random(Xp.shape) < config['drop']
+                    Xp = np.where(mask, unk, Xp).astype(np.int32)
+                    Xn = np.where(mask, unk, Xn).astype(np.int32)
+                return Xp, Xn
+
+            losses = []
+            for j in range(0, n_pairs, bs):
+                Xp, Xn = build(j)
+                losses.append(model.step_pair(Xp, Xn))
             all_losses.extend(losses)
             model.ema_update(config['ema'])
         ema_pairs = [m.ema_weights(config['ema']) for m in models]
```

---

## Iteration 17: `node_017`

**Status** `success` · **Parent** `node_015` · **Commit** `f06fc8a17657`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss formulation — hybrid pairwise+pointwise multi-objective training that finally uses the currently discarded single-class users): keep everything in the selected parent (3-replica seed ensemble, EMA weight averaging with ema=0.7, sparse lazy Adam with decoupled decay, leave-one-day-out prior-token features, activity-weighted uniform-negative BPR pair sampling) and add a weighted pointwise binary-cross-entropy term computed on ALL training rows into the same sparse update as the BPR term.

Hypothesis (grounded in the supplied code): train.py builds pairs only from `eligible` users that have both a positive and a negative training row, so every row belonging to a single-class user is never used for any gradient — those users' `user_id` embeddings stay at their N(0,0.01) initialization and their impressions contribute nothing to the video/author/prior-token embeddings. At validation time those same users are scored with untrained user vectors, injecting pure noise into their per-user ordering (GAUC averages over user groups, so these users are weighted equally with well-trained ones). A pointwise BCE term over all training rows gives those rows and users real gradients and adds extra supervision for sparse videos/authors, while the dominant BPR term keeps the objective ranking-oriented. Because the two terms are summed into ONE gradient before a single lazy Adam step, the mixing weight actually controls their relative influence (separate alternating batches would not, since Adam normalizes each step).

Implementation:

1. config.py — add `aux=0.5` to DEFAULTS (keep k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7). In `resolve`, validate it with `math.isfinite(config['aux'])` and `0 <= config['aux'] <= 10`, raising `ValueError('invalid aux')`; leave all existing checks unchanged so the value is serialized into the checkpoint config and enforced on resume.

2. model.py — change only `FM.step_pair`, extending its signature to `def step_pair(self, Xp, Xn, Xa=None, ya=None, alpha=0.0)` (default arguments keep the current call contract). Keep the existing BPR math (`zp, Ep, Sp = self.logits(Xp)`, `zn, En, Sn = self.logits(Xn)`, `d = zp - zn`, `B = len(Xp)`, `c = (-sigmoid(-d) / B).astype(np.float32)`), the unique-index compression, the compact `gV`/`gW` scatter, the single lazy Adam update over the touched rows with b1=0.9, b2=0.999, eps=1e-8, `self.t += 1`, and the decoupled multiplicative shrink `* (1.0 - self.l2)` exactly as supplied. When `Xa is not None and alpha > 0`: compute `za, Ea, Sa = self.logits(Xa)`, `ca = (alpha * (sigmoid(za) - ya) / len(ya)).astype(np.float32)`; include `Xa.ravel()` in the `np.concatenate` fed to `np.unique(..., return_inverse=True)` and slice out `loc_a` alongside `loc_p`/`loc_n`; add `np.add.at(gW, loc_a, ca[:, None])` and `np.add.at(gV, loc_a, ca[:, None, None] * (Sa[:, None, :] - Ea))` before the Adam block; and update the global bias with `self.b = np.float32(self.b - self.lr * float(ca.sum()))` (a constant shift, harmless for within-user ranking, but it keeps the BCE term well posed). Keep returning the BPR loss `float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))` so logging semantics are unchanged. Add no new instance attributes (so train.py's `set(latest) == set(vars(model))` resume check still holds) and leave `logits`, `predict`, `step`, `ema_update`, `ema_weights`, `read_checkpoint`, `Predictor`, and `load_predictor` untouched.

3. train.py — keep the `train(train_rows, valid_rows, checkpoint_path, overrides, context)` signature, the eligible-user pair construction and its ValueError guard, the per-replica RNGs, `n_pairs = len(train_rows)`, the pair draw, per-epoch `model.ema_update(config['ema'])`, EMA-weighted ensemble validation scoring, `evaluate(...)`, best-primary early stopping with patience, the nonfinite guard over ('V','W','b','mV','vV','mW','vW','eV','eW'), the atomic temp-file-then-os.replace save, and the resume path exactly as supplied. Only add the auxiliary stream: after `Xtr = transform(train_rows, features)`, build `ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)` (all training rows, including those of users excluded from pair sampling). Inside the per-replica epoch loop, after drawing `pos_sel`/`neg` with that replica's RNG `r`, also draw `aux_order = r.permutation(len(train_rows))`, and call `model.step_pair(Xtr[pos_sel[j:j + bs]], Xtr[neg[j:j + bs]], Xtr[aux_order[j:j + bs]], ytr[aux_order[j:j + bs]], config['aux'])` for each mini-batch (the last partial slices may differ in length; that is fine because the two streams are scattered independently).

4. features.py and requirements.txt — unchanged. Frozen splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, checkpoint payload structure and test isolation are untouched; only training-row labels are used, never validation or test labels.

Distinction from the closest supplied prior attempts: node_002 replaced pointwise BCE with pairwise BPR (this does not revert it — BPR remains the primary term and the pointwise term is a weighted addition inside the same sparse lazy-Adam gradient, over the full training set rather than only eligible users); node_005 tried listwise sampled softmax and node_010/node_011 changed negative/positive sampling, all from different parents; the only supplied sibling of this parent, node_016, regularized inputs with feature dropout. No supplied experiment has combined two loss terms or trained on the single-class users' rows.

Expected wall clock is roughly 1.4x the parent's ~139 s (~195 s, one extra forward/scatter of bs rows per batch, no extra optimizer pass), far inside candidate_timeout_s=1800 and affordable within the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668797 | 0.535873 | 0.602335 | -0.001283 | 185 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 model.py  | 27 ++++++++++++++++++++++-----
 train.py  |  5 ++++-
 3 files changed, 29 insertions(+), 7 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index d7cce0c..ae15d1f 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7, aux=0.5)
 
 
 def resolve(overrides):
@@ -38,4 +38,6 @@ def resolve(overrides):
             raise ValueError(f'invalid {key}')
     if not math.isfinite(config['ema']) or not (0 <= config['ema'] < 1):
         raise ValueError('invalid ema')
+    if not math.isfinite(config['aux']) or not (0 <= config['aux'] <= 10):
+        raise ValueError('invalid aux')
     return config
diff --git a/model.py b/model.py
index f793463..e979ab8 100644
--- a/model.py
+++ b/model.py
@@ -82,7 +82,7 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
-    def step_pair(self, Xp, Xn):
+    def step_pair(self, Xp, Xn, Xa=None, ya=None, alpha=0.0):
         # self.l2 is a decoupled per-touch multiplicative shrink factor, not
         # an added gradient penalty.
         B = len(Xp)
@@ -91,10 +91,20 @@ class FM:
         d = zp - zn
         c = (-sigmoid(-d) / B).astype(np.float32)
 
-        flat = np.concatenate((Xp.ravel(), Xn.ravel()))
-        idx, inv = np.unique(flat, return_inverse=True)
-        loc_p = inv[:Xp.size].reshape(Xp.shape)
-        loc_n = inv[Xp.size:].reshape(Xn.shape)
+        use_aux = Xa is not None and alpha > 0
+        if use_aux:
+            za, Ea, Sa = self.logits(Xa)
+            ca = (alpha * (sigmoid(za) - ya) / len(ya)).astype(np.float32)
+            flat = np.concatenate((Xp.ravel(), Xn.ravel(), Xa.ravel()))
+            idx, inv = np.unique(flat, return_inverse=True)
+            loc_p = inv[:Xp.size].reshape(Xp.shape)
+            loc_n = inv[Xp.size:Xp.size + Xn.size].reshape(Xn.shape)
+            loc_a = inv[Xp.size + Xn.size:].reshape(Xa.shape)
+        else:
+            flat = np.concatenate((Xp.ravel(), Xn.ravel()))
+            idx, inv = np.unique(flat, return_inverse=True)
+            loc_p = inv[:Xp.size].reshape(Xp.shape)
+            loc_n = inv[Xp.size:].reshape(Xn.shape)
 
         gV = np.zeros((len(idx), self.V.shape[1]), np.float32)
         gW = np.zeros(len(idx), np.float32)
@@ -103,6 +113,10 @@ class FM:
         np.add.at(gV, loc_p, c[:, None, None] * (Sp[:, None, :] - Ep))
         np.add.at(gV, loc_n, -c[:, None, None] * (Sn[:, None, :] - En))
 
+        if use_aux:
+            np.add.at(gW, loc_a, ca[:, None])
+            np.add.at(gV, loc_a, ca[:, None, None] * (Sa[:, None, :] - Ea))
+
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
 
@@ -120,6 +134,9 @@ class FM:
         self.W[idx] = self.W[idx] * (1.0 - self.l2) - self.lr * (mW_i / (1 - b1 ** self.t)) / (
             np.sqrt(vW_i / (1 - b2 ** self.t)) + eps)
 
+        if use_aux:
+            self.b = np.float32(self.b - self.lr * float(ca.sum()))
+
         return float(np.mean(np.log1p(np.exp(-np.clip(d, -30, 30)))))
 
     def predict(self, X, bs=200_000, V=None, W=None):
diff --git a/train.py b/train.py
index 8dd2506..231f9c0 100644
--- a/train.py
+++ b/train.py
@@ -131,6 +131,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print('fresh training', flush=True)
     Xtr = transform(train_rows, features)
     Xva = transform(valid_rows, features)
+    ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
 
     users = {}
     for i, r in enumerate(train_rows):
@@ -170,7 +171,9 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             off = (r.random(n_pairs) * neg_count[u]).astype(np.int64)
             neg = neg_flat[neg_start[u] + off]
             pos_sel = pos_idx[sel]
-            losses = [model.step_pair(Xtr[pos_sel[j:j + bs]], Xtr[neg[j:j + bs]])
+            aux_order = r.permutation(len(train_rows))
+            losses = [model.step_pair(Xtr[pos_sel[j:j + bs]], Xtr[neg[j:j + bs]],
+                                       Xtr[aux_order[j:j + bs]], ytr[aux_order[j:j + bs]], config['aux'])
                       for j in range(0, n_pairs, bs)]
             all_losses.extend(losses)
             model.ema_update(config['ema'])
```

---

## Iteration 18: `node_018`

**Status** `success` · **Parent** `node_015` · **Commit** `980575cdd3b8`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model backbone capacity — the FM hyperparameter subsystem, never varied anywhere in this lineage): raise the factorization embedding dimension from k=16 to k=32, changing nothing else.

Hypothesis: every recent gain in this lineage has come from variance reduction (3-seed ensemble, EMA weight averaging) or from feature/estimation refinements, all on a backbone whose interaction rank has been fixed at k=16 since genesis. GAUC and nDCG@5 are driven purely by the within-user item ordering, which in this model comes from the pairwise interactions between the user embedding and the item-side fields (video_id, author_id, tab, duration bin, video prior token, author prior token). With 7 fields and 21 field pairs, a rank-16 factorization may be the binding capacity limit on how much distinct per-user taste structure can be represented. The parent already carries three regularizers that make a capacity increase safe to test now (decoupled multiplicative decay l2=1e-4 applied only to touched rows, bias-corrected EMA weight averaging with ema=0.7, and score averaging over 3 independently seeded replicas), so doubling k is more likely to add usable interaction detail than to simply overfit the sparse ID embeddings.

Implementation:

1. config.py — change `k` in DEFAULTS from 16 to 32. Keep lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7 unchanged, and leave `resolve` exactly as supplied (k is already validated as an int >= 1 and serialized into the checkpoint config, so a fresh candidate checkpoint is created and any incompatible checkpoint still fails loudly).

2. model.py, train.py, features.py, requirements.txt — unchanged. `FM.__init__` already sizes V/mV/vV/eV from the `k` argument, `Predictor` already rebuilds replicas with `config['k']`, and train.py already passes `k=config['k']`, so no code edits are required for the new dimension to propagate to training, EMA averaging, checkpointing, and inference.

Frozen splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, the train.train and model.load_predictor contracts, and test isolation are untouched; no test data is read.

Distinction from prior attempts: no supplied lineage node or sibling has ever changed k (or any FM capacity/learning hyperparameter on its own) — node_002 changed the loss, node_004/node_013 the features, node_008 the update rule (and repurposed l2), node_012 prediction aggregation, node_015 temporal weight averaging, and the two supplied siblings of this parent changed input dropout (node_016) and added a pointwise auxiliary term (node_017). Expected wall clock is roughly 1.6–2x the parent's ~139 s (embedding gather, scatter, lazy-Adam and EMA work all scale with k), i.e. about 220–300 s and bounded well under candidate_timeout_s=1800 by the existing patience=4 early stopping.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669431 | 0.536873 | 0.603152 | -0.000465 | 180 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

```diff
diff --git a/config.py b/config.py
index d7cce0c..7e684d9 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7)
+DEFAULTS = dict(k=32, lr=0.001, l2=1e-4, epochs=60, bs=8192, patience=4, seed=0, n_models=3, ema=0.7)
 
 
 def resolve(overrides):
```

---

## Iteration 19: `node_019`

**Status** `success` · **Parent** `node_015` · **Commit** `cb463c0e4849`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature engineering — add a user-side leave-one-day-out behavioral backoff token, so sparse/cold users get a shared, well-trained representation that interacts with the item-side fields). Hypothesis: within-user GAUC/nDCG ordering currently depends on the user_id embedding to modulate the item-side fields, but users with few training impressions have essentially untrained user vectors, so their candidate ordering is driven by noise plus the global item priors. Adding one categorical field that encodes the user's own long-view propensity level and exposure confidence gives every user (including unseen ones, via the shared 'n'/backoff bucket) a dense, frequently-updated embedding whose FM interactions with video_id, author_id, tab, duration bin and the video/author prior tokens supply generalizable per-user taste signal. This targets the same cold-user weakness the failed input-dropout sibling (node_016) attacked at the optimizer/input level, but does it by adding shared structure instead of perturbing inputs.

Edit features.py only (model.py, train.py, config.py, requirements.txt unchanged; keep the fit(rows)/transform(rows, state) signatures, the vocab/offsets/dim machinery, the 10-bin duration quantiles, the existing 7 tokens, and the rule that tokens_for/transform never read row[6]):

1. In fit, build a third statistics table with the existing helper, `user_tables = build_tables(rows, 1, date_map)` (key = user_id at row index 1), and store it in the returned state as `state['user_tables']`, using exactly the same leave-one-day-out semantics as the existing video/author tables: `lookup(state['user_tables'], row[1], row[0], state['date_map'])` returns (cnt_total - cnt_on_that_day, pos_total - pos_on_that_day) for training dates, the untouched totals for dates outside date_map (validation/inference), and (0, 0) for unseen users. No validation or test labels are ever used.
2. In fit, after the video/author rate edges, compute a training rate list `ru_list` over all training rows with cnt_u > 0 using smoothing weight 10: `ru = (pos_u + 10 * g) / (cnt_u + 10)`, and store `state['ru_edges'] = np.unique(np.quantile(ru_list, np.linspace(0, 1, 16)[1:-1]))` (empty np.array([]) fallback when ru_list is empty), so ru_edges exists in the state before the vocabulary-fitting loop runs.
3. In tokens_for, append an eighth token: look up (cnt_u, pos_u) for row[1]; emit 'n' when cnt_u == 0, else f"{int(np.searchsorted(state['ru_edges'], ru))}_{conf(cnt_u)}" with ru = (pos_u + 10 * g) / (cnt_u + 10) and the existing conf() buckets ('a' 1-4, 'b' 5-19, 'c' 20-99, 'd' >=100). The returned list becomes [user_id, video_id, author_id, tab, duration_bin, video_prior, author_prior, user_prior].
4. Change the vocabulary construction in fit to `vocabs = [{} for _ in range(8)]`; transform is already generic over `len(state['vocabs'])` and needs no change, and FM.logits/step_pair/predict already handle an arbitrary field count F, so no other file requires edits.

Distinction from the closest supplied prior attempts: the parent's siblings changed input dropout (node_016), added a pointwise auxiliary loss term (node_017) and raised k to 32 (node_018), all of which regressed; node_004 introduced the video/author prior tokens and node_013 changed how those two item-side tables are estimated — none of them added a user-keyed statistic to this lineage's code state. The other-branch node_006 (user-conditioned prior stats keyed on user×item-side combinations, never adopted) is a different construction and was evaluated on a baseline without leave-one-day-out estimation, the 3-replica ensemble, or EMA averaging.

Frozen splits, the long_view target, per-user ranking groups, GAUC/nDCG@5 evaluation, the checkpoint payload, the train.train and model.load_predictor contracts, and test isolation are untouched; no test data is read. Expected wall clock is roughly 1.15x the parent's ~139 s (one extra field in the gather/scatter and one extra dict lookup per row in transform), i.e. about 155-170 s, inside the remaining budget and far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670251 | 0.536986 | 0.603619 | +0.000001 | 117 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 22 +++++++++++++++++++---
 1 file changed, 19 insertions(+), 3 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index af2f602..d7c9d26 100644
--- a/features.py
+++ b/features.py
@@ -78,6 +78,7 @@ def tokens_for(row, state):
     g = state['g']
     cnt_v, pos_v = lookup(state['video_tables'], row[2], row[0], state['date_map'])
     cnt_a, pos_a = lookup(state['author_tables'], row[3], row[0], state['date_map'])
+    cnt_u, pos_u = lookup(state['user_tables'], row[1], row[0], state['date_map'])
     if cnt_v == 0:
         tv = 'n'
     else:
@@ -88,7 +89,12 @@ def tokens_for(row, state):
     else:
         ra = (pos_a + 50 * g) / (cnt_a + 50)
         ta = f"{int(np.searchsorted(state['ra_edges'], ra))}_{conf(cnt_a)}"
-    return [row[1], row[2], row[3], row[4], dur_bin, tv, ta]
+    if cnt_u == 0:
+        tu = 'n'
+    else:
+        ru = (pos_u + 10 * g) / (cnt_u + 10)
+        tu = f"{int(np.searchsorted(state['ru_edges'], ru))}_{conf(cnt_u)}"
+    return [row[1], row[2], row[3], row[4], dur_bin, tv, ta, tu]
 
 
 def fit(rows):
@@ -97,20 +103,25 @@ def fit(rows):
     date_map = {d: i for i, d in enumerate(dates)}
     video_tables = build_tables(rows, 2, date_map)
     author_tables = build_tables(rows, 3, date_map)
+    user_tables = build_tables(rows, 1, date_map)
     g = float(np.mean([1.0 if r[6] == 1 else 0.0 for r in rows])) if rows else 0.0
 
     state = dict(dates=dates, date_map=date_map, video_tables=video_tables,
-                 author_tables=author_tables, g=g, edges=edges)
+                 author_tables=author_tables, user_tables=user_tables, g=g, edges=edges)
 
     rv_list = []
     ra_list = []
+    ru_list = []
     for r in rows:
         cnt_v, pos_v = lookup(video_tables, r[2], r[0], date_map)
         cnt_a, pos_a = lookup(author_tables, r[3], r[0], date_map)
+        cnt_u, pos_u = lookup(user_tables, r[1], r[0], date_map)
         if cnt_v > 0:
             rv_list.append((pos_v + 20 * g) / (cnt_v + 20))
         if cnt_a > 0:
             ra_list.append((pos_a + 50 * g) / (cnt_a + 50))
+        if cnt_u > 0:
+            ru_list.append((pos_u + 10 * g) / (cnt_u + 10))
 
     if rv_list:
         rv_edges = np.unique(np.quantile(rv_list, np.linspace(0, 1, 16)[1:-1]))
@@ -120,11 +131,16 @@ def fit(rows):
         ra_edges = np.unique(np.quantile(ra_list, np.linspace(0, 1, 16)[1:-1]))
     else:
         ra_edges = np.array([])
+    if ru_list:
+        ru_edges = np.unique(np.quantile(ru_list, np.linspace(0, 1, 16)[1:-1]))
+    else:
+        ru_edges = np.array([])
 
     state['rv_edges'] = rv_edges
     state['ra_edges'] = ra_edges
+    state['ru_edges'] = ru_edges
 
-    vocabs = [{} for _ in range(7)]
+    vocabs = [{} for _ in range(8)]
     for row in rows:
         for i, value in enumerate(tokens_for(row, state)):
             if value not in vocabs[i]:
```

