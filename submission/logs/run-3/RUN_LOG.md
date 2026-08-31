# Run log: run-3

Run id `af0ec7d596834b579014e266d1ef4d98` · evaluation protocol `cfe7881824a34480…` · schema 1

## Summary

| | |
|---|---|
| Candidate iterations | 16 of 50 permitted |
| Candidate outcomes | 16 success |
| Stop reason | `stagnation` |
| Baseline (`genesis`) | Primary 0.601469 |
| Selected (`node_011`) | Primary 0.604793 |
| Validation gain | +0.003324 |
| **Held-out test** | GAUC 0.664867 · nDCG@5 0.530850 · **Primary 0.597859** |
| Test coverage | 23,875 users · 170,588 rows |
| Model calls | 42 |
| Provider-reported tokens | 760,268 |
| Agent wall clock | 55.4 min |
| GPU hours | 0 (CPU only) |

## Manual interventions

**0** operator intervention(s) during this run.

Interventions are counted from the run's own event log: a provider or infrastructure failure pauses the run and records `run.failed`, and further orchestrator activity in the same log means an operator resumed it. Every intervention above is a resume of an unmodified run.

No manual edits were made to candidate code: every commit in the candidate workspace is authored by the agent identity (ML Loop <ml-loop@localhost>). Hypotheses, diffs, parent selection, and stopping were produced by the agent without human editing.

### Provider transport failures (1)

| Time (UTC) | Error | HTTP | Candidate | Attempt |
|---|---|---|---|---|
| 20:37:06 | `Timeout` | 408 | node_006 | 1 |

Transport failures are retried inside the client and do not count as experimental evidence. Only an exhausted retry budget pauses the run.

## Iteration index

| # | Candidate | GAUC | nDCG@5 | Primary | vs parent | Status | Repairs |
|---|---|---|---|---|---|---|---|
| baseline | `genesis` | 0.667133 | 0.535805 | 0.601469 | - | success | 0 |
| 1 | `node_001` | 0.670057 | 0.537139 | 0.603598 | +0.002129 | success | 0 |
| 2 | `node_002` | 0.665044 | 0.533567 | 0.599305 | -0.004293 | success | 0 |
| 3 | `node_003` | 0.668457 | 0.535410 | 0.601933 | -0.001665 | success | 0 |
| 4 | `node_004` | 0.666766 | 0.534868 | 0.600817 | -0.002781 | success | 0 |
| 5 | `node_005` | 0.669846 | 0.537040 | 0.603443 | -0.000155 | success | 0 |
| 6 | `node_006` | 0.669700 | 0.537009 | 0.603355 | -0.000243 | success | 0 |
| 7 | `node_007` | 0.665424 | 0.535459 | 0.600441 | -0.001027 | success | 0 |
| 8 | `node_008` | 0.671470 | 0.537678 | 0.604574 | +0.004132 | success | 0 |
| 9 | `node_009` | 0.668137 | 0.536289 | 0.602213 | -0.002361 | success | 0 |
| 10 | `node_010` | 0.670462 | 0.536947 | 0.603704 | -0.000869 | success | 0 |
| 11 | `node_011` | 0.671678 | 0.537908 | 0.604793 | +0.000219 | success | 0 |
| 12 | `node_012` | 0.669565 | 0.536819 | 0.603192 | -0.001601 | success | 0 |
| 13 | `node_013` | 0.669645 | 0.536744 | 0.603195 | -0.001598 | success | 0 |
| 14 | `node_014` | 0.669647 | 0.536898 | 0.603272 | -0.001520 | success | 0 |
| 15 | `node_015` | 0.670451 | 0.537342 | 0.603896 | -0.000896 | success | 0 |
| 16 | `node_016` | 0.671775 | 0.537556 | 0.604665 | -0.000127 | success | 0 |

---

## Baseline: `genesis`

**Status** `success` · **Parent** `none` · **Commit** `07e083848466`

### Hypothesis

Supplied reference pipeline. No agent hypothesis; this is the baseline every candidate is measured against.

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667133 | 0.535805 | 0.601469 | - | 37 s |

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

**Status** `success` · **Parent** `genesis` · **Commit** `88898ddb164d`

### Hypothesis

```text
SELECTED CHANGE
Change the training objective in train.py/model.py (with a small config.py addition) from pointwise sigmoid cross-entropy to an in-user pairwise BPR ranking loss, keeping the existing FM backbone, the 5-field encoding in features.py, the frozen splits/long_view target, and the existing validation-driven early stopping unchanged. Hypothesis: the evaluation metrics (GAUC and nDCG@5) are computed within user groups, so directly optimizing within-user score differences should align training with the metric better than globally calibrated pointwise logloss. Distinction from supplied prior attempts: no sibling experiments exist from this genesis parent, and the only related memory entry is a multi-negative sampled-softmax listwise loss that replaced an already-present BPR loss on a different (FFM, 9-field) code state; here the parent is plain pointwise FM, so introducing single-pair BPR is a new transfer experiment, not a repeat.

Implementation behavior:
- model.py: keep FM.logits, FM.predict, FM.step, Predictor, read_checkpoint, and load_predictor contracts intact (Predictor must still restore V, W, b exactly as now). Add a method FM.step_pairwise(Xp, Xn) that computes z_p, E_p, S_p and z_n, E_n, S_n via self.logits, forms d = z_p - z_n, uses loss = -log(sigmoid(d)) averaged over the batch, and gradient factor g = -sigmoid(-d)/B applied with +g to the positive rows and -g to the negative rows. Accumulate into gW via np.add.at(gW, Xp, g[:, None]) and np.add.at(gW, Xn, -g[:, None]), and into gV via np.add.at(gV, Xp, g[:, None, None] * (S_p[:, None, :] - E_p)) and np.add.at(gV, Xn, -g[:, None, None] * (S_n[:, None, :] - E_n)); add self.l2 * V and self.l2 * W, then apply the same Adam update (b1=0.9, b2=0.999, eps=1e-8, self.t increment) already used in FM.step. The global bias self.b cancels in the pairwise difference and must be left unchanged. Return the mean pairwise loss as a float. Keep vars(model) keys identical so the existing checkpoint 'latest' state validation in train.py still works.
- train.py: after transform, group training row indices by user_id (r[1]) and split each user's indices into positives (label 1) and negatives (label 0) using the training labels only. Keep only users that have at least one positive and at least one negative. Each epoch, for every positive index of such users, sample neg_per_pos negative indices uniformly at random from the same user's negative pool using the existing seeded rng, build the paired index arrays, shuffle the pair order with rng.permutation, and iterate in minibatches of config['bs'] pairs calling model.step_pairwise(Xtr[pos_idx_batch], Xtr[neg_idx_batch]). Log the mean pairwise loss per epoch. If no user qualifies (degenerate data), fall back to the existing pointwise model.step loop so the run cannot crash. Leave validation (evaluate on valid_rows), best-primary selection, payload contents, atomic save_checkpoint, and resume logic exactly as they are.
- config.py: add DEFAULTS key neg_per_pos=2 and validate it in the existing integer loop (int, >= 1); leave k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0 unchanged so the comparison against the genesis baseline is controlled.
Expected cost is roughly 2-3x the 37s baseline per run, far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670057 | 0.537139 | 0.603598 | +0.002129 | 39 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 20 ++++++++++++++++++++
 train.py  | 35 ++++++++++++++++++++++++++++++++---
 3 files changed, 54 insertions(+), 5 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 147c6ac..3b1b451 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'neg_per_pos'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 495d48e..23fdaa1 100644
--- a/model.py
+++ b/model.py
@@ -65,6 +65,26 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
+    def step_pairwise(self, Xp, Xn):
+        B = len(Xp)
+        z_p, E_p, S_p = self.logits(Xp)
+        z_n, E_n, S_n = self.logits(Xn)
+        d = z_p - z_n
+        g = (-sigmoid(-d) / B).astype(np.float32)
+        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        np.add.at(gW, Xp, g[:, None])
+        np.add.at(gW, Xn, -g[:, None])
+        np.add.at(gV, Xp, g[:, None, None] * (S_p[:, None, :] - E_p))
+        np.add.at(gV, Xn, -g[:, None, None] * (S_n[:, None, :] - E_n))
+        gV += self.l2 * self.V; gW += self.l2 * self.W
+        self.t += 1
+        b1, b2, eps = 0.9, 0.999, 1e-8
+        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M *= b1; M += (1 - b1) * G
+            Vv *= b2; Vv += (1 - b2) * (G * G)
+            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        return float(np.mean(-np.log(sigmoid(d) + 1e-9)))
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index 0451b1a..cc761ee 100644
--- a/train.py
+++ b/train.py
@@ -122,12 +122,41 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     Xtr = transform(train_rows, features)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
+
+    user_pos = {}
+    user_neg = {}
+    for idx, r in enumerate(train_rows):
+        uid = r[1]
+        if ytr[idx] > 0.5:
+            user_pos.setdefault(uid, []).append(idx)
+        else:
+            user_neg.setdefault(uid, []).append(idx)
+    qualifying_users = [u for u in user_pos if u in user_neg and user_pos[u] and user_neg[u]]
+
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
-        order = rng.permutation(len(ytr))
-        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                  for i in range(0, len(order), config['bs'])]
+        if qualifying_users:
+            pos_list = []
+            neg_list = []
+            for u in qualifying_users:
+                pos_idx = user_pos[u]
+                neg_idx = np.asarray(user_neg[u])
+                for p in pos_idx:
+                    sampled = neg_idx[rng.integers(0, len(neg_idx), size=config['neg_per_pos'])]
+                    pos_list.extend([p] * config['neg_per_pos'])
+                    neg_list.extend(sampled.tolist())
+            pos_arr = np.asarray(pos_list, dtype=np.int64)
+            neg_arr = np.asarray(neg_list, dtype=np.int64)
+            perm = rng.permutation(len(pos_arr))
+            pos_arr = pos_arr[perm]
+            neg_arr = neg_arr[perm]
+            losses = [model.step_pairwise(Xtr[pos_arr[i:i + config['bs']]], Xtr[neg_arr[i:i + config['bs']]])
+                      for i in range(0, len(pos_arr), config['bs'])]
+        else:
+            order = rng.permutation(len(ytr))
+            losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
+                      for i in range(0, len(order), config['bs'])]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

---

## Iteration 2: `node_002`

**Status** `success` · **Parent** `node_001` · **Commit** `6217003fb655`

### Hypothesis

```text
SELECTED CHANGE
SELECTED CHANGE
Expand the feature representation in features.py from the current 5 fields to 9 fields (richer duration binning, in-user personalization crosses, and train-only item/author/user exposure-count buckets), keeping the FM backbone, the in-user pairwise BPR training loop, config defaults (k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2), the frozen splits/long_view target, and the GAUC/nDCG@5 evaluation exactly as they are.

Hypothesis: GAUC and nDCG@5 are computed within user groups and training now optimizes within-user score differences, so the model can only rank via signals that vary across items inside a user's group. Today the only such signals are video_id, author_id, tab, and a coarse 10-bin duration bucket; the user field is constant within a group and contributes only through interactions. Adding (a) finer duration quantile bins, (b) user x duration-bucket and user x tab crosses whose linear weights vary within a user's group and therefore encode personalized duration/tab preference directly in the pairwise objective, and (c) item-side and author-side popularity (exposure-count) buckets that provide a robust prior for long-tail videos with few training rows, should raise within-user ranking quality more than further loss-function tuning. Distinction from supplied prior attempts: the only sibling/lineage experiment from this parent changed the loss (pointwise -> pairwise BPR); no feature-engineering experiment has been tried on this branch, and the memory entry about a 9-field encoding comes from a different run with an FFM backbone, so this is a transfer to a materially different (plain FM, 5-field, single-negative BPR) code state, not a duplicate. The refuted sampled-softmax/listwise loss change is not repeated.

Implementation behavior (features.py only; model.py, train.py, config.py, requirements.txt unchanged):
- fit(rows): first compute duration quantile edges with 20 bins, i.e. edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 21)[1:-1]). Then compute train-only exposure counts (row counts, never labels): counts of rows per video_id (r[2]), per author_id (r[3]), and per user_id (r[1]). Convert each count c to a coarse string bucket via str(int(min(15, math.floor(math.log2(1 + c))))) and store three dicts video_cnt, author_cnt, user_cnt in the fitted state. Only after these statistics exist, build the per-field vocabularies by iterating raw(row, state_parts) over the training rows exactly as now.
- raw(...): return 9 string values in this fixed order: [user_id, video_id, author_id, tab, dur_bucket, user_id + '|' + dur_bucket, user_id + '|' + tab, video_cnt_bucket, author_cnt_bucket], where dur_bucket = str(int(np.searchsorted(edges, row[5]))) with the 20-bin edges, and the count buckets are looked up from the fitted dicts with a distinct fallback token (for example 'na') for unseen video_id/author_id. Change raw's signature to accept the fitted pieces it needs (edges plus the count dicts) and update both call sites accordingly.
- The fitted state must remain a plain serializable dict containing edges, vocabs (list of 9 dicts), offsets = np.cumsum([0] + dims[:-1]).astype(np.int32) over dims = [len(v) + 1 for v in vocabs], dim = sum(dims), and the three count-bucket dicts, so it continues to pickle inside the single checkpoint.
- transform(rows, state): allocate np.empty((len(rows), len(state['vocabs'])), dtype=np.int32) instead of a hard-coded width 5, and keep the existing unseen-value handling (vocab.get(value, len(vocab)) + offset) so validation/inference rows with unseen users, videos, authors, or crosses map to the per-field OOV slot. Preserve input row order and read only row fields 0-5 (never the label).
- No leakage: all statistics and vocabularies are fit on train_rows only inside fit() and reused unchanged for validation and inference; no target or post-outcome signal is used as input.
- model.py needs no edit because FM.logits/step/step_pairwise sum over the field axis and are agnostic to the number of fields; Predictor keeps using features['dim'].

Expected cost: roughly 2-3x the ~39s parent run (more fields per row plus a larger embedding table), comfortably inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.665044 | 0.533567 | 0.599305 | -0.004293 | 69 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 42 ++++++++++++++++++++++++++++++++++--------
 1 file changed, 34 insertions(+), 8 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..4c90cf7 100644
--- a/features.py
+++ b/features.py
@@ -23,29 +23,55 @@ while preserving the input-row contract and leakage constraints.
 """
 
 # Reference implementation: replaceable while preserving the contracts above.
+import math
 import numpy as np
 
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+def _bucket(c):
+    return str(int(min(15, math.floor(math.log2(1 + c)))))
+
+
+def raw(row, edges, video_cnt, author_cnt, user_cnt):
+    dur_bucket = str(int(np.searchsorted(edges, row[5])))
+    vid = row[2]
+    aid = row[3]
+    return [
+        row[1], row[2], row[3], row[4], dur_bucket,
+        row[1] + '|' + dur_bucket, row[1] + '|' + row[4],
+        video_cnt.get(vid, 'na'), author_cnt.get(aid, 'na'),
+    ]
 
 
 def fit(rows):
-    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 21)[1:-1])
+
+    video_counts = {}
+    author_counts = {}
+    user_counts = {}
+    for r in rows:
+        video_counts[r[2]] = video_counts.get(r[2], 0) + 1
+        author_counts[r[3]] = author_counts.get(r[3], 0) + 1
+        user_counts[r[1]] = user_counts.get(r[1], 0) + 1
+    video_cnt = {k: _bucket(v) for k, v in video_counts.items()}
+    author_cnt = {k: _bucket(v) for k, v in author_counts.items()}
+    user_cnt = {k: _bucket(v) for k, v in user_counts.items()}
+
+    vocabs = [{} for _ in range(9)]
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
+        for i, value in enumerate(raw(row, edges, video_cnt, author_cnt, user_cnt)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
     return dict(edges=edges, vocabs=vocabs,
-                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
+                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims),
+                video_cnt=video_cnt, author_cnt=author_cnt, user_cnt=user_cnt)
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 5), dtype=np.int32)
+    result = np.empty((len(rows), len(state['vocabs'])), dtype=np.int32)
     for n, row in enumerate(rows):
-        for i, value in enumerate(raw(row, state['edges'])):
+        values = raw(row, state['edges'], state['video_cnt'], state['author_cnt'], state['user_cnt'])
+        for i, value in enumerate(values):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
     return result
```

---

## Iteration 3: `node_003`

**Status** `success` · **Parent** `node_001` · **Commit** `26d64a4ff4dd`

### Hypothesis

```text
SELECTED CHANGE
Replace the FM backbone in model.py with a field-aware factorization machine (FFM) while keeping everything else on this branch unchanged (5-field encoding in features.py, in-user pairwise BPR training loop in train.py, frozen splits/long_view target, GAUC/nDCG@5 evaluation, checkpoint and load_predictor contracts).

Hypothesis: with only 5 fields and within-user pairwise training, a single shared latent vector per feature forces the same embedding to model user-video, user-author, user-tab and user-duration interactions simultaneously. Field-aware embeddings (one latent vector per (feature, interacting-field) pair) let the user representation specialize per target field, which is exactly the kind of within-user discrimination GAUC and nDCG@5 reward. Distinction from supplied prior attempts: the only sibling from this parent (node_002) changed features.py to 9 fields and lost 0.0043; no backbone change has been tried on this branch, and the memory entry mentioning an FFM backbone comes from a different run whose code state already had 9 fields and a different loss, so this is a transfer of the backbone idea to the plain 5-field, single-negative BPR parent, not a duplicate. The refuted sampled-softmax/listwise loss change is not repeated.

Implementation behavior:
- model.py: change FM.__init__ to signature FM(dim, fields, k=16, lr=0.001, l2=1e-6, seed=0). Store self.F = int(fields) and allocate self.V with shape (dim, fields, k) initialized rng.normal(0, 0.01) float32; keep self.W = zeros(dim), self.b = float32(0.0), and Adam moments mV/vV (shape of V) and mW/vW (shape of W), self.t = 0, self.lr, self.l2 exactly as now so vars(model) stays a plain, picklable, finite-checkable dict compatible with train.py's 'latest' state validation.
- model.py logits(X): compute E = self.V[X] with shape (B, F, F, k), where E[b, f, j] is the latent vector of the feature in field f used when interacting with field j. Precompute the pair list PAIRS = [(f, g) for f in range(F) for g in range(f+1, F)] once in __init__. Score z = self.b + self.W[X].sum(1) + sum over (f, g) in PAIRS of (E[:, f, g, :] * E[:, g, f, :]).sum(-1). Return (z, E) and update all callers accordingly.
- model.py step_pairwise(Xp, Xn): keep the identical BPR objective and bookkeeping as now (d = z_p - z_n, loss = mean(-log(sigmoid(d))), per-sample factor g = -sigmoid(-d)/B, positive rows use +g, negative rows use -g, self.b untouched, Adam with b1=0.9, b2=0.999, eps=1e-8 and self.t increment, l2 added as self.l2*V and self.l2*W). Only the gradient accumulation changes: allocate gV = np.zeros_like(self.V), gW = np.zeros_like(self.W); accumulate gW via np.add.at(gW, Xp, g[:, None]) and np.add.at(gW, Xn, -g[:, None]); for each (f, g_field) in PAIRS accumulate np.add.at(gV, (Xp[:, f], g_field), g[:, None] * E_p[:, g_field, f, :]), np.add.at(gV, (Xp[:, g_field], f), g[:, None] * E_p[:, f, g_field, :]) and the same two updates for the negative side with -g and E_n. Return the mean pairwise loss as a float.
- model.py step(X, y): keep the pointwise sigmoid cross-entropy fallback used by train.py's degenerate-data branch, rewritten with the same FFM gradient accumulation pattern (per-sample factor g = (sigmoid(z) - y)/B, self.b -= lr * g.sum()).
- model.py Predictor.__init__: construct FM(self.features['dim'], len(self.features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed']) and keep restoring exactly V, W, b with the existing shape/finiteness checks; predict(rows) unchanged.
- train.py: pass the field count to both FM constructions, i.e. FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed']) in the resume branch and the fresh branch. Leave the user grouping, pair sampling, epoch loop, validation call, best-primary selection, payload contents, atomic save_checkpoint, and resume logic exactly as they are.
- config.py: change the DEFAULTS value k from 16 to 8 (FFM holds F=5 vectors per feature, so a smaller k keeps parameter count and per-step cost in the same range and limits overfitting); keep lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2 and the existing validation logic unchanged.
- features.py and requirements.txt unchanged.

Expected cost roughly 3-5x the ~39s parent run, comfortably inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668457 | 0.535410 | 0.601933 | -0.001665 | 62 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  2 +-
 model.py  | 47 +++++++++++++++++++++++++++++------------------
 train.py  |  4 ++--
 3 files changed, 32 insertions(+), 21 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 3b1b451..41c1a91 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2)
+DEFAULTS = dict(k=8, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2)
 
 
 def resolve(overrides):
diff --git a/model.py b/model.py
index 23fdaa1..416e8cd 100644
--- a/model.py
+++ b/model.py
@@ -32,32 +32,41 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, fields, k=16, lr=0.001, l2=1e-6, seed=0):
         rng = np.random.default_rng(seed)
-        self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
+        self.F = int(fields)
+        self.V = rng.normal(0, 0.01, (dim, self.F, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
         self.b = np.float32(0.0)
         self.lr, self.l2 = lr, l2
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
         self.t = 0
+        self.PAIRS = [(f, g) for f in range(self.F) for g in range(f + 1, self.F)]
 
     def logits(self, X):
-        E = self.V[X]                                   # (B,F,k)
-        S = E.sum(1)                                    # (B,k)
-        inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        E = self.V[X]                                   # (B,F,F,k)
+        z = self.b + self.W[X].sum(1)
+        for f, g in self.PAIRS:
+            z = z + (E[:, f, g, :] * E[:, g, f, :]).sum(-1)
+        return z, E
+
+    def _adam(self):
+        self.t += 1
+        b1, b2, eps = 0.9, 0.999, 1e-8
+        return b1, b2, eps
 
     def step(self, X, y):
         B = len(y)
-        z, E, S = self.logits(X)
-        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
+        z, E = self.logits(X)
+        g = ((sigmoid(z) - y) / B).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
+        for f, gf in self.PAIRS:
+            np.add.at(gV, (X[:, f], gf), g[:, None] * E[:, gf, f, :])
+            np.add.at(gV, (X[:, gf], f), g[:, None] * E[:, f, gf, :])
         gV += self.l2 * self.V; gW += self.l2 * self.W
-        self.t += 1
-        b1, b2, eps = 0.9, 0.999, 1e-8
+        b1, b2, eps = self._adam()
         for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
             M *= b1; M += (1 - b1) * G
             Vv *= b2; Vv += (1 - b2) * (G * G)
@@ -67,18 +76,20 @@ class FM:
 
     def step_pairwise(self, Xp, Xn):
         B = len(Xp)
-        z_p, E_p, S_p = self.logits(Xp)
-        z_n, E_n, S_n = self.logits(Xn)
+        z_p, E_p = self.logits(Xp)
+        z_n, E_n = self.logits(Xn)
         d = z_p - z_n
         g = (-sigmoid(-d) / B).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, Xp, g[:, None])
         np.add.at(gW, Xn, -g[:, None])
-        np.add.at(gV, Xp, g[:, None, None] * (S_p[:, None, :] - E_p))
-        np.add.at(gV, Xn, -g[:, None, None] * (S_n[:, None, :] - E_n))
+        for f, gf in self.PAIRS:
+            np.add.at(gV, (Xp[:, f], gf), g[:, None] * E_p[:, gf, f, :])
+            np.add.at(gV, (Xp[:, gf], f), g[:, None] * E_p[:, f, gf, :])
+            np.add.at(gV, (Xn[:, f], gf), -g[:, None] * E_n[:, gf, f, :])
+            np.add.at(gV, (Xn[:, gf], f), -g[:, None] * E_n[:, f, gf, :])
         gV += self.l2 * self.V; gW += self.l2 * self.W
-        self.t += 1
-        b1, b2, eps = 0.9, 0.999, 1e-8
+        b1, b2, eps = self._adam()
         for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
             M *= b1; M += (1 - b1) * G
             Vv *= b2; Vv += (1 - b2) * (G * G)
@@ -105,7 +116,7 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        self.model = FM(self.features['dim'], len(self.features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         weights = state['model_state']
         for name in ('V', 'W', 'b'):
             value = weights[name]
diff --git a/train.py b/train.py
index cc761ee..c121ea4 100644
--- a/train.py
+++ b/train.py
@@ -98,7 +98,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +115,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
```

---

## Iteration 4: `node_004`

**Status** `success` · **Parent** `node_001` · **Commit** `5866c91946a4`

### Hypothesis

```text
SELECTED CHANGE
SELECTED CHANGE
On top of the parent's in-user pairwise BPR FM (5 fields, k=16, neg_per_pos=2), change the training objective from pure BPR to a hybrid multi-objective loss that adds an auxiliary pointwise sigmoid cross-entropy term computed over ALL training rows (not only the sampled pairs), with both gradients accumulated into a single Adam update per step.

Hypothesis: the current pair construction in train.py silently discards every training row belonging to a user that lacks both a positive and a negative (qualifying_users filter), and even for qualifying users each epoch only touches ~2 negatives per positive, so most rows never contribute to item/author/duration embedding learning. GAUC/nDCG@5 depend on within-user ordering, which BPR optimizes, but the item-side priors that make that ordering generalize to sparse videos/authors are better estimated from all labeled rows. Blending a weighted pointwise BCE over the full training set with the existing within-user BPR term should keep the ranking-aligned gradient while restoring full data coverage and re-enabling the global bias update. Distinction from supplied prior attempts: the only siblings from this parent changed features.py to 9 fields (node_002, worse) and replaced the backbone with FFM (node_003, worse); no loss-formulation experiment has been run from this parent since BPR was introduced. The refuted memory entry replaced BPR outright with a multi-negative in-user sampled-softmax/listwise loss on a different run's FFM/9-field code state; here BPR is retained and augmented with a full-data pointwise auxiliary term, which is a materially different objective.

Implementation behavior:
- config.py: add DEFAULTS key alpha=0.5 (weight of the auxiliary pointwise term) and validate it in the existing float loop by extending the tuple to ('lr', 'l2', 'alpha'), so alpha must be finite and >= 0 (alpha == 0 is allowed and reproduces the parent). Leave k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2 unchanged so the comparison is controlled.
- model.py: keep FM.logits, FM.step, FM.step_pairwise, FM.predict, Predictor, read_checkpoint and load_predictor exactly as they are (do not add any new instance attributes, so vars(model) keys stay identical for train.py's 'latest' state validation). Add a method FM.step_mixed(Xp, Xn, Xo, yo, alpha) that: computes z_p, E_p, S_p = self.logits(Xp) and z_n, E_n, S_n = self.logits(Xn); d = z_p - z_n; Bp = len(Xp); pairwise per-row factors gp = (-sigmoid(-d)/Bp) for the positive rows and -gp for the negative rows; computes z_o, E_o, S_o = self.logits(Xo) with Bo = len(yo) and pointwise factor go = (alpha * (sigmoid(z_o) - yo) / Bo).astype(np.float32) (skip the pointwise part entirely if Bo == 0 or alpha == 0). Allocate gV = np.zeros_like(self.V), gW = np.zeros_like(self.W) and accumulate np.add.at(gW, Xp, gp[:, None]), np.add.at(gW, Xn, -gp[:, None]), np.add.at(gW, Xo, go[:, None]); np.add.at(gV, Xp, gp[:, None, None] * (S_p[:, None, :] - E_p)), np.add.at(gV, Xn, -gp[:, None, None] * (S_n[:, None, :] - E_n)), np.add.at(gV, Xo, go[:, None, None] * (S_o[:, None, :] - E_o)). Then gV += self.l2 * self.V; gW += self.l2 * self.W; self.t += 1; apply the same Adam update already used (b1=0.9, b2=0.999, eps=1e-8) to (V, gV, mV, vV) and (W, gW, mW, vW); update the global bias only from the pointwise part via self.b -= self.lr * go.sum() (the bias cancels in the pairwise difference). Return the combined float loss: float(np.mean(-np.log(sigmoid(d) + 1e-9)) + alpha * (-np.mean(yo * np.log(sigmoid(z_o) + 1e-9) + (1 - yo) * np.log(1 - sigmoid(z_o) + 1e-9)))) (omit the second term when the pointwise part is skipped).
- train.py: keep the existing user_pos/user_neg grouping, qualifying_users filter, per-epoch pair sampling with config['neg_per_pos'], the rng.permutation shuffle of the pair arrays, and the degenerate-data fallback to the pointwise model.step loop. Inside the qualifying_users branch, additionally build order = rng.permutation(len(ytr)) each epoch, then set n_batches = max(ceil(len(order)/config['bs']), ceil(len(pos_arr)/config['bs'])) and per-step chunk sizes point_chunk = ceil(len(order)/n_batches) and pair_chunk = ceil(len(pos_arr)/n_batches), so that each epoch traverses all training rows once for the pointwise term and all sampled pairs once for the BPR term. Loop i in range(n_batches) and call model.step_mixed(Xtr[pos_arr[i*pair_chunk:(i+1)*pair_chunk]], Xtr[neg_arr[i*pair_chunk:(i+1)*pair_chunk]], Xtr[order[i*point_chunk:(i+1)*point_chunk]], ytr[order[i*point_chunk:(i+1)*point_chunk]], config['alpha']), collecting the returned losses into the existing losses list used for the epoch log. Guard against empty pair slices (skip the call if the pair slice is empty). Leave validation on valid_rows, best-primary selection, payload contents ('V', 'W', 'b' in model_state), atomic save_checkpoint, resume logic, and the finiteness checks exactly as they are.
- features.py and requirements.txt unchanged.

Expected cost roughly 1.5-2x the ~39s parent run (one extra full-data forward/backward pass per epoch), comfortably inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.666766 | 0.534868 | 0.600817 | -0.002781 | 67 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 31 +++++++++++++++++++++++++++++++
 train.py  | 14 ++++++++++++--
 3 files changed, 45 insertions(+), 4 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 3b1b451..8bea778 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2, alpha=0.5)
 
 
 def resolve(overrides):
@@ -33,7 +33,7 @@ def resolve(overrides):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
-    for key in ('lr', 'l2'):
+    for key in ('lr', 'l2', 'alpha'):
         if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
             raise ValueError(f'invalid {key}')
     return config
diff --git a/model.py b/model.py
index 23fdaa1..fc1c36f 100644
--- a/model.py
+++ b/model.py
@@ -85,6 +85,37 @@ class FM:
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         return float(np.mean(-np.log(sigmoid(d) + 1e-9)))
 
+    def step_mixed(self, Xp, Xn, Xo, yo, alpha):
+        Bp = len(Xp)
+        z_p, E_p, S_p = self.logits(Xp)
+        z_n, E_n, S_n = self.logits(Xn)
+        d = z_p - z_n
+        gp = (-sigmoid(-d) / Bp).astype(np.float32)
+        Bo = len(yo)
+        do_pointwise = Bo > 0 and alpha != 0
+        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        np.add.at(gW, Xp, gp[:, None])
+        np.add.at(gW, Xn, -gp[:, None])
+        np.add.at(gV, Xp, gp[:, None, None] * (S_p[:, None, :] - E_p))
+        np.add.at(gV, Xn, -gp[:, None, None] * (S_n[:, None, :] - E_n))
+        if do_pointwise:
+            z_o, E_o, S_o = self.logits(Xo)
+            go = (alpha * (sigmoid(z_o) - yo) / Bo).astype(np.float32)
+            np.add.at(gW, Xo, go[:, None])
+            np.add.at(gV, Xo, go[:, None, None] * (S_o[:, None, :] - E_o))
+        gV += self.l2 * self.V; gW += self.l2 * self.W
+        self.t += 1
+        b1, b2, eps = 0.9, 0.999, 1e-8
+        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M *= b1; M += (1 - b1) * G
+            Vv *= b2; Vv += (1 - b2) * (G * G)
+            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        loss = float(np.mean(-np.log(sigmoid(d) + 1e-9)))
+        if do_pointwise:
+            self.b -= self.lr * go.sum()
+            loss += alpha * float(-np.mean(yo * np.log(sigmoid(z_o) + 1e-9) + (1 - yo) * np.log(1 - sigmoid(z_o) + 1e-9)))
+        return loss
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index cc761ee..3500cea 100644
--- a/train.py
+++ b/train.py
@@ -151,8 +151,18 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             perm = rng.permutation(len(pos_arr))
             pos_arr = pos_arr[perm]
             neg_arr = neg_arr[perm]
-            losses = [model.step_pairwise(Xtr[pos_arr[i:i + config['bs']]], Xtr[neg_arr[i:i + config['bs']]])
-                      for i in range(0, len(pos_arr), config['bs'])]
+            order = rng.permutation(len(ytr))
+            n_batches = max(-(-len(order) // config['bs']), -(-len(pos_arr) // config['bs']))
+            point_chunk = -(-len(order) // n_batches)
+            pair_chunk = -(-len(pos_arr) // n_batches)
+            losses = []
+            for i in range(n_batches):
+                pp = pos_arr[i * pair_chunk:(i + 1) * pair_chunk]
+                nn = neg_arr[i * pair_chunk:(i + 1) * pair_chunk]
+                if len(pp) == 0:
+                    continue
+                oo = order[i * point_chunk:(i + 1) * point_chunk]
+                losses.append(model.step_mixed(Xtr[pp], Xtr[nn], Xtr[oo], ytr[oo], config['alpha']))
         else:
             order = rng.permutation(len(ytr))
             losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
```

---

## Iteration 5: `node_005`

**Status** `success` · **Parent** `node_001` · **Commit** `876830c96913`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT: Bagged multi-seed ensemble of the existing pairwise-BPR FM (train N independent FMs in one run and average their scores), keeping everything else on this branch identical (5-field features.py encoding, FM backbone, in-user BPR pair sampling with neg_per_pos=2, k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, frozen splits/long_view target, GAUC/nDCG@5 evaluation).

Hypothesis: every structural sibling from this parent lost ground (9-field features -0.0043, FFM backbone -0.0017, BPR+pointwise hybrid -0.0028), which suggests the single FM is not capacity-limited but variance-limited: its within-user ranking depends on sparse ID embeddings fit from a small number of Adam steps over randomly sampled negatives, so both the random initialization and the per-epoch negative draw inject noise into item/author ordering. Averaging the logits of several independently initialized models trained on independently sampled negative pairs should cancel a large part of that noise and raise within-user ordering quality (GAUC and nDCG@5) without adding model complexity or new features. Distinction from supplied prior attempts: no lineage node, sibling, or memory entry has tried ensembling / prediction averaging; all previous experiments from this parent modified features, backbone, or loss for a single model.

Implementation behavior:
- config.py: add DEFAULTS key n_models=3 and validate it in the existing integer loop by extending the tuple to ('k', 'epochs', 'bs', 'patience', 'seed', 'neg_per_pos', 'n_models') so it must be an int >= 1 (n_models=1 reproduces the parent exactly). Leave all other defaults unchanged so the comparison is controlled.
- model.py: keep the FM class (logits, step, step_pairwise, predict), read_checkpoint, and load_predictor signatures and behavior unchanged. Change Predictor to hold a list of members: read config = state['config']; treat state['model_state'] as a list of per-member dicts with keys 'V', 'W', 'b' (if a bare dict is found, wrap it in a one-element list for robustness); construct one FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i) per member i in range(len(model_state)); restore V, W, b into each member with the existing shape-match and np.isfinite checks, raising the same 'incompatible or nonfinite model weights' error on mismatch. Predictor.predict(rows) must transform rows once with the restored features state and return the element-wise mean over members of member.predict(X) as a finite float array in input order (empty input still returns np.empty(0, dtype=np.float32)).
- train.py: replace the single `model` with `models`, a list of config['n_models'] FMs constructed as FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i). Keep the single seeded `rng` and the existing user_pos/user_neg grouping and qualifying_users filter; inside each epoch, loop over members and, for each member, draw its own negative samples and its own rng.permutation from that shared rng (so members see different pairs) and run the existing minibatch loop calling member.step_pairwise(...); keep the existing degenerate-data fallback to member.step(...) for every member when qualifying_users is empty. Collect all member losses into the existing `losses` list for the epoch log. Compute validation with the ensemble score: ensemble_pred = np.mean([m.predict(Xva) for m in models], axis=0), then call evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], ensemble_pred) exactly as now; early stopping, the best + 1e-5 comparison, bad/patience bookkeeping, and best_epoch remain based on this ensemble primary. Set payload['model_state'] = [{key: copy.deepcopy(getattr(m, key)) for key in ('V', 'W', 'b')} for m in models] and payload['training_state']['latest'] = [copy.deepcopy(vars(m)) for m in models]; run the nonfinite guard over ('V','W','b','mV','vV','mW','vW') for every member. Keep atomic save_checkpoint, payload['validation'], and the per-epoch log line unchanged in form.
- train.py resume path: after Predictor(payload) validation, rebuild the member list, require len(state['latest']) == config['n_models'] and, for each member, set(state['latest'][i]) == set(vars(models[i])) plus the existing per-key shape/finiteness checks (raise 'incomplete optimizer/model state' / 'incompatible or nonfinite latest state: <key>' otherwise); restore each member's attributes; keep the existing epoch/bad/best/lr/l2/t progress validation using models[0].
- features.py and requirements.txt unchanged.

Expected cost roughly 3x the ~39s parent run (about 110-130s including per-epoch ensemble validation), far inside candidate_timeout_s and affordable within the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669846 | 0.537040 | 0.603443 | -0.000155 | 93 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 24 ++++++++++++++-------
 train.py  | 74 ++++++++++++++++++++++++++++++++++++---------------------------
 3 files changed, 60 insertions(+), 42 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 3b1b451..0fad1bc 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2, n_models=3)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'neg_per_pos'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'neg_per_pos', 'n_models'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 23fdaa1..1bd9d1d 100644
--- a/model.py
+++ b/model.py
@@ -105,13 +105,19 @@ class Predictor:
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
+        model_state = state['model_state']
+        if isinstance(model_state, dict):
+            model_state = [model_state]
+        self.models = []
+        for i, weights in enumerate(model_state):
+            model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'],
+                       seed=config['seed'] + i)
+            for name in ('V', 'W', 'b'):
+                value = weights[name]
+                if np.shape(value) != np.shape(getattr(model, name)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite model weights: ' + name)
+                setattr(model, name, value)
+            self.models.append(model)
 
     def predict(self, rows):
         """Return one finite real-valued score per row, preserving input order.
@@ -122,7 +128,9 @@ class Predictor:
         """
         if not len(rows):
             return np.empty(0, dtype=np.float32)
-        return self.model.predict(transform(rows, self.features))
+        X = transform(rows, self.features)
+        preds = np.mean([m.predict(X) for m in self.models], axis=0)
+        return preds.astype(np.float32)
 
 
 def load_predictor(checkpoint_path):
diff --git a/train.py b/train.py
index cc761ee..77af03c 100644
--- a/train.py
+++ b/train.py
@@ -98,13 +98,19 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
-        if set(state['latest']) != set(vars(model)):
+        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i)
+                  for i in range(config['n_models'])]
+        latest = state['latest']
+        if len(latest) != config['n_models']:
             raise ValueError('incomplete optimizer/model state')
-        for key, value in state['latest'].items():
-            if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
-                raise ValueError('incompatible or nonfinite latest state: ' + key)
-            setattr(model, key, value)
+        for i, model in enumerate(models):
+            if set(latest[i]) != set(vars(model)):
+                raise ValueError('incomplete optimizer/model state')
+            for key, value in latest[i].items():
+                if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite latest state: ' + key)
+                setattr(model, key, value)
+        model = models[0]
         best, bad, epoch = state['best'], state['bad'], state['epoch']
         if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
                 or type(bad) is not int or not 0 <= bad <= config['patience']
@@ -115,7 +121,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i)
+                  for i in range(config['n_models'])]
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -136,38 +143,41 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
-        if qualifying_users:
-            pos_list = []
-            neg_list = []
-            for u in qualifying_users:
-                pos_idx = user_pos[u]
-                neg_idx = np.asarray(user_neg[u])
-                for p in pos_idx:
-                    sampled = neg_idx[rng.integers(0, len(neg_idx), size=config['neg_per_pos'])]
-                    pos_list.extend([p] * config['neg_per_pos'])
-                    neg_list.extend(sampled.tolist())
-            pos_arr = np.asarray(pos_list, dtype=np.int64)
-            neg_arr = np.asarray(neg_list, dtype=np.int64)
-            perm = rng.permutation(len(pos_arr))
-            pos_arr = pos_arr[perm]
-            neg_arr = neg_arr[perm]
-            losses = [model.step_pairwise(Xtr[pos_arr[i:i + config['bs']]], Xtr[neg_arr[i:i + config['bs']]])
-                      for i in range(0, len(pos_arr), config['bs'])]
-        else:
-            order = rng.permutation(len(ytr))
-            losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                      for i in range(0, len(order), config['bs'])]
-        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
+        losses = []
+        for model in models:
+            if qualifying_users:
+                pos_list = []
+                neg_list = []
+                for u in qualifying_users:
+                    pos_idx = user_pos[u]
+                    neg_idx = np.asarray(user_neg[u])
+                    for p in pos_idx:
+                        sampled = neg_idx[rng.integers(0, len(neg_idx), size=config['neg_per_pos'])]
+                        pos_list.extend([p] * config['neg_per_pos'])
+                        neg_list.extend(sampled.tolist())
+                pos_arr = np.asarray(pos_list, dtype=np.int64)
+                neg_arr = np.asarray(neg_list, dtype=np.int64)
+                perm = rng.permutation(len(pos_arr))
+                pos_arr = pos_arr[perm]
+                neg_arr = neg_arr[perm]
+                losses.extend(model.step_pairwise(Xtr[pos_arr[i:i + config['bs']]], Xtr[neg_arr[i:i + config['bs']]])
+                              for i in range(0, len(pos_arr), config['bs']))
+            else:
+                order = rng.permutation(len(ytr))
+                losses.extend(model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
+                              for i in range(0, len(order), config['bs']))
+        ensemble_pred = np.mean([m.predict(Xva) for m in models], axis=0)
+        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], ensemble_pred)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            payload['model_state'] = [{key: copy.deepcopy(getattr(m, key)) for key in ('V', 'W', 'b')} for m in models]
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+        if not all(np.isfinite(getattr(m, key)).all() for m in models for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
-            rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
+            rng=rng.bit_generator.state, latest=[copy.deepcopy(vars(m)) for m in models])
         payload['validation'] = validation
         save_checkpoint(checkpoint_path, payload)
         print(f'epoch={epoch} loss={np.mean(losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
```

---

## Iteration 6: `node_006`

**Status** `success` · **Parent** `node_001` · **Commit** `2f05345e54c1`

### Hypothesis

```text
SELECTED CHANGE
SELECTED CHANGE
Replace the dense Adam update in model.py with a lazy/sparse Adam update that touches only the feature rows appearing in the current minibatch, keeping everything else on this branch identical (5-field features.py encoding, FM backbone with k=16, in-user pairwise BPR pair sampling with neg_per_pos=2, frozen splits/long_view target, GAUC/nDCG@5 evaluation, checkpoint and load_predictor contracts).

Hypothesis: FM.step_pairwise currently applies the Adam update to every row of V and W on every step, even for features that did not occur in the batch. Because momentum m decays by 0.9 per step while v decays by only 0.999, an untouched embedding keeps drifting in the direction of its last gradient for many subsequent steps (an effective ~10x amplification of each sparse gradient), and the L2 term self.l2*V is also applied to all rows each step. With very sparse ID features (video_id, author_id) this injects systematic noise into exactly the item-side embeddings that determine within-user ordering, which is what GAUC and nDCG@5 measure. Restricting the moment updates, bias-corrected step, and weight decay to the rows actually present in the batch should make each embedding's trajectory reflect only its own gradients and improve within-user ranking. Distinction from supplied prior attempts: the four siblings from this parent changed features (9 fields, node_002), backbone (FFM, node_003), loss (BPR + pointwise hybrid, node_004), and prediction ensembling (node_005) - all lost ground; no optimizer/update-rule experiment has been run anywhere on this branch. The single memory entry about optimizer hyperparameters comes from a different run and crashed with an error; this is an algorithmic sparse-update change, not an Adam hyperparameter sweep.

Implementation behavior:
- model.py: keep the class name FM and the signatures/behavior of __init__, logits, predict, Predictor, read_checkpoint and load_predictor unchanged; do not add or remove any instance attributes, so vars(model) keys stay exactly ('V','W','b','lr','l2','mV','vV','mW','vW','t') and train.py's 'latest' state validation and resume logic keep working unchanged.
- model.py FM.step_pairwise(Xp, Xn): keep the identical BPR objective and bookkeeping (z_p/z_n via self.logits, d = z_p - z_n, per-row factor g = (-sigmoid(-d)/B).astype(np.float32), +g on positive rows and -g on negative rows, self.b untouched, self.t += 1, b1=0.9, b2=0.999, eps=1e-8, return float(np.mean(-np.log(sigmoid(d) + 1e-9)))). Accumulate gV and gW into dense zeros_like buffers with the existing np.add.at calls, then compute idx = np.unique(np.concatenate((Xp.ravel(), Xn.ravel()))) and apply the update only to those rows: gV_i = gV[idx] + self.l2 * self.V[idx]; self.mV[idx] = b1 * self.mV[idx] + (1 - b1) * gV_i; self.vV[idx] = b2 * self.vV[idx] + (1 - b2) * (gV_i * gV_i); self.V[idx] -= self.lr * (self.mV[idx] / (1 - b1 ** self.t)) / (np.sqrt(self.vV[idx] / (1 - b2 ** self.t)) + eps); and the exact analogue for W with gW_i = gW[idx] + self.l2 * self.W[idx]. Do not modify rows outside idx, and do not add the L2 term to untouched rows.
- model.py FM.step(X, y): apply the same lazy update pattern (idx = np.unique(X.ravel()), moments/weight-decay/parameter update restricted to idx, global self.t used for bias correction) so the degenerate-data pointwise fallback in train.py stays consistent; keep g = ((sigmoid(z) - y)/B), the global-bias update self.b -= self.lr * g.sum(), and the returned logloss value unchanged.
- config.py: change DEFAULTS epochs from 40 to 120 and leave k=16, lr=0.001, l2=1e-6, bs=8192, patience=4, seed=0, neg_per_pos=2 and all validation logic unchanged. Rationale: lazy Adam removes the phantom momentum amplification, so per-step progress is smaller and the run may need more epochs; patience=4 early stopping on validation primary still governs when training ends, and best-epoch selection is unchanged.
- train.py, features.py and requirements.txt unchanged.

Expected cost: per-step cost is equal or lower than the parent (fewer full-array Adam ops), and the epoch cap raise means at most roughly 3x the ~39s parent run (about 60-130s), far inside candidate_timeout_s and affordable within the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669700 | 0.537009 | 0.603355 | -0.000243 | 41 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  2 +-
 model.py  | 28 ++++++++++++++++++----------
 2 files changed, 19 insertions(+), 11 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 3b1b451..388e6c7 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, neg_per_pos=2)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=120, bs=8192, patience=4, seed=0, neg_per_pos=2)
 
 
 def resolve(overrides):
diff --git a/model.py b/model.py
index 23fdaa1..9321740 100644
--- a/model.py
+++ b/model.py
@@ -55,13 +55,17 @@ class FM:
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
         np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
-        gV += self.l2 * self.V; gW += self.l2 * self.W
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M *= b1; M += (1 - b1) * G
-            Vv *= b2; Vv += (1 - b2) * (G * G)
-            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        idx = np.unique(X.ravel())
+        gV_i = gV[idx] + self.l2 * self.V[idx]
+        self.mV[idx] = b1 * self.mV[idx] + (1 - b1) * gV_i
+        self.vV[idx] = b2 * self.vV[idx] + (1 - b2) * (gV_i * gV_i)
+        self.V[idx] -= self.lr * (self.mV[idx] / (1 - b1 ** self.t)) / (np.sqrt(self.vV[idx] / (1 - b2 ** self.t)) + eps)
+        gW_i = gW[idx] + self.l2 * self.W[idx]
+        self.mW[idx] = b1 * self.mW[idx] + (1 - b1) * gW_i
+        self.vW[idx] = b2 * self.vW[idx] + (1 - b2) * (gW_i * gW_i)
+        self.W[idx] -= self.lr * (self.mW[idx] / (1 - b1 ** self.t)) / (np.sqrt(self.vW[idx] / (1 - b2 ** self.t)) + eps)
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
@@ -76,13 +80,17 @@ class FM:
         np.add.at(gW, Xn, -g[:, None])
         np.add.at(gV, Xp, g[:, None, None] * (S_p[:, None, :] - E_p))
         np.add.at(gV, Xn, -g[:, None, None] * (S_n[:, None, :] - E_n))
-        gV += self.l2 * self.V; gW += self.l2 * self.W
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M *= b1; M += (1 - b1) * G
-            Vv *= b2; Vv += (1 - b2) * (G * G)
-            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        idx = np.unique(np.concatenate((Xp.ravel(), Xn.ravel())))
+        gV_i = gV[idx] + self.l2 * self.V[idx]
+        self.mV[idx] = b1 * self.mV[idx] + (1 - b1) * gV_i
+        self.vV[idx] = b2 * self.vV[idx] + (1 - b2) * (gV_i * gV_i)
+        self.V[idx] -= self.lr * (self.mV[idx] / (1 - b1 ** self.t)) / (np.sqrt(self.vV[idx] / (1 - b2 ** self.t)) + eps)
+        gW_i = gW[idx] + self.l2 * self.W[idx]
+        self.mW[idx] = b1 * self.mW[idx] + (1 - b1) * gW_i
+        self.vW[idx] = b2 * self.vW[idx] + (1 - b2) * (gW_i * gW_i)
+        self.W[idx] -= self.lr * (self.mW[idx] / (1 - b1 ** self.t)) / (np.sqrt(self.vW[idx] / (1 - b2 ** self.t)) + eps)
         return float(np.mean(-np.log(sigmoid(d) + 1e-9)))
 
     def predict(self, X, bs=200_000):
```

---

## Iteration 7: `node_007`

**Status** `success` · **Parent** `genesis` · **Commit** `cca2fd74d9c9`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature engineering subsystem — untouched anywhere in this run; the only supplied sibling from this genesis parent, node_001, changed the training loss to pairwise BPR, and the memory entries are loss/optimizer changes on other branches, so this is a materially different, non-duplicate experiment): enrich the FM input encoding in features.py from the current 5 categorical fields to 9 fields by adding train-only exposure-frequency buckets and one conjunction feature, while keeping the pointwise sigmoid loss, the FM backbone in model.py, train.py, and all config.py values (k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0) exactly as they are, so the effect of the encoding is isolated.

Hypothesis: the reference FM only sees raw ID indices, so it cannot generalize across rare or unseen users/videos/authors; explicit popularity/activity buckets (computed from training rows only, using no labels and no post-outcome signals) give the model a label-free generalization signal for cold or low-frequency IDs, and an explicit tab×duration-decile conjunction gives that interaction a dedicated weight and embedding beyond the rank-k dot product.

Implementation behavior (features.py only; train.py, model.py, config.py, requirements.txt unchanged):
- fit(rows) becomes two-pass. Pass 1: compute the existing duration quantile edges (np.quantile over r[5], np.linspace(0,1,11)[1:-1], unchanged 10 bins) and build three plain-dict counters over the training rows only: user_counts[r[1]], video_counts[r[2]], author_counts[r[3]]. Pass 2: build one vocab per field over the 9 field values produced by raw().
- Add a helper freq_bucket(count) returning 'z' when count == 0 (i.e. an ID unseen in training) and otherwise str(min(int(np.floor(np.log2(count))), 20)).
- raw(row, state) returns exactly these 9 strings in this order: (0) str(row[1]) user_id, (1) str(row[2]) video_id, (2) str(row[3]) author_id, (3) str(row[4]) tab, (4) 'd' + str(int(np.searchsorted(state['edges'], row[5]))) duration decile, (5) 'uc' + freq_bucket(state['user_counts'].get(row[1], 0)), (6) 'vc' + freq_bucket(state['video_counts'].get(row[2], 0)), (7) 'ac' + freq_bucket(state['author_counts'].get(row[3], 0)), (8) 'td' + str(row[4]) + '|' + the duration-decile string from field 4. raw must take the fitted state (or an equivalent dict carrying edges plus the three counters) so transform reuses training-fitted statistics without refitting.
- The returned fitted state keeps the same structure and keys used elsewhere: edges, vocabs (now 9 entries), offsets = np.cumsum([0] + dims[:-1]).astype(np.int32) with dims = [len(v)+1 for v in vocabs], dim = sum(dims), plus the three new count dicts. All state must stay picklable so train.py's single-checkpoint payload and model.Predictor keep working unchanged.
- transform(rows, state) keeps its signature and row order, allocates np.empty((len(rows), len(state['vocabs'])), dtype=np.int32) instead of a hardcoded 5 columns, and keeps the existing unseen-value handling vocab.get(value, len(vocab)) + offsets[i] so unseen users/items/videos and never-seen frequency buckets fall into the per-field OOV slot.
- No date-derived feature (the splits are time-based, so date values would be OOV at validation) and no label-derived statistic of any kind; only ID exposure counts and the duration input are used.

Everything downstream is untouched: model.FM.logits/step/predict already handle an arbitrary number of fields, Predictor rebuilds FM from features_state['dim'], and load_predictor/train contracts are preserved. Expected cost is roughly 1.5-2x the 37s genesis baseline (field count 5→9, vocab growth only ~60 extra rows), comfortably inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.665424 | 0.535459 | 0.600441 | -0.001027 | 67 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 42 ++++++++++++++++++++++++++++++++++--------
 1 file changed, 34 insertions(+), 8 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..5b1da2d 100644
--- a/features.py
+++ b/features.py
@@ -26,26 +26,52 @@ while preserving the input-row contract and leakage constraints.
 import numpy as np
 
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+def freq_bucket(count):
+    if count == 0:
+        return 'z'
+    return str(min(int(np.floor(np.log2(count))), 20))
+
+
+def raw(row, state):
+    duration_decile = str(int(np.searchsorted(state['edges'], row[5])))
+    return [
+        str(row[1]),
+        str(row[2]),
+        str(row[3]),
+        str(row[4]),
+        'd' + duration_decile,
+        'uc' + freq_bucket(state['user_counts'].get(row[1], 0)),
+        'vc' + freq_bucket(state['video_counts'].get(row[2], 0)),
+        'ac' + freq_bucket(state['author_counts'].get(row[3], 0)),
+        'td' + str(row[4]) + '|' + duration_decile,
+    ]
 
 
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    user_counts, video_counts, author_counts = {}, {}, {}
+    for r in rows:
+        user_counts[r[1]] = user_counts.get(r[1], 0) + 1
+        video_counts[r[2]] = video_counts.get(r[2], 0) + 1
+        author_counts[r[3]] = author_counts.get(r[3], 0) + 1
+    state = dict(edges=edges, user_counts=user_counts, video_counts=video_counts,
+                 author_counts=author_counts)
+    vocabs = [{} for _ in range(9)]
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
+        for i, value in enumerate(raw(row, state)):
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
+        for i, value in enumerate(raw(row, state)):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
     return result
```

---

## Iteration 8: `node_008`

**Status** `success` · **Parent** `node_007` · **Commit** `fd929205be9d`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model backbone subsystem — never touched anywhere in this lineage or in the supplied memory: node_007 changed feature encoding, node_001 changed the loss to pairwise BPR on a different branch, and other-run memory covers loss/EMA/ensembling/optimizer-hyperparameter edits only; this is therefore not a repeat of any supplied attempt): upgrade the reference second-order FM in model.py into a DeepFM — the existing FM (bias + linear + rank-k pairwise interaction) plus a shared-embedding MLP tower — while keeping the 9-field encoding in features.py, the pointwise sigmoid cross-entropy loss, the Adam update style, and all existing config values (k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0) unchanged, so the effect of the deep tower is isolated.

Hypothesis: the current model can only score a row through a global bias, per-feature linear weights, and rank-k dot products between field embeddings; a shared-embedding MLP can capture higher-order, non-linear combinations (e.g. tab × duration-decile × author-frequency effects that the enriched 9-field encoding exposes but the bilinear form cannot use) and should raise within-user ranking quality (GAUC/nDCG@5) without changing the encoding or objective.

Implementation behavior:
- model.py: keep the class name FM (so train.py's `from model import FM` keeps working) and add an `n_fields` constructor argument, `FM(dim, n_fields, k=16, lr=0.001, l2=1e-6, seed=0, h1=64, h2=32)`. Keep V, W, b and their Adam moments exactly as they are. Add MLP parameters W1 (n_fields*k, h1), b1 (h1,), W2 (h1, h2), b2 (h2,), W3 (h2, 1), b3 (1,), all float32, with their own Adam first/second moment arrays following the existing mV/vV naming pattern. Initialize W1 and W2 with He-style normals (std = sqrt(2 / fan_in)) from the same seeded np.random.default_rng(seed), biases at zero, and initialize W3 and b3 to zeros so the network starts numerically identical to the current FM and learns the deep correction on top of it.
- Forward: in logits(), after computing E = V[X] (B, F, k), S, and the existing FM term, compute d0 = E.reshape(B, F*k), a1 = relu(d0 @ W1 + b1), a2 = relu(a1 @ W2 + b2), deep = (a2 @ W3 + b3).ravel(), and return z = b + W[X].sum(1) + inter + deep (plus whatever intermediates step() needs). predict() keeps its batched signature and behavior.
- Backward in step(): keep g = (sigmoid(z) - y) / B and the existing FM gradients; additionally backpropagate g through the MLP (ReLU masks) to obtain gW3, gb3, gW2, gb2, gW1, gb1 and the embedding-side gradient gd0 = ((g[:,None] * W3.T) masked-back through the layers) @ W1.T, reshaped to (B, F, k), and accumulate it into the same np.add.at(gV, X, ...) call together with the existing FM embedding gradient. Apply the existing self.l2 weight decay to V, W, W1, W2, W3 (not to biases), and extend the existing Adam parameter/moment loop to cover the MLP weights and biases with the same b1=0.9, b2=0.999, eps=1e-8 and bias correction; keep the global bias b on its current plain-SGD update. Return the same pointwise log-loss value.
- Define a module-level tuple in model.py, e.g. PARAM_KEYS = ('V', 'W', 'b', 'W1', 'b1', 'W2', 'b2', 'W3', 'b3'), and use it in Predictor's weight-restore loop (shape + finiteness checks unchanged in spirit) instead of the hardcoded ('V', 'W', 'b'). Predictor must construct FM with n_fields = len(self.features['vocabs']) alongside features['dim'] and config k/lr/l2/seed, and h1/h2 taken from config.
- train.py: import PARAM_KEYS from model, pass n_fields = len(features['vocabs']) and h1/h2 from config at both FM construction sites (fresh and resume), build payload['model_state'] as {key: deepcopy(getattr(model, key)) for key in PARAM_KEYS}, and replace the hardcoded finite-state check tuple with a generic check over every numeric attribute in vars(model) (numpy arrays and float scalars) so the new MLP weights and moments are validated. Leave the resume logic, early stopping on validation primary, atomic save_checkpoint, evaluate() usage, and the train()/load_predictor signatures untouched.
- config.py: add h1=64 and h2=32 to DEFAULTS and include them in the existing integer validation list (must be int >= 1). No other config value changes.
- features.py and requirements.txt unchanged.

Cost expectation: roughly 3-5x the parent's 67s wall clock (a few hundred seconds worst case for the full 40 epochs), comfortably inside candidate_timeout_s=1800 and affordable against the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671470 | 0.537678 | 0.604574 | +0.004132 | 56 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 72 +++++++++++++++++++++++++++++++++++++++++++++++++++++----------
 train.py  | 19 +++++++++++------
 3 files changed, 76 insertions(+), 19 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 147c6ac..4be20d6 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 495d48e..38db7f0 100644
--- a/model.py
+++ b/model.py
@@ -31,37 +31,86 @@ from features import transform
 
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
+PARAM_KEYS = ('V', 'W', 'b', 'W1', 'b1', 'W2', 'b2', 'W3', 'b3')
+
+
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, n_fields, k=16, lr=0.001, l2=1e-6, seed=0, h1=64, h2=32):
         rng = np.random.default_rng(seed)
         self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
         self.b = np.float32(0.0)
         self.lr, self.l2 = lr, l2
+        self.n_fields, self.k, self.h1, self.h2 = n_fields, k, h1, h2
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
+
+        fan_in1 = n_fields * k
+        self.W1 = rng.normal(0, np.sqrt(2.0 / fan_in1), (fan_in1, h1)).astype(np.float32)
+        self.b1 = np.zeros(h1, dtype=np.float32)
+        self.W2 = rng.normal(0, np.sqrt(2.0 / h1), (h1, h2)).astype(np.float32)
+        self.b2 = np.zeros(h2, dtype=np.float32)
+        self.W3 = np.zeros((h2, 1), dtype=np.float32)
+        self.b3 = np.zeros(1, dtype=np.float32)
+
+        self.mW1 = np.zeros_like(self.W1); self.vW1 = np.zeros_like(self.W1)
+        self.mb1 = np.zeros_like(self.b1); self.vb1 = np.zeros_like(self.b1)
+        self.mW2 = np.zeros_like(self.W2); self.vW2 = np.zeros_like(self.W2)
+        self.mb2 = np.zeros_like(self.b2); self.vb2 = np.zeros_like(self.b2)
+        self.mW3 = np.zeros_like(self.W3); self.vW3 = np.zeros_like(self.W3)
+        self.mb3 = np.zeros_like(self.b3); self.vb3 = np.zeros_like(self.b3)
         self.t = 0
 
     def logits(self, X):
         E = self.V[X]                                   # (B,F,k)
         S = E.sum(1)                                    # (B,k)
         inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        B = X.shape[0]
+        d0 = E.reshape(B, -1)
+        z1 = d0 @ self.W1 + self.b1
+        a1 = np.maximum(z1, 0)
+        z2 = a1 @ self.W2 + self.b2
+        a2 = np.maximum(z2, 0)
+        deep = (a2 @ self.W3 + self.b3).ravel()
+        z = self.b + self.W[X].sum(1) + inter + deep
+        return z, E, S, d0, z1, a1, z2, a2
 
     def step(self, X, y):
         B = len(y)
-        z, E, S = self.logits(X)
+        z, E, S, d0, z1, a1, z2, a2 = self.logits(X)
         g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
+
+        gW3 = a2.T @ g[:, None]
+        gb3 = g.sum(keepdims=True)
+        ga2 = g[:, None] * self.W3.T
+        gz2 = ga2 * (z2 > 0)
+        gW2 = a1.T @ gz2
+        gb2 = gz2.sum(0)
+        ga1 = gz2 @ self.W2.T
+        gz1 = ga1 * (z1 > 0)
+        gW1 = d0.T @ gz1
+        gb1 = gz1.sum(0)
+        gd0 = gz1 @ self.W1.T
+        gE_deep = gd0.reshape(E.shape)
+
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
+        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E) + gE_deep)
         gV += self.l2 * self.V; gW += self.l2 * self.W
+        gW1 += self.l2 * self.W1; gW2 += self.l2 * self.W2; gW3 += self.l2 * self.W3
+
         self.t += 1
-        b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M *= b1; M += (1 - b1) * G
-            Vv *= b2; Vv += (1 - b2) * (G * G)
-            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        b1c, b2c, eps = 0.9, 0.999, 1e-8
+        params = (
+            (self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW),
+            (self.W1, gW1, self.mW1, self.vW1), (self.b1, gb1, self.mb1, self.vb1),
+            (self.W2, gW2, self.mW2, self.vW2), (self.b2, gb2, self.mb2, self.vb2),
+            (self.W3, gW3, self.mW3, self.vW3), (self.b3, gb3, self.mb3, self.vb3),
+        )
+        for P, G, M, Vv in params:
+            M *= b1c; M += (1 - b1c) * G
+            Vv *= b2c; Vv += (1 - b2c) * (G * G)
+            P -= self.lr * (M / (1 - b1c ** self.t)) / (np.sqrt(Vv / (1 - b2c ** self.t)) + eps)
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
@@ -85,9 +134,10 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        self.model = FM(self.features['dim'], len(self.features['vocabs']), k=config['k'], lr=config['lr'],
+                         l2=config['l2'], seed=config['seed'], h1=config['h1'], h2=config['h2'])
         weights = state['model_state']
-        for name in ('V', 'W', 'b'):
+        for name in PARAM_KEYS:
             value = weights[name]
             if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
                 raise ValueError('incompatible or nonfinite model weights: ' + name)
diff --git a/train.py b/train.py
index 0451b1a..1ad046f 100644
--- a/train.py
+++ b/train.py
@@ -70,7 +70,7 @@ import numpy as np
 from agent.sandbox.protocol import evaluate
 from config import resolve
 from features import fit, transform
-from model import FM, Predictor, read_checkpoint
+from model import FM, Predictor, read_checkpoint, PARAM_KEYS
 
 
 def save_checkpoint(path, payload):
@@ -98,7 +98,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'],
+                    seed=config['seed'], h1=config['h1'], h2=config['h2'])
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +116,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'],
+                    seed=config['seed'], h1=config['h1'], h2=config['h2'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -131,12 +133,17 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in PARAM_KEYS}
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
-            raise ValueError('nonfinite training state; keeping last valid checkpoint')
+        for key, value in vars(model).items():
+            if isinstance(value, np.ndarray):
+                if not np.isfinite(value).all():
+                    raise ValueError('nonfinite training state; keeping last valid checkpoint')
+            elif isinstance(value, (int, float, np.floating, np.integer)):
+                if not np.isfinite(value):
+                    raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
             rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
         payload['validation'] = validation
```

---

## Iteration 9: `node_009`

**Status** `success` · **Parent** `node_008` · **Commit** `bc72d9c200e0`

### Hypothesis

```text
SELECTED CHANGE
SELECTED CHANGE

Subsystem: loss formulation (untouched anywhere in this lineage: node_007 changed the encoding, node_008 changed the backbone to DeepFM; the only supplied loss experiment, node_001, was a full replacement of the pointwise objective with pairwise BPR on the *genesis* 5-field plain-FM code, its metrics were not supplied, and it is not this parent). Distinction from that closest prior attempt: this experiment does NOT replace the pointwise objective; it keeps the pointwise sigmoid cross-entropy head and ADDS a weighted within-user RankNet (pairwise logistic) term computed in the same optimizer step, sampled globally per epoch with a per-user cap, on the materially different DeepFM + 9-field parent, so the ranking signal now also shapes the shared embeddings feeding the MLP tower.

Hypothesis: GAUC and nDCG@5 are within-user ranking metrics, but the current objective only optimizes globally calibrated pointwise log-loss, which spends capacity on cross-user score calibration that the metric ignores. Adding an explicit within-user pairwise ranking term should directly sharpen intra-user ordering and raise Primary, while keeping the pointwise term for stable, well-conditioned training of the linear/FM/deep components.

Implementation behavior:

model.py
- Change FM.step to the signature `step(self, X, y, Xp=None, Xn=None, lam=0.0)`. Build a single concatenated index matrix `Xall = X` when `Xp is None or len(Xp) == 0 or lam == 0`, otherwise `Xall = np.concatenate([X, Xp, Xn], axis=0)` (all int32, same field count F). Run exactly one forward pass `z, E, S, d0, z1, a1, z2, a2 = self.logits(Xall)`.
- Build the per-row dL/dz vector `g` (float32, length len(Xall)): the first B entries are the existing `(sigmoid(z[:B]) - y) / B`; when pairs are present, let `P = len(Xp)`, `d = z[B:B+P] - z[B+P:]`, `s = sigmoid(d)`, `c = lam * (1.0 - s) / P`; the next P entries are `-c` and the final P entries are `+c`.
- Reuse the existing backward code unchanged in structure, but with `Xall` and this `g`: the MLP backprop (gW3, gb3, gW2, gb2, gW1, gb1, gd0 -> gE_deep), `np.add.at(gW, Xall, g[:, None])`, `np.add.at(gV, Xall, g[:, None, None] * (S[:, None, :] - E) + gE_deep)`, the same l2 decay on V, W, W1, W2, W3, the same single Adam update over the existing params tuple, and the same plain-SGD update `self.b -= self.lr * g.sum()` (the pairwise contributions cancel there, which is correct).
- Return `float(pointwise_logloss + lam * pairwise_logloss)` where pointwise_logloss is the existing expression evaluated on `z[:B]` and pairwise_logloss is `-np.mean(np.log(sigmoid(d) + 1e-9))` (0.0 when no pairs), so train.py logging still gets one finite float.
- Do NOT add any new instance attributes to FM (lam is an argument only), so train.py's `set(state['latest']) != set(vars(model))` resume check, PARAM_KEYS, Predictor, predict, logits, read_checkpoint and load_predictor all stay exactly as they are.

train.py
- After `ytr` is built (both in the fresh and resume paths, i.e. after `Xtr`/`ytr` are available), precompute once: a dict from `r[1]` (user_id) of each training row to its row indices, split into positive indices (ytr == 1) and negative indices (ytr == 0); keep a list `pair_users` of `(pos_idx_array, neg_idx_array)` int32 pairs only for users that have at least one of each class. This uses only training rows and their own labels for pair construction (no validation/test data, no leakage into features).
- At the start of each epoch, after the existing `order = rng.permutation(len(ytr))`, sample pairs with the same `rng`: for each `(pos, neg)` in `pair_users`, `n = min(len(pos), len(neg), config['pairs_cap'])`, take `pos[rng.integers(0, len(pos), n)]` and `neg[rng.integers(0, len(neg), n)]` (sampling with replacement for speed); concatenate into `P_pos`, `P_neg`, then apply one shared `rng.permutation` to shuffle the pairs.
- Distribute pairs evenly across the epoch's minibatches: with `n_batches = ceil(len(order) / config['bs'])` and `chunk = max(1, ceil(len(P_pos) / n_batches))`, the j-th minibatch (j starting at 0) uses pair slice `P_pos[j*chunk:(j+1)*chunk]` and `P_neg[j*chunk:(j+1)*chunk]`, and calls `model.step(Xtr[batch_idx], ytr[batch_idx], Xtr[pp], Xtr[pn], config['lam'])`. If `len(P_pos) == 0`, pass `None, None, 0.0`.
- Everything else in train.py is untouched: transform usage, validation via `evaluate` on the frozen valid rows, early stopping on validation primary with patience, best-weight capture over PARAM_KEYS, nonfinite-state checks, atomic save_checkpoint, resume logic, and the `train(...)` signature.

config.py
- Add `lam=1.0` and `pairs_cap=10` to DEFAULTS. Add `'pairs_cap'` to the integer validation tuple (int >= 1) and `'lam'` to the float validation loop (must be finite and >= 0; the existing `key == 'lr'` nonzero exception keeps lam=0 legal as an ablation). No other config value changes: k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32 stay as they are.

features.py and requirements.txt are unchanged.

Cost: the forward/backward per step grows from B rows to at most B + 2*chunk rows (pairs are capped at 10 per user per epoch), so expect roughly 2-3x the parent's 56s wall clock (~150s worst case), comfortably inside candidate_timeout_s=1800 and affordable against the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668137 | 0.536289 | 0.602213 | -0.002361 | 59 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  7 ++++---
 model.py  | 33 +++++++++++++++++++++++++--------
 train.py  | 38 ++++++++++++++++++++++++++++++++++++--
 3 files changed, 65 insertions(+), 13 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 4be20d6..6a35a16 100644
--- a/config.py
+++ b/config.py
@@ -22,18 +22,19 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32,
+                 lam=1.0, pairs_cap=10)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2', 'pairs_cap'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
-    for key in ('lr', 'l2'):
+    for key in ('lr', 'l2', 'lam'):
         if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
             raise ValueError(f'invalid {key}')
     return config
diff --git a/model.py b/model.py
index 38db7f0..13f97b8 100644
--- a/model.py
+++ b/model.py
@@ -75,10 +75,26 @@ class FM:
         z = self.b + self.W[X].sum(1) + inter + deep
         return z, E, S, d0, z1, a1, z2, a2
 
-    def step(self, X, y):
+    def step(self, X, y, Xp=None, Xn=None, lam=0.0):
         B = len(y)
-        z, E, S, d0, z1, a1, z2, a2 = self.logits(X)
-        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
+        if Xp is None or len(Xp) == 0 or lam == 0:
+            Xall = X.astype(np.int32)
+            P = 0
+        else:
+            Xall = np.concatenate([X, Xp, Xn], axis=0).astype(np.int32)
+            P = len(Xp)
+        z, E, S, d0, z1, a1, z2, a2 = self.logits(Xall)
+
+        g = np.zeros(len(Xall), dtype=np.float32)
+        g[:B] = ((sigmoid(z[:B]) - y) / B).astype(np.float32)
+        pairwise_logloss = 0.0
+        if P > 0:
+            d = z[B:B + P] - z[B + P:]
+            s = sigmoid(d)
+            c = (lam * (1.0 - s) / P).astype(np.float32)
+            g[B:B + P] = -c
+            g[B + P:] = c
+            pairwise_logloss = -np.mean(np.log(sigmoid(d) + 1e-9))
 
         gW3 = a2.T @ g[:, None]
         gb3 = g.sum(keepdims=True)
@@ -94,8 +110,8 @@ class FM:
         gE_deep = gd0.reshape(E.shape)
 
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
-        np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E) + gE_deep)
+        np.add.at(gW, Xall, g[:, None])
+        np.add.at(gV, Xall, g[:, None, None] * (S[:, None, :] - E) + gE_deep)
         gV += self.l2 * self.V; gW += self.l2 * self.W
         gW1 += self.l2 * self.W1; gW2 += self.l2 * self.W2; gW3 += self.l2 * self.W3
 
@@ -107,12 +123,13 @@ class FM:
             (self.W2, gW2, self.mW2, self.vW2), (self.b2, gb2, self.mb2, self.vb2),
             (self.W3, gW3, self.mW3, self.vW3), (self.b3, gb3, self.mb3, self.vb3),
         )
-        for P, G, M, Vv in params:
+        for P_, G, M, Vv in params:
             M *= b1c; M += (1 - b1c) * G
             Vv *= b2c; Vv += (1 - b2c) * (G * G)
-            P -= self.lr * (M / (1 - b1c ** self.t)) / (np.sqrt(Vv / (1 - b2c ** self.t)) + eps)
+            P_ -= self.lr * (M / (1 - b1c ** self.t)) / (np.sqrt(Vv / (1 - b2c ** self.t)) + eps)
         self.b -= self.lr * g.sum()
-        return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
+        pointwise_logloss = -np.mean(y * np.log(sigmoid(z[:B]) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z[:B]) + 1e-9))
+        return float(pointwise_logloss + lam * pairwise_logloss)
 
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
diff --git a/train.py b/train.py
index 1ad046f..faaf93e 100644
--- a/train.py
+++ b/train.py
@@ -124,12 +124,46 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     Xtr = transform(train_rows, features)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
+
+    user_rows = {}
+    for idx, r in enumerate(train_rows):
+        user_rows.setdefault(r[1], []).append(idx)
+    pair_users = []
+    for uid, idxs in user_rows.items():
+        idxs = np.asarray(idxs, dtype=np.int32)
+        pos = idxs[ytr[idxs] == 1]
+        neg = idxs[ytr[idxs] == 0]
+        if len(pos) > 0 and len(neg) > 0:
+            pair_users.append((pos, neg))
+
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
         order = rng.permutation(len(ytr))
-        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                  for i in range(0, len(order), config['bs'])]
+
+        pos_list, neg_list = [], []
+        for pos, neg in pair_users:
+            n = min(len(pos), len(neg), config['pairs_cap'])
+            pos_list.append(pos[rng.integers(0, len(pos), n)])
+            neg_list.append(neg[rng.integers(0, len(neg), n)])
+        P_pos = np.concatenate(pos_list).astype(np.int32) if pos_list else np.empty(0, dtype=np.int32)
+        P_neg = np.concatenate(neg_list).astype(np.int32) if neg_list else np.empty(0, dtype=np.int32)
+        if len(P_pos) > 0:
+            perm = rng.permutation(len(P_pos))
+            P_pos, P_neg = P_pos[perm], P_neg[perm]
+
+        n_batches = -(-len(order) // config['bs'])
+        chunk = max(1, -(-len(P_pos) // n_batches)) if len(P_pos) > 0 else 1
+
+        losses = []
+        for j, i in enumerate(range(0, len(order), config['bs'])):
+            batch_idx = order[i:i + config['bs']]
+            if len(P_pos) == 0:
+                pp, pn = None, None
+            else:
+                pp = Xtr[P_pos[j * chunk:(j + 1) * chunk]]
+                pn = Xtr[P_neg[j * chunk:(j + 1) * chunk]]
+            losses.append(model.step(Xtr[batch_idx], ytr[batch_idx], pp, pn, config['lam'] if pp is not None else 0.0))
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

---

## Iteration 10: `node_010`

**Status** `success` · **Parent** `node_008` · **Commit** `c70a33c617ca`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature engineering subsystem, label-based prior-history encoding — materially different from the only supplied feature experiment, node_007, which added label-free exposure-count buckets, and from sibling node_009, which changed the loss; no supplied attempt has used target/label statistics of any kind): add two new categorical fields to features.py that encode each video's and each author's smoothed historical long_view rate computed ONLY from training rows on strictly earlier dates, leaving model.py, train.py, config.py and requirements.txt logically unchanged (DeepFM backbone, pointwise loss, k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32 all stay exactly as they are) so the effect of the encoding is isolated.

Hypothesis: GAUC and nDCG@5 are within-user metrics, so only features that vary across the candidate items of a single user can move them; the current 9 fields give the model raw video/author IDs and label-free exposure counts, but no direct estimate of how likely an item is to be long-viewed. A smoothed, strictly-prior-history long_view rate for video and author is the strongest item-side ranking signal and should sharpen intra-user ordering, especially for mid-frequency items whose ID embeddings are undertrained.

Implementation behavior (features.py only):
- fit(rows) keeps everything it currently computes (duration quantile edges, user_counts, video_counts, author_counts) and additionally builds day-indexed prior-history statistics. Build dates = sorted({str(r[0]) for r in rows}) and date_index = {d: i for i, d in enumerate(dates)}. Compute prior_mean = mean of float(r[6]) over training rows. If any row has len(row) <= 6 (no label), leave the history dicts empty and fall back to the 'new' token everywhere, so the module never requires labels at inference time.
- For each of the two id types video (row[2]) and author (row[3]): accumulate per-(id, day_index) totals and positive sums over the training rows; then, per id, walk its day indices in ascending order keeping running sums of the STRICTLY EARLIER days and store train_token[(id, day_index)] = token(prior_pos, prior_tot); also store final_token[id] = token(total_pos_over_all_train_days, total_count_over_all_train_days).
- token(p, t): return 'new' when t == 0; otherwise rate = (p + 20.0 * prior_mean) / (t + 20.0), b = min(int(rate * 16), 15), and return f'{b}|' + freq_bucket(t) (reuse the existing freq_bucket helper) so the token carries both the estimated rate bin and the support level, letting the model discount noisy low-support estimates.
- Add a helper hist_token(state, kind, ident, date): di = state['date_index'].get(str(date)); if di is None (validation/test dates, which are strictly after the training period) return final_token.get(ident, 'new'); otherwise return train_token.get((ident, di), 'new'). This guarantees a row's own label and all same-day labels are excluded from its features (no leakage), while validation rows correctly see the full training-period statistics.
- raw(row, state) now returns 11 strings: the existing 9 in the same order, then (9) 'vr' + hist_token(state, 'video', row[2], row[0]) and (10) 'ar' + hist_token(state, 'author', row[3], row[0]). Do not add a user-level rate field (it is constant within a ranking group and cannot change GAUC/nDCG@5).
- fit builds vocabs for 11 fields (vocabs = [{} for _ in range(11)] or len(raw(...))-driven), keeps dims = [len(v)+1 for v in vocabs], offsets = np.cumsum([0] + dims[:-1]).astype(np.int32), dim = sum(dims), and stores date_index, prior_mean, and the four token dicts in the returned state. All state must stay picklable (plain dicts with str/tuple keys, numpy arrays) so train.py's single-checkpoint payload, resume logic, and model.Predictor keep working unchanged.
- transform(rows, state) keeps its signature and behavior; it already allocates len(state['vocabs']) columns and maps unseen values to the per-field OOV slot vocab.get(value, len(vocab)) + offsets[i], so unseen ids and unseen tokens are handled.

Nothing downstream needs editing: model.FM/logits/step handle any field count, train.py and Predictor already pass n_fields = len(features['vocabs']) and dim = features['dim'], so the MLP input width adapts automatically. Expected cost is roughly 1.5-2.5x the parent's 56s wall clock (one extra O(N) statistics pass in fit plus two dict lookups per row in raw), comfortably inside candidate_timeout_s=1800 and affordable against the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670462 | 0.536947 | 0.603704 | -0.000869 | 66 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 63 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 1 file changed, 61 insertions(+), 2 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 5b1da2d..3c4b879 100644
--- a/features.py
+++ b/features.py
@@ -32,6 +32,21 @@ def freq_bucket(count):
     return str(min(int(np.floor(np.log2(count))), 20))
 
 
+def token(p, t, prior_mean):
+    if t == 0:
+        return 'new'
+    rate = (p + 20.0 * prior_mean) / (t + 20.0)
+    b = min(int(rate * 16), 15)
+    return f'{b}|' + freq_bucket(t)
+
+
+def hist_token(state, kind, ident, date):
+    di = state['date_index'].get(str(date))
+    if di is None:
+        return state[kind + '_final_token'].get(ident, 'new')
+    return state[kind + '_train_token'].get((ident, di), 'new')
+
+
 def raw(row, state):
     duration_decile = str(int(np.searchsorted(state['edges'], row[5])))
     return [
@@ -44,9 +59,38 @@ def raw(row, state):
         'vc' + freq_bucket(state['video_counts'].get(row[2], 0)),
         'ac' + freq_bucket(state['author_counts'].get(row[3], 0)),
         'td' + str(row[4]) + '|' + duration_decile,
+        'vr' + hist_token(state, 'video', row[2], row[0]),
+        'ar' + hist_token(state, 'author', row[3], row[0]),
     ]
 
 
+def _build_history(rows, date_index, prior_mean, id_index):
+    totals = {}
+    positives = {}
+    for r in rows:
+        ident = r[id_index]
+        di = date_index[str(r[0])]
+        key = (ident, di)
+        totals[key] = totals.get(key, 0) + 1
+        positives[key] = positives.get(key, 0) + float(r[6])
+    per_id_days = {}
+    for (ident, di) in totals:
+        per_id_days.setdefault(ident, []).append(di)
+    train_token = {}
+    final_token = {}
+    for ident, days in per_id_days.items():
+        days = sorted(set(days))
+        running_pos = 0.0
+        running_tot = 0
+        for di in days:
+            train_token[(ident, di)] = token(running_pos, running_tot, prior_mean)
+            key = (ident, di)
+            running_pos += positives.get(key, 0.0)
+            running_tot += totals.get(key, 0)
+        final_token[ident] = token(running_pos, running_tot, prior_mean)
+    return train_token, final_token
+
+
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
     user_counts, video_counts, author_counts = {}, {}, {}
@@ -54,9 +98,24 @@ def fit(rows):
         user_counts[r[1]] = user_counts.get(r[1], 0) + 1
         video_counts[r[2]] = video_counts.get(r[2], 0) + 1
         author_counts[r[3]] = author_counts.get(r[3], 0) + 1
+
+    dates = sorted({str(r[0]) for r in rows})
+    date_index = {d: i for i, d in enumerate(dates)}
+    has_labels = all(len(r) > 6 for r in rows)
+    if has_labels:
+        prior_mean = float(np.mean([float(r[6]) for r in rows]))
+        video_train_token, video_final_token = _build_history(rows, date_index, prior_mean, 2)
+        author_train_token, author_final_token = _build_history(rows, date_index, prior_mean, 3)
+    else:
+        prior_mean = 0.0
+        video_train_token, video_final_token = {}, {}
+        author_train_token, author_final_token = {}, {}
+
     state = dict(edges=edges, user_counts=user_counts, video_counts=video_counts,
-                 author_counts=author_counts)
-    vocabs = [{} for _ in range(9)]
+                 author_counts=author_counts, date_index=date_index, prior_mean=prior_mean,
+                 video_train_token=video_train_token, video_final_token=video_final_token,
+                 author_train_token=author_train_token, author_final_token=author_final_token)
+    vocabs = [{} for _ in range(11)]
     for row in rows:
         for i, value in enumerate(raw(row, state)):
             if value not in vocabs[i]:
```

---

## Iteration 11: `node_011`

**Status** `success` · **Parent** `node_008` · **Commit** `f9b8472f95cd`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model backbone subsystem — the only direction that has produced a gain in this lineage: node_007→node_008 added the DeepFM MLP tower for +0.0041, while both supplied siblings from this same parent regressed, node_009 with an added pairwise RankNet loss term (0.60221) and node_010 with label-based prior-history video/author rate fields (0.60370)). Distinction from the closest prior attempt: node_008 added an *implicit* additive MLP tower over the concatenated field embeddings; this experiment adds an explicit *multiplicative* DCN-V2-style cross network in parallel with that MLP, leaving the MLP, the 9-field encoding, the pointwise sigmoid cross-entropy loss and every config value untouched. No supplied experiment has added a cross network anywhere in this run.

Hypothesis: the current scorer combines a bilinear rank-k FM term and a ReLU MLP; neither represents explicit bounded-degree multiplicative feature crosses efficiently (e.g. duration-decile × author-frequency × tab), which are exactly the item-varying interactions that decide within-user ordering. A DCN-V2 cross network on the same shared embeddings should add these high-order crosses cheaply and raise GAUC/nDCG@5.

Implementation behavior (model.py only; train.py, config.py, features.py, requirements.txt unchanged in logic — train.py already imports PARAM_KEYS, saves {key: deepcopy(getattr(model,key)) for key in PARAM_KEYS}, and validates all numeric attributes in vars(model), and Predictor already loops over PARAM_KEYS, so no edits are required there):
- In FM.__init__, after the existing MLP parameters, set D = n_fields * k and add two cross layers plus a linear head, all float32, drawn from the same seeded rng: Wx0 = rng.normal(0, 1/sqrt(D), (D, D)), bx0 = zeros(D), Wx1 = rng.normal(0, 1/sqrt(D), (D, D)), bx1 = zeros(D), Wxo = zeros((D, 1)), bxo = zeros(1). Zero-initializing Wxo/bxo makes the model start numerically identical to the current DeepFM so the cross correction is learned on top. Add matching Adam first/second moment arrays following the existing naming pattern (mWx0/vWx0, mbx0/vbx0, mWx1/vWx1, mbx1/vbx1, mWxo/vWxo, mbxo/vbxo).
- Extend the module constant to PARAM_KEYS = ('V','W','b','W1','b1','W2','b2','W3','b3','Wx0','bx0','Wx1','bx1','Wxo','bxo').
- Forward in logits(X): keep everything as is (E, S, inter, d0, z1, a1, z2, a2, deep) and additionally compute x0 = d0; u0 = x0 @ Wx0 + bx0; x1 = x0 * u0 + x0; u1 = x1 @ Wx1 + bx1; x2 = x0 * u1 + x1; cross = (x2 @ Wxo + bxo).ravel(); return z = b + W[X].sum(1) + inter + deep + cross, extending the returned tuple with (u0, x1, u1, x2). predict() keeps its current signature and continues to take element [0].
- Backward in step(): keep g = (sigmoid(z) - y)/B and the existing FM and MLP gradients (producing gd0 from the MLP path). Add the cross-network gradients: gWxo = x2.T @ g[:,None]; gbxo = g.sum(keepdims=True); dx2 = g[:,None] * Wxo.T; du1 = dx2 * x0; gWx1 = x1.T @ du1; gbx1 = du1.sum(0); dx1 = du1 @ Wx1.T + dx2; du0 = dx1 * x0; gWx0 = x0.T @ du0; gbx0 = du0.sum(0); dx0 = dx2 * u1 + du0 @ Wx0.T + dx1 * u0 + dx1. Then form the embedding-side gradient as gE_extra = (gd0 + dx0).reshape(E.shape) and use it in the single existing np.add.at(gV, X, g[:,None,None] * (S[:,None,:] - E) + gE_extra) call.
- Apply the existing self.l2 weight decay to Wx0, Wx1 and Wxo (not to the cross biases), and extend the existing Adam params tuple to update Wx0, bx0, Wx1, bx1, Wxo, bxo with the same b1c=0.9, b2c=0.999, eps=1e-8 and bias correction; keep the global bias b on its plain-SGD update and return the same pointwise log-loss value.
- Do not change the number of fields, the loss, or any config value (k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32 all stay).

Cost: two extra (8192,144)@(144,144) matmuls forward and their backward counterparts per minibatch; expect roughly 1.5-2.5x the parent's 56s wall clock (~150s worst case), comfortably inside candidate_timeout_s=1800 and affordable against the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671678 | 0.537908 | 0.604793 | +0.000219 | 77 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
model.py | 53 +++++++++++++++++++++++++++++++++++++++++++++++------
 1 file changed, 47 insertions(+), 6 deletions(-)
```

```diff
diff --git a/model.py b/model.py
index 38db7f0..0399a21 100644
--- a/model.py
+++ b/model.py
@@ -31,7 +31,7 @@ from features import transform
 
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
-PARAM_KEYS = ('V', 'W', 'b', 'W1', 'b1', 'W2', 'b2', 'W3', 'b3')
+PARAM_KEYS = ('V', 'W', 'b', 'W1', 'b1', 'W2', 'b2', 'W3', 'b3', 'Wx0', 'bx0', 'Wx1', 'bx1', 'Wxo', 'bxo')
 
 
 class FM:
@@ -59,6 +59,21 @@ class FM:
         self.mb2 = np.zeros_like(self.b2); self.vb2 = np.zeros_like(self.b2)
         self.mW3 = np.zeros_like(self.W3); self.vW3 = np.zeros_like(self.W3)
         self.mb3 = np.zeros_like(self.b3); self.vb3 = np.zeros_like(self.b3)
+
+        D = n_fields * k
+        self.Wx0 = rng.normal(0, 1 / np.sqrt(D), (D, D)).astype(np.float32)
+        self.bx0 = np.zeros(D, dtype=np.float32)
+        self.Wx1 = rng.normal(0, 1 / np.sqrt(D), (D, D)).astype(np.float32)
+        self.bx1 = np.zeros(D, dtype=np.float32)
+        self.Wxo = np.zeros((D, 1), dtype=np.float32)
+        self.bxo = np.zeros(1, dtype=np.float32)
+
+        self.mWx0 = np.zeros_like(self.Wx0); self.vWx0 = np.zeros_like(self.Wx0)
+        self.mbx0 = np.zeros_like(self.bx0); self.vbx0 = np.zeros_like(self.bx0)
+        self.mWx1 = np.zeros_like(self.Wx1); self.vWx1 = np.zeros_like(self.Wx1)
+        self.mbx1 = np.zeros_like(self.bx1); self.vbx1 = np.zeros_like(self.bx1)
+        self.mWxo = np.zeros_like(self.Wxo); self.vWxo = np.zeros_like(self.Wxo)
+        self.mbxo = np.zeros_like(self.bxo); self.vbxo = np.zeros_like(self.bxo)
         self.t = 0
 
     def logits(self, X):
@@ -72,12 +87,20 @@ class FM:
         z2 = a1 @ self.W2 + self.b2
         a2 = np.maximum(z2, 0)
         deep = (a2 @ self.W3 + self.b3).ravel()
-        z = self.b + self.W[X].sum(1) + inter + deep
-        return z, E, S, d0, z1, a1, z2, a2
+
+        x0 = d0
+        u0 = x0 @ self.Wx0 + self.bx0
+        x1 = x0 * u0 + x0
+        u1 = x1 @ self.Wx1 + self.bx1
+        x2 = x0 * u1 + x1
+        cross = (x2 @ self.Wxo + self.bxo).ravel()
+
+        z = self.b + self.W[X].sum(1) + inter + deep + cross
+        return z, E, S, d0, z1, a1, z2, a2, u0, x1, u1, x2
 
     def step(self, X, y):
         B = len(y)
-        z, E, S, d0, z1, a1, z2, a2 = self.logits(X)
+        z, E, S, d0, z1, a1, z2, a2, u0, x1, u1, x2 = self.logits(X)
         g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
 
         gW3 = a2.T @ g[:, None]
@@ -91,13 +114,28 @@ class FM:
         gW1 = d0.T @ gz1
         gb1 = gz1.sum(0)
         gd0 = gz1 @ self.W1.T
-        gE_deep = gd0.reshape(E.shape)
+        x0 = d0
+
+        gWxo = x2.T @ g[:, None]
+        gbxo = g.sum(keepdims=True)
+        dx2 = g[:, None] * self.Wxo.T
+        du1 = dx2 * x0
+        gWx1 = x1.T @ du1
+        gbx1 = du1.sum(0)
+        dx1 = du1 @ self.Wx1.T + dx2
+        du0 = dx1 * x0
+        gWx0 = x0.T @ du0
+        gbx0 = du0.sum(0)
+        dx0 = dx2 * u1 + du0 @ self.Wx0.T + dx1 * u0 + dx1
+
+        gE_extra = (gd0 + dx0).reshape(E.shape)
 
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E) + gE_deep)
+        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E) + gE_extra)
         gV += self.l2 * self.V; gW += self.l2 * self.W
         gW1 += self.l2 * self.W1; gW2 += self.l2 * self.W2; gW3 += self.l2 * self.W3
+        gWx0 += self.l2 * self.Wx0; gWx1 += self.l2 * self.Wx1; gWxo += self.l2 * self.Wxo
 
         self.t += 1
         b1c, b2c, eps = 0.9, 0.999, 1e-8
@@ -106,6 +144,9 @@ class FM:
             (self.W1, gW1, self.mW1, self.vW1), (self.b1, gb1, self.mb1, self.vb1),
             (self.W2, gW2, self.mW2, self.vW2), (self.b2, gb2, self.mb2, self.vb2),
             (self.W3, gW3, self.mW3, self.vW3), (self.b3, gb3, self.mb3, self.vb3),
+            (self.Wx0, gWx0, self.mWx0, self.vWx0), (self.bx0, gbx0, self.mbx0, self.vbx0),
+            (self.Wx1, gWx1, self.mWx1, self.vWx1), (self.bx1, gbx1, self.mbx1, self.vbx1),
+            (self.Wxo, gWxo, self.mWxo, self.vWxo), (self.bxo, gbxo, self.mbxo, self.vbxo),
         )
         for P, G, M, Vv in params:
             M *= b1c; M += (1 - b1c) * G
```

---

## Iteration 12: `node_012`

**Status** `success` · **Parent** `node_011` · **Commit** `0c440efc2d27`

### Hypothesis

```text
SELECTED CHANGE
Experiment (optimization-hyperparameter subsystem — completely untouched anywhere in this lineage; every node from genesis through node_011 kept the original FM-era config values k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0 while the backbone grew into DeepFM + DCN-V2 cross network, and the two feature experiments (node_007, node_010) and the two loss experiments (node_001 BPR, node_009 RankNet) all failed to help; the last two backbone edits are also showing diminishing returns, +0.0041 then +0.0002): reduce the minibatch size from 8192 to 2048 in config.py and change nothing else.

Hypothesis: the current DeepFM+cross model performs only ~len(train_rows)/8192 Adam updates per epoch, an update budget inherited from the much simpler pure-FM genesis model. With a batch size of 2048 the model takes 4x more Adam steps per epoch on the same data, which both lets the sparse ID embeddings and the two 144x144 cross layers actually converge within the 40-epoch/patience-4 envelope and injects more gradient noise (a mild regularizer for the large embedding table). This should improve within-user discrimination and therefore GAUC and nDCG@5, and it also effectively strengthens the currently negligible l2=1e-6 pressure since the decay term is applied once per step.

Implementation behavior:
- config.py only: in DEFAULTS change bs=8192 to bs=2048. Leave k=16, lr=0.001, l2=1e-6, epochs=40, patience=4, seed=0, h1=64, h2=32 exactly as they are, and leave the resolve() validation logic (bs still validated as int >= 1) unchanged.
- features.py, model.py, train.py and requirements.txt are unchanged: train.py already reads config['bs'] for both the minibatch loop and checkpoint payload, the 9-field encoding, the pointwise sigmoid cross-entropy loss, the FM+MLP+DCN-V2 forward/backward, PARAM_KEYS serialization, early stopping on validation primary, and the train()/load_predictor contracts all stay exactly as supplied.

Distinction from the closest supplied prior attempt: no experiment in this lineage or among the supplied siblings has altered any config.py value; the only hyperparameter-related memory entries are optimizer edits observed on other branches from a materially different (pre-DeepFM, pre-cross-network) code state, and none of them changed the batch size on this backbone. This is a single-variable optimization-budget test, not another feature, loss, or architecture variant.

Cost expectation: same total FLOPs per epoch with 4x more per-batch call overhead and less efficient BLAS shapes, i.e. roughly 1.5-2.5x the parent's 77s wall clock (~120-200s worst case), comfortably inside candidate_timeout_s=1800 and a small fraction of the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669565 | 0.536819 | 0.603192 | -0.001601 | 86 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

```diff
diff --git a/config.py b/config.py
index 4be20d6..36186e2 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=2048, patience=4, seed=0, h1=64, h2=32)
 
 
 def resolve(overrides):
```

---

## Iteration 13: `node_013`

**Status** `success` · **Parent** `node_011` · **Commit** `8bad68eb3525`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss-weighting / objective-alignment subsystem — new for this lineage): keep the pointwise sigmoid cross-entropy loss and the current FM + DeepFM-MLP + DCN-V2 backbone exactly as they are, but weight each training row inversely to its user's training impression count so the training objective matches the per-user averaging used by GAUC and nDCG@5.

Hypothesis: the metric averages ranking quality per user group, while the current loss sums equally over rows, so heavy-impression users dominate the gradient and the model is tuned mostly for them. Down-weighting rows from high-frequency users (and up-weighting sparse users) should improve average within-user ordering. This is materially different from the two supplied loss experiments (node_009 added a pairwise RankNet term from this same parent, node_001 added BPR from genesis) — the loss form, the pairwise/pointwise structure, and the model are unchanged; only per-sample weights in the existing log-loss change. No supplied experiment has altered sample weighting, and this does not touch batch size (node_012, refuted).

Implementation behavior:
- config.py: add `uwp=0.5` to DEFAULTS (user-weight power). Validate it alongside the existing float checks: it must be a finite float (int accepted, cast to float) with 0.0 <= uwp <= 1.0, raising ValueError('invalid uwp') otherwise. Leave k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32 unchanged.
- model.py: change FM.step to `step(self, X, y, w=None)`. When w is None, use np.ones(len(y), dtype=np.float32). Compute g = ((sigmoid(z) - y) * w / B).astype(np.float32) and leave every downstream gradient expression, the l2 decay, the Adam update loop, the global-bias SGD update, and PARAM_KEYS exactly as they are (all gradients already flow from g, so no other formula changes). Return the weighted log-loss float(-np.sum(w * (y*np.log(sigmoid(z)+1e-9) + (1-y)*np.log(1-sigmoid(z)+1e-9))) / B). Do not change logits(), predict(), Predictor, read_checkpoint, or load_predictor.
- train.py: after building Xtr/ytr, compute per-row weights from the training-fitted counts already present in features_state: counts = np.array([features['user_counts'].get(r[1], 1) for r in train_rows], dtype=np.float64); wtr = (1.0 / np.maximum(counts, 1.0) ** config['uwp']); then normalize so the mean weight is exactly 1.0 (wtr *= len(wtr) / wtr.sum()) and cast to np.float32, so the effective gradient scale and learning rate stay comparable to the parent. Pass the matching slice into the training call: model.step(Xtr[idx], ytr[idx], wtr[idx]) where idx = order[i:i+config['bs']]. Weights are recomputed deterministically on both fresh and resume paths (no new model attributes, so vars(model) and the resume/state validation stay compatible). Validation, evaluate() usage, early stopping on validation primary, atomic checkpoint saving, PARAM_KEYS serialization, and the train()/load_predictor signatures are unchanged. No validation-row statistics and no labels are used to build the weights.
- features.py and requirements.txt unchanged.

Cost: weight computation is O(n) once; per-batch cost is one extra elementwise multiply, so wall clock should stay near the parent's ~77s, far inside candidate_timeout_s=1800.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669645 | 0.536744 | 0.603195 | -0.001598 | 76 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py | 6 +++++-
 model.py  | 8 +++++---
 train.py  | 6 +++++-
 3 files changed, 15 insertions(+), 5 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 4be20d6..15d8979 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32, uwp=0.5)
 
 
 def resolve(overrides):
@@ -36,4 +36,8 @@ def resolve(overrides):
     for key in ('lr', 'l2'):
         if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
             raise ValueError(f'invalid {key}')
+    uwp = config['uwp']
+    if type(uwp) not in (int, float) or not math.isfinite(float(uwp)) or not (0.0 <= float(uwp) <= 1.0):
+        raise ValueError('invalid uwp')
+    config['uwp'] = float(uwp)
     return config
diff --git a/model.py b/model.py
index 0399a21..275da1d 100644
--- a/model.py
+++ b/model.py
@@ -98,10 +98,12 @@ class FM:
         z = self.b + self.W[X].sum(1) + inter + deep + cross
         return z, E, S, d0, z1, a1, z2, a2, u0, x1, u1, x2
 
-    def step(self, X, y):
+    def step(self, X, y, w=None):
         B = len(y)
+        if w is None:
+            w = np.ones(len(y), dtype=np.float32)
         z, E, S, d0, z1, a1, z2, a2, u0, x1, u1, x2 = self.logits(X)
-        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
+        g = ((sigmoid(z) - y) * w / B).astype(np.float32)    # (B,)
 
         gW3 = a2.T @ g[:, None]
         gb3 = g.sum(keepdims=True)
@@ -153,7 +155,7 @@ class FM:
             Vv *= b2c; Vv += (1 - b2c) * (G * G)
             P -= self.lr * (M / (1 - b1c ** self.t)) / (np.sqrt(Vv / (1 - b2c ** self.t)) + eps)
         self.b -= self.lr * g.sum()
-        return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
+        return float(-np.sum(w * (y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9))) / B)
 
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
diff --git a/train.py b/train.py
index 1ad046f..afacdc2 100644
--- a/train.py
+++ b/train.py
@@ -124,11 +124,15 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     Xtr = transform(train_rows, features)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
+    counts = np.array([features['user_counts'].get(r[1], 1) for r in train_rows], dtype=np.float64)
+    wtr = (1.0 / np.maximum(counts, 1.0) ** config['uwp'])
+    wtr *= len(wtr) / wtr.sum()
+    wtr = wtr.astype(np.float32)
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
         order = rng.permutation(len(ytr))
-        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
+        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]], wtr[order[i:i + config['bs']]])
                   for i in range(0, len(order), config['bs'])]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
```

---

## Iteration 14: `node_014`

**Status** `success` · **Parent** `node_011` · **Commit** `fcf6f1afed9e`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem, applied on top of the current DeepFM + DCN-V2 backbone): add user-relative duration encoding to features.py so the model gets item-varying, label-free signals that can actually change within-user ordering. Rationale: GAUC and nDCG@5 are computed inside user groups, so purely user-level or globally-shifting signals cannot help; what matters is how an impression's item differs from the user's other candidates. The current 9-field encoding only has a coarse 10-bin absolute duration decile (plus tab x decile) as an item-side numeric signal, and the two most recent backbone edits are showing diminishing returns (+0.0041 then +0.0002) while loss changes (BPR node_001, RankNet node_009), sample weighting (node_013) and batch-size (node_012) all regressed. Hypothesis: whether a video's length is longer or shorter than the user's typical exposed length, at finer duration resolution, is a strong predictor of long_view that the present encoding cannot express.

Edit features.py only (model.py, train.py, config.py, requirements.txt unchanged; model.FM already derives D = n_fields * k and Predictor/train pass n_fields = len(features_state['vocabs']), so the wider encoding flows through automatically).

Implementation behavior:
- Add a module-level constant REL_EDGES = np.array([-2.0, -1.5, -1.0, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1.0, 1.5, 2.0], dtype=np.float64) and a helper log_dur(ms) returning float(np.log2(max(float(ms), 0.0) + 1.0)).
- In fit(rows), keep the existing 10-bin edges and the three exposure-count dicts exactly as they are, and additionally compute (training rows only, no labels used): fine_edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 41)[1:-1]) (40 duration bins); per-user sums/counts of log_dur(r[5]) to build user_logd = {user_id: mean log duration}; and global_logd = mean of log_dur over all training rows (fallback for users unseen in training). Store fine_edges, user_logd and global_logd in the returned state dict alongside edges, user_counts, video_counts, author_counts, vocabs, offsets, dim; everything must stay picklable for train.py's single-checkpoint payload.
- In raw(row, state), keep the current 9 field strings unchanged and append exactly three new strings, giving 12 fields in this order: (9) 'q' + str(int(np.searchsorted(state['fine_edges'], row[5]))); (10) 'r' + rel_b where rel = log_dur(row[5]) - state['user_logd'].get(row[1], state['global_logd']) and rel_b = str(int(np.searchsorted(REL_EDGES, rel))); (11) 'rt' + str(row[4]) + '|' + rel_b (tab-conditioned relative-length bucket).
- Change the vocab construction to [{} for _ in range(12)]; keep dims = [len(v) + 1 for v in vocabs], offsets = np.cumsum([0] + dims[:-1]).astype(np.int32), dim = sum(dims), and keep transform()'s existing signature, row order, dynamic column count len(state['vocabs']) and unseen-value handling vocab.get(value, len(vocab)) + offsets[i] so unseen users fall back to the global mean and unseen buckets land in the per-field OOV slot.
- No date-derived feature, no label-derived or post-outcome statistic of any kind; all statistics are fitted on training rows only and reused unchanged for validation/inference.

Distinction from the closest supplied prior attempts: node_007 added exposure-frequency buckets and a tab x duration-decile conjunction (already present in this parent), and node_010 (a sibling of node_008) added label-based prior-history video/author rates and regressed; no supplied experiment has used user-level duration statistics, a signed user-relative duration bucket, or finer-than-decile duration quantiles.

Cost: field count 9 -> 12 grows the cross/MLP input width D from 144 to 192, roughly 1.5x the parent's 77s wall clock (~120s), comfortably inside candidate_timeout_s = 1800 and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669647 | 0.536898 | 0.603272 | -0.001520 | 98 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 27 ++++++++++++++++++++++++---
 1 file changed, 24 insertions(+), 3 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 5b1da2d..59c624a 100644
--- a/features.py
+++ b/features.py
@@ -25,6 +25,12 @@ while preserving the input-row contract and leakage constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import numpy as np
 
+REL_EDGES = np.array([-2.0, -1.5, -1.0, -0.6, -0.3, -0.1, 0.1, 0.3, 0.6, 1.0, 1.5, 2.0], dtype=np.float64)
+
+
+def log_dur(ms):
+    return float(np.log2(max(float(ms), 0.0) + 1.0))
+
 
 def freq_bucket(count):
     if count == 0:
@@ -34,6 +40,8 @@ def freq_bucket(count):
 
 def raw(row, state):
     duration_decile = str(int(np.searchsorted(state['edges'], row[5])))
+    rel = log_dur(row[5]) - state['user_logd'].get(row[1], state['global_logd'])
+    rel_b = str(int(np.searchsorted(REL_EDGES, rel)))
     return [
         str(row[1]),
         str(row[2]),
@@ -44,19 +52,32 @@ def raw(row, state):
         'vc' + freq_bucket(state['video_counts'].get(row[2], 0)),
         'ac' + freq_bucket(state['author_counts'].get(row[3], 0)),
         'td' + str(row[4]) + '|' + duration_decile,
+        'q' + str(int(np.searchsorted(state['fine_edges'], row[5]))),
+        'r' + rel_b,
+        'rt' + str(row[4]) + '|' + rel_b,
     ]
 
 
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
+    fine_edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 41)[1:-1])
     user_counts, video_counts, author_counts = {}, {}, {}
+    user_logd_sum, user_logd_count = {}, {}
+    global_sum, global_count = 0.0, 0
     for r in rows:
         user_counts[r[1]] = user_counts.get(r[1], 0) + 1
         video_counts[r[2]] = video_counts.get(r[2], 0) + 1
         author_counts[r[3]] = author_counts.get(r[3], 0) + 1
-    state = dict(edges=edges, user_counts=user_counts, video_counts=video_counts,
-                 author_counts=author_counts)
-    vocabs = [{} for _ in range(9)]
+        ld = log_dur(r[5])
+        user_logd_sum[r[1]] = user_logd_sum.get(r[1], 0.0) + ld
+        user_logd_count[r[1]] = user_logd_count.get(r[1], 0) + 1
+        global_sum += ld
+        global_count += 1
+    user_logd = {u: user_logd_sum[u] / user_logd_count[u] for u in user_logd_sum}
+    global_logd = global_sum / global_count if global_count else 0.0
+    state = dict(edges=edges, fine_edges=fine_edges, user_counts=user_counts, video_counts=video_counts,
+                 author_counts=author_counts, user_logd=user_logd, global_logd=global_logd)
+    vocabs = [{} for _ in range(12)]
     for row in rows:
         for i, value in enumerate(raw(row, state)):
             if value not in vocabs[i]:
```

---

## Iteration 15: `node_015`

**Status** `success` · **Parent** `node_011` · **Commit** `e436bb73fded`

### Hypothesis

```text
SELECTED CHANGE
Experiment (training-procedure / prediction-aggregation subsystem — untouched in this lineage: from this same parent node_011 the supplied siblings changed batch size (node_012, 0.60319), per-user inverse-frequency sample weights (node_013, 0.60319) and user-relative duration features (node_014, 0.60327), all landing within noise below the parent's 0.60479, and earlier nodes only touched features (node_007/node_010), loss (node_001 BPR, node_009 RankNet) and the backbone (node_008 MLP tower, node_011 DCN-V2 cross); no supplied experiment has trained more than one model or changed how scores are aggregated): turn the single DeepFM+DCN-V2 candidate into a seed-diversified ensemble of 3 independently trained models whose predicted probabilities are averaged at inference, leaving the 9-field encoding, the pointwise sigmoid cross-entropy loss, the FM+MLP+cross architecture and all other hyperparameters (k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, h1=64, h2=32) exactly as supplied.

Hypothesis: the last three single-variable edits all moved Primary by less than the apparent run-to-run noise (~0.0015), which indicates the current single model's within-user ranking is variance-limited (sparse ID embeddings initialized from one seed, one shuffle order, one early-stopping epoch) rather than bias-limited. Averaging the probabilities of several independently seeded models cancels this initialization/ordering variance and should raise per-user ranking quality (GAUC and nDCG@5) without changing the model class, features, or objective.

Implementation behavior:
- config.py: add n_models=3 to DEFAULTS and include 'n_models' in the existing integer validation tuple ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2') so it must be an int >= 1. No other config values change.
- train.py: fit features once with fit(train_rows) and compute Xtr, ytr, Xva once, exactly as now. Then train config['n_models'] members sequentially. Member m (0-based) is constructed as FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + m, h1=config['h1'], h2=config['h2']) and uses its own shuffling generator np.random.default_rng(config['seed'] + 1000 * (m + 1)). Each member runs the existing epoch loop (same np.random shuffle, same model.step over config['bs'] minibatches, same evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva)) call, same 'primary' > best + 1e-5 early-stopping rule with per-member best/bad counters and config['patience']), and keeps its own best-epoch weight snapshot {key: copy.deepcopy(getattr(model, key)) for key in PARAM_KEYS}.
- Checkpoint payload: payload['model_state'] becomes a list of per-member best-weight dicts (one entry appended/updated per member, in member order), payload['best_epoch'] becomes a list of per-member best epochs, and payload['training_state'] gains a 'member' index alongside epoch/best/bad/rng and stores 'latest' as the current member's copy.deepcopy(vars(model)). Keep save_checkpoint atomic and keep saving after every epoch of every member. Keep the existing nonfinite-state check over all numeric attributes in vars(model).
- Resume path: keep validating payload['config'] == config and payload['context'] == context and calling Predictor(payload) before resuming; restore member index, epoch, best, bad, the shuffling rng state and the current member's 'latest' state (same shape/finiteness checks and the same set(state['latest']) != set(vars(model)) completeness check), then continue that member's remaining epochs and afterwards train any remaining members from scratch. Preserve the train(train_rows, valid_rows, checkpoint_path, overrides, context) signature and log one line per member/epoch.
- model.py: leave class FM, PARAM_KEYS, logits, step, predict, read_checkpoint and load_predictor(checkpoint_path) unchanged in behavior. Change Predictor.__init__ to build one FM per entry in state['model_state'] (list), each with len(self.features['vocabs']) fields and config k/lr/l2/h1/h2 and seed=config['seed'] + i, applying the existing per-key shape and np.isfinite validation over PARAM_KEYS before setattr, and raising a clear ValueError on empty or malformed model_state. Change Predictor.predict(rows) to transform rows once with the restored features state and return the elementwise mean over members of sigmoid(member.predict(X)) as a float array, preserving input order and the empty-input early return. Higher score still means stronger predicted long_view relevance.
- features.py and requirements.txt unchanged.

Cost: roughly 3x the parent's 77s wall clock (~230-260s), far inside candidate_timeout_s=1800 and affordable within the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670451 | 0.537342 | 0.603896 | -0.000896 | 198 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |   4 +--
 model.py  |  27 ++++++++++-----
 train.py  | 113 +++++++++++++++++++++++++++++++++++++-------------------------
 3 files changed, 87 insertions(+), 57 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 4be20d6..a7cc9d5 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32, n_models=3)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2', 'n_models'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 0399a21..ad69d03 100644
--- a/model.py
+++ b/model.py
@@ -175,14 +175,21 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], len(self.features['vocabs']), k=config['k'], lr=config['lr'],
-                         l2=config['l2'], seed=config['seed'], h1=config['h1'], h2=config['h2'])
-        weights = state['model_state']
-        for name in PARAM_KEYS:
-            value = weights[name]
-            if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
-                raise ValueError('incompatible or nonfinite model weights: ' + name)
-            setattr(self.model, name, value)
+        model_states = state['model_state']
+        if not isinstance(model_states, list) or not model_states:
+            raise ValueError('model_state must be a non-empty list of member weights')
+        self.models = []
+        for i, weights in enumerate(model_states):
+            model = FM(self.features['dim'], len(self.features['vocabs']), k=config['k'], lr=config['lr'],
+                       l2=config['l2'], seed=config['seed'] + i, h1=config['h1'], h2=config['h2'])
+            for name in PARAM_KEYS:
+                if name not in weights:
+                    raise ValueError('malformed model_state, missing key: ' + name)
+                value = weights[name]
+                if np.shape(value) != np.shape(getattr(model, name)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite model weights: ' + name)
+                setattr(model, name, value)
+            self.models.append(model)
 
     def predict(self, rows):
         """Return one finite real-valued score per row, preserving input order.
@@ -193,7 +200,9 @@ class Predictor:
         """
         if not len(rows):
             return np.empty(0, dtype=np.float32)
-        return self.model.predict(transform(rows, self.features))
+        X = transform(rows, self.features)
+        scores = np.mean([sigmoid(model.predict(X)) for model in self.models], axis=0)
+        return scores.astype(np.float32)
 
 
 def load_predictor(checkpoint_path):
diff --git a/train.py b/train.py
index 1ad046f..3d26853 100644
--- a/train.py
+++ b/train.py
@@ -89,7 +89,8 @@ def save_checkpoint(path, payload):
 
 def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     config = resolve(overrides)
-    rng = np.random.default_rng(config['seed'])
+    n_models = config['n_models']
+    resume_member = None
     if Path(checkpoint_path).exists():
         payload = read_checkpoint(checkpoint_path)
         if payload['config'] != config or payload['context'] != context:
@@ -97,55 +98,75 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         Predictor(payload)  # Validate inference weights before resuming.
         features = payload['features_state']
         state = payload['training_state']
-        rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'],
-                    seed=config['seed'], h1=config['h1'], h2=config['h2'])
-        if set(state['latest']) != set(vars(model)):
-            raise ValueError('incomplete optimizer/model state')
-        for key, value in state['latest'].items():
-            if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
-                raise ValueError('incompatible or nonfinite latest state: ' + key)
-            setattr(model, key, value)
-        best, bad, epoch = state['best'], state['bad'], state['epoch']
-        if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
-                or type(bad) is not int or not 0 <= bad <= config['patience']
-                or not np.isfinite(best) or not 0 <= best <= 1
-                or model.lr != config['lr'] or model.l2 != config['l2']
-                or type(model.t) is not int or model.t < 1):
-            raise ValueError('invalid checkpoint training progress/settings')
-        print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
+        resume_member = state['member']
+        resume_epoch = state['epoch']
+        resume_best = state['best']
+        resume_bad = state['bad']
+        resume_rng_state = state['rng']
+        resume_latest = state['latest']
+        print(f'resume: member={resume_member}, completed epoch={resume_epoch}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'],
-                    seed=config['seed'], h1=config['h1'], h2=config['h2'])
-        best, bad, epoch = -1.0, 0, 0
-        payload = dict(version=1, config=config, features_state=features, context=context)
+        payload = dict(version=1, config=config, features_state=features, context=context,
+                        model_state=[], best_epoch=[])
         print('fresh training', flush=True)
+
     Xtr = transform(train_rows, features)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
-    for epoch in range(epoch + 1, config['epochs'] + 1):
-        if bad >= config['patience']:
-            break
-        order = rng.permutation(len(ytr))
-        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                  for i in range(0, len(order), config['bs'])]
-        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
-        if validation['primary'] > best + 1e-5:
-            best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in PARAM_KEYS}
-            payload['best_epoch'] = epoch
+
+    start_member = resume_member if resume_member is not None else 0
+    for m in range(start_member, n_models):
+        model = FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'],
+                    seed=config['seed'] + m, h1=config['h1'], h2=config['h2'])
+        member_rng = np.random.default_rng(config['seed'] + 1000 * (m + 1))
+        if resume_member is not None and m == resume_member:
+            member_rng.bit_generator.state = resume_rng_state
+            if set(resume_latest) != set(vars(model)):
+                raise ValueError('incomplete optimizer/model state')
+            for key, value in resume_latest.items():
+                if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite latest state: ' + key)
+                setattr(model, key, value)
+            best, bad, epoch = resume_best, resume_bad, resume_epoch
+            if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
+                    or type(bad) is not int or not 0 <= bad <= config['patience']
+                    or not np.isfinite(best) or not 0 <= best <= 1
+                    or model.lr != config['lr'] or model.l2 != config['l2']
+                    or type(model.t) is not int or model.t < 1):
+                raise ValueError('invalid checkpoint training progress/settings')
+            print(f'resume: member={m} optimizer step={model.t}', flush=True)
         else:
-            bad += 1
-        for key, value in vars(model).items():
-            if isinstance(value, np.ndarray):
-                if not np.isfinite(value).all():
-                    raise ValueError('nonfinite training state; keeping last valid checkpoint')
-            elif isinstance(value, (int, float, np.floating, np.integer)):
-                if not np.isfinite(value):
-                    raise ValueError('nonfinite training state; keeping last valid checkpoint')
-        payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
-            rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
-        payload['validation'] = validation
-        save_checkpoint(checkpoint_path, payload)
-        print(f'epoch={epoch} loss={np.mean(losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
+            best, bad, epoch = -1.0, 0, 0
+
+        for epoch in range(epoch + 1, config['epochs'] + 1):
+            if bad >= config['patience']:
+                break
+            order = member_rng.permutation(len(ytr))
+            losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
+                      for i in range(0, len(order), config['bs'])]
+            validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
+            if validation['primary'] > best + 1e-5:
+                best, bad = validation['primary'], 0
+                best_state = {key: copy.deepcopy(getattr(model, key)) for key in PARAM_KEYS}
+                if len(payload['model_state']) > m:
+                    payload['model_state'][m] = best_state
+                    payload['best_epoch'][m] = epoch
+                else:
+                    payload['model_state'].append(best_state)
+                    payload['best_epoch'].append(epoch)
+            else:
+                bad += 1
+            for key, value in vars(model).items():
+                if isinstance(value, np.ndarray):
+                    if not np.isfinite(value).all():
+                        raise ValueError('nonfinite training state; keeping last valid checkpoint')
+                elif isinstance(value, (int, float, np.floating, np.integer)):
+                    if not np.isfinite(value):
+                        raise ValueError('nonfinite training state; keeping last valid checkpoint')
+            payload['training_state'] = dict(member=m, epoch=epoch, best=best, bad=bad,
+                rng=member_rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
+            payload['validation'] = validation
+            save_checkpoint(checkpoint_path, payload)
+            print(f'member={m} epoch={epoch} loss={np.mean(losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
+        resume_member = None
```

---

## Iteration 16: `node_016`

**Status** `success` · **Parent** `node_011` · **Commit** `93c84b0633dc`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-encoding regularization / cold-start handling — a new direction not attempted from this parent or anywhere in the supplied lineage): introduce a minimum-occurrence vocabulary threshold for the three ID fields in features.py so that rare training IDs share the per-field out-of-vocabulary slot, making that slot a *trained* "rare/unseen ID" representation instead of a never-updated random embedding. Keep the 9-field encoding order, the pointwise sigmoid cross-entropy loss, and the entire FM + DeepFM-MLP + DCN-V2 backbone in model.py exactly as supplied.

Hypothesis: today every distinct user_id/video_id/author_id in training gets its own embedding, even those seen once or twice, and validation rows with unseen IDs fall into the per-field index len(vocab), which receives no gradient during training and therefore keeps its random 0.01-scale initialization. Both effects hurt within-user ordering: singleton-ID embeddings are pure noise, and unseen items are scored by an untrained vector. Folding rare IDs into the shared OOV slot both denoises the embedding table and trains a meaningful "cold ID" prior that validation rows can actually use; the already-present uc/vc/ac frequency-bucket fields and the duration/tab fields still carry the item- and user-specific signal for these rows.

Implementation behavior:
- config.py: add `min_count=3` to DEFAULTS and include 'min_count' in the existing integer validation tuple ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2') so it must be an int >= 1. No other config value changes (k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32 stay).
- features.py: change the signature to `fit(rows, min_count=1)`. Keep the existing first pass unchanged (duration quantile `edges` over np.linspace(0,1,11)[1:-1], and the user_counts/video_counts/author_counts dicts). Then, when building the 9 vocabs from raw(row, state), apply the threshold to ID fields only: for field indices 0 (user_id string), 1 (video_id string) and 2 (author_id string), insert a value into vocabs[i] only if its training occurrence count is >= min_count; for field indices 3..8 (tab, duration decile, uc/vc/ac frequency buckets, tab×decile conjunction) keep every observed value as today. Occurrence counts for the ID fields may be taken directly from the already-computed user_counts/video_counts/author_counts dicts (keys are the raw row values) or from an equivalent per-field string counter; use whichever is consistent with the raw() string form. Keep dims = [len(v) + 1 for v in vocabs], offsets = np.cumsum([0] + dims[:-1]).astype(np.int32), dim = sum(dims), and keep transform(rows, state) exactly as it is, including its dynamic column count and the `vocab.get(value, len(vocab)) + offsets[i]` fallback — the point is that below-threshold IDs now hit that fallback during *training* as well, so its embedding and linear weight are learned. State must stay picklable and keep all existing keys so train.py's single checkpoint payload and model.Predictor keep working unchanged.
- train.py: only change the fresh-training call to `features = fit(train_rows, config['min_count'])`. Everything else (resume path, Xtr/ytr/Xva construction, epoch loop, model.step, evaluate() usage, early stopping on validation primary, PARAM_KEYS serialization, atomic save_checkpoint, train()/load_predictor contracts) is untouched.
- model.py and requirements.txt unchanged; no labels, no validation statistics, and no date-derived signals are used — only training-row exposure counts already fitted in features.fit.

Distinction from the closest supplied prior attempts: node_007 (ancestor) *added* log2 frequency-bucket fields alongside the raw IDs but left every ID in its own vocabulary slot; node_010 used label-based history rates; sibling node_014 added user-relative duration fields; siblings node_012 (bs=2048), node_013 (per-user sample weights) and node_015 (3-seed ensemble) did not touch the encoding. No supplied experiment has pruned rare IDs into a shared trainable OOV bucket.

Cost: strictly cheaper than the parent (smaller embedding table, same number of fields and epochs), expected around the parent's ~77 s wall clock and far inside candidate_timeout_s=1800, which fits the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671775 | 0.537556 | 0.604665 | -0.000127 | 83 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py   |  4 ++--
 features.py | 14 +++++++++++---
 train.py    |  2 +-
 3 files changed, 14 insertions(+), 6 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 4be20d6..5d9f3cd 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, h1=64, h2=32, min_count=3)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'h1', 'h2', 'min_count'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/features.py b/features.py
index 5b1da2d..ce29db5 100644
--- a/features.py
+++ b/features.py
@@ -47,7 +47,7 @@ def raw(row, state):
     ]
 
 
-def fit(rows):
+def fit(rows, min_count=1):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
     user_counts, video_counts, author_counts = {}, {}, {}
     for r in rows:
@@ -56,10 +56,18 @@ def fit(rows):
         author_counts[r[3]] = author_counts.get(r[3], 0) + 1
     state = dict(edges=edges, user_counts=user_counts, video_counts=video_counts,
                  author_counts=author_counts)
+    id_counts = [user_counts, video_counts, author_counts]
     vocabs = [{} for _ in range(9)]
     for row in rows:
-        for i, value in enumerate(raw(row, state)):
-            if value not in vocabs[i]:
+        values = raw(row, state)
+        raw_ids = (row[1], row[2], row[3])
+        for i, value in enumerate(values):
+            if value in vocabs[i]:
+                continue
+            if i < 3:
+                if id_counts[i].get(raw_ids[i], 0) >= min_count:
+                    vocabs[i][value] = len(vocabs[i])
+            else:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
     state['vocabs'] = vocabs
diff --git a/train.py b/train.py
index 1ad046f..f5d873e 100644
--- a/train.py
+++ b/train.py
@@ -115,7 +115,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             raise ValueError('invalid checkpoint training progress/settings')
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
-        features = fit(train_rows)
+        features = fit(train_rows, config['min_count'])
         model = FM(features['dim'], len(features['vocabs']), k=config['k'], lr=config['lr'], l2=config['l2'],
                     seed=config['seed'], h1=config['h1'], h2=config['h2'])
         best, bad, epoch = -1.0, 0, 0
```

