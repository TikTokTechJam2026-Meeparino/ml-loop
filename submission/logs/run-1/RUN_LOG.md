# Run log: run-1

Run id `e1d10ad213b54f9d88b0c672f47e168f` · evaluation protocol `cfe7881824a34480…` · schema 1

## Summary

| | |
|---|---|
| Candidate iterations | 22 of 50 permitted |
| Candidate outcomes | 1 failed, 21 success |
| Stop reason | `time_budget` |
| Baseline (`genesis`) | Primary 0.601469 |
| Selected (`node_021`) | Primary 0.605256 |
| Validation gain | +0.003787 |
| **Held-out test** | GAUC 0.665500 · nDCG@5 0.531409 · **Primary 0.598454** |
| Test coverage | 23,875 users · 170,588 rows |
| Model calls | 57 |
| Provider-reported tokens | 1,170,743 |
| Agent wall clock | 87.1 min |
| GPU hours | 0 (CPU only) |

## Manual interventions

**2** operator intervention(s) during this run.

| Time (UTC) | Cause | Stage | Candidate | Operator action |
|---|---|---|---|---|
| 18:33:04 | `LLMError` | propose | node_011 | resumed the run |
| 19:19:53 | `LLMError` | propose | node_021 | resumed the run |

Interventions are counted from the run's own event log: a provider or infrastructure failure pauses the run and records `run.failed`, and further orchestrator activity in the same log means an operator resumed it. Every intervention above is a resume of an unmodified run.

No manual edits were made to candidate code: every commit in the candidate workspace is authored by the agent identity (ML Loop <ml-loop@localhost>). Hypotheses, diffs, parent selection, and stopping were produced by the agent without human editing.

### Provider transport failures (6)

| Time (UTC) | Error | HTTP | Candidate | Attempt |
|---|---|---|---|---|
| 18:32:57 | `InternalServerError` | 500 | node_011 | 1 |
| 18:33:00 | `InternalServerError` | 500 | node_011 | 2 |
| 18:33:04 | `InternalServerError` | 500 | node_011 | 3 |
| 19:19:42 | `InternalServerError` | 500 | node_021 | 1 |
| 19:19:50 | `InternalServerError` | 500 | node_021 | 2 |
| 19:19:53 | `InternalServerError` | 500 | node_021 | 3 |

Transport failures are retried inside the client and do not count as experimental evidence. Only an exhausted retry budget pauses the run.

## Iteration index

| # | Candidate | GAUC | nDCG@5 | Primary | vs parent | Status | Repairs |
|---|---|---|---|---|---|---|---|
| baseline | `genesis` | 0.667133 | 0.535805 | 0.601469 | - | success | 0 |
| 1 | `node_001` | 0.661792 | 0.532990 | 0.597391 | -0.004078 | success | 0 |
| 2 | `node_002` | 0.668873 | 0.536475 | 0.602674 | +0.001205 | success | 0 |
| 3 | `node_003` | 0.668640 | 0.536115 | 0.602377 | -0.000297 | success | 0 |
| 4 | `node_004` | 0.670133 | 0.536906 | 0.603519 | +0.000845 | success | 0 |
| 5 | `node_005` | 0.670368 | 0.536819 | 0.603593 | +0.000074 | success | 0 |
| 6 | `node_006` | 0.670176 | 0.536748 | 0.603462 | -0.000058 | success | 0 |
| 7 | `node_007` | 0.668068 | 0.535744 | 0.601906 | -0.001613 | success | 0 |
| 8 | `node_008` | 0.671384 | 0.537380 | 0.604382 | +0.000863 | success | 0 |
| 9 | `node_009` | 0.670041 | 0.537083 | 0.603562 | -0.000820 | success | 0 |
| 10 | `node_010` | 0.670923 | 0.537116 | 0.604020 | -0.000362 | success | 0 |
| 11 | `node_011` | 0.666475 | 0.535652 | 0.601063 | -0.003319 | success | 0 |
| 12 | `node_012` | 0.671572 | 0.537457 | 0.604515 | +0.000133 | success | 0 |
| 13 | `node_013` | 0.671071 | 0.536974 | 0.604023 | -0.000492 | success | 0 |
| 14 | `node_014` | 0.670624 | 0.537200 | 0.603912 | -0.000602 | success | 0 |
| 15 | `node_015` | 0.671154 | 0.537311 | 0.604232 | -0.000282 | success | 0 |
| 16 | `node_016` | 0.671595 | 0.537453 | 0.604524 | +0.000010 | success | 1 |
| 17 | `node_017` | 0.669509 | 0.536716 | 0.603112 | -0.001402 | success | 0 |
| 18 | `node_018` | 0.671799 | 0.537578 | 0.604689 | +0.001095 | success | 0 |
| 19 | `node_019` | 0.671054 | 0.537565 | 0.604309 | -0.000380 | success | 0 |
| 20 | `node_020` | 0.672447 | 0.537976 | 0.605211 | +0.000523 | success | 0 |
| 21 | `node_021` | 0.672574 | 0.537937 | 0.605256 | +0.000044 | success | 0 |
| 22 | `node_022` | - | - | - | - | failed | 0 |

---

## Baseline: `genesis`

**Status** `success` · **Parent** `none` · **Commit** `9fdb9ba1a857`

### Hypothesis

Supplied reference pipeline. No agent hypothesis; this is the baseline every candidate is measured against.

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667133 | 0.535805 | 0.601469 | - | 34 s |

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

**Status** `success` · **Parent** `genesis` · **Commit** `0a66cd78972e`

### Hypothesis

```text
SELECTED CHANGE
Experiment: enrich the FM input feature set in features.py (the only module that must change substantially) to test the hypothesis that the current 5-field encoding (user_id, video_id, author_id, tab, 10-bin duration) is the main bottleneck, and that adding duration resolution, frequency/popularity buckets, and explicit categorical crosses will raise GAUC and nDCG@5. No prior feature-engineering attempt was supplied in the lineage (genesis is the only node, no siblings), so this is the first change to this subsystem.

Implementation behavior:
1. Generalize the encoder to an arbitrary number of fields F: `raw(row, state)` returns a list of F string tokens; `fit(rows)` builds one vocabulary per field; `transform` allocates `np.empty((len(rows), F), dtype=np.int32)` using `len(state['vocabs'])` instead of the hardcoded 5, and keeps returning offset-shifted global indices plus a per-field out-of-vocabulary slot (unchanged offsets/dim conventions so model.FM, Predictor, and train.py continue to work unmodified apart from any import signature adjustment).
2. Fit two duration quantile binnings on training rows only: fine edges = np.quantile(durations, np.linspace(0, 1, 33)[1:-1]) (32 bins) and coarse edges = np.quantile(durations, np.linspace(0, 1, 9)[1:-1]) (8 bins). Use np.searchsorted for both.
3. Compute training-only occurrence counts for user_id, video_id, author_id (no labels used, so no leakage) and store them in the fitted state. Derive bucket tokens as str(min(int(log2(1 + count)), 12)); unseen ids at transform time get count 0 -> bucket '0'.
4. Final field list (F = 12): user_id, video_id, author_id, tab, duration_fine_bin, user_count_bucket, video_count_bucket, author_count_bucket, user_id x tab, user_id x duration_coarse_bin, author_id x duration_coarse_bin, tab x duration_fine_bin (crosses formed by joining tokens with a separator such as '|').
5. For the four cross fields only, prune rare values during fit: any cross token whose training count is < 2 is not added to the vocabulary and therefore maps to that field's OOV index at transform time (base ID fields keep no threshold). Store the fitted edges, vocabs, count dicts, offsets, and dim in the same serializable state dict that train.py already embeds in the checkpoint, so load_predictor/Predictor restore it unchanged.
6. Preserve input row order, handle missing/unseen users, items, authors, and tabs via the OOV slot, and read only the first six row fields.

Keep config.py DEFAULTS unchanged (k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0) so the effect of the feature change is isolated; expected runtime is roughly 2-3x the 34 s baseline, far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.661792 | 0.532990 | 0.597391 | -0.004078 | 69 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 66 +++++++++++++++++++++++++++++++++++++++++++++++++++----------
 1 file changed, 56 insertions(+), 10 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..e478413 100644
--- a/features.py
+++ b/features.py
@@ -24,28 +24,74 @@ while preserving the input-row contract and leakage constraints.
 
 # Reference implementation: replaceable while preserving the contracts above.
 import numpy as np
+import math
 
+NUM_FIELDS = 12
+CROSS_FIELDS = (8, 9, 10, 11)
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+
+def _count_bucket(counts, key):
+    count = counts.get(key, 0)
+    return str(min(int(math.log2(1 + count)), 12))
+
+
+def raw(row, state):
+    user_id, video_id, author_id, tab = row[1], row[2], row[3], row[4]
+    duration = row[5]
+    fine_bin = str(int(np.searchsorted(state['fine_edges'], duration)))
+    coarse_bin = str(int(np.searchsorted(state['coarse_edges'], duration)))
+    user_bucket = _count_bucket(state['user_counts'], user_id)
+    video_bucket = _count_bucket(state['video_counts'], video_id)
+    author_bucket = _count_bucket(state['author_counts'], author_id)
+    return [
+        user_id, video_id, author_id, tab, fine_bin,
+        user_bucket, video_bucket, author_bucket,
+        user_id + '|' + tab,
+        user_id + '|' + coarse_bin,
+        author_id + '|' + coarse_bin,
+        tab + '|' + fine_bin,
+    ]
 
 
 def fit(rows):
-    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    durations = [r[5] for r in rows]
+    fine_edges = np.quantile(durations, np.linspace(0, 1, 33)[1:-1])
+    coarse_edges = np.quantile(durations, np.linspace(0, 1, 9)[1:-1])
+
+    user_counts, video_counts, author_counts = {}, {}, {}
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
-            if value not in vocabs[i]:
+        user_counts[row[1]] = user_counts.get(row[1], 0) + 1
+        video_counts[row[2]] = video_counts.get(row[2], 0) + 1
+        author_counts[row[3]] = author_counts.get(row[3], 0) + 1
+
+    state = dict(fine_edges=fine_edges, coarse_edges=coarse_edges,
+                 user_counts=user_counts, video_counts=video_counts,
+                 author_counts=author_counts)
+
+    vocabs = [{} for _ in range(NUM_FIELDS)]
+    cross_counts = [{} for _ in range(NUM_FIELDS)]
+    for row in rows:
+        values = raw(row, state)
+        for i, value in enumerate(values):
+            if i in CROSS_FIELDS:
+                cross_counts[i][value] = cross_counts[i].get(value, 0) + 1
+            elif value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
+    for i in CROSS_FIELDS:
+        for value, count in cross_counts[i].items():
+            if count >= 2 and value not in vocabs[i]:
+                vocabs[i][value] = len(vocabs[i])
+
     dims = [len(v) + 1 for v in vocabs]
-    return dict(edges=edges, vocabs=vocabs,
-                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
+    state.update(vocabs=vocabs,
+                 offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
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

## Iteration 2: `node_002`

**Status** `success` · **Parent** `genesis` · **Commit** `70f683826bac`

### Hypothesis

```text
SELECTED CHANGE
Change the training objective from pointwise binary cross-entropy to an in-group (per-user) pairwise BPR ranking loss, keeping the FM backbone, the current 5-field encoding in features.py, and config.py DEFAULTS unchanged so the loss change is isolated. Rationale: the evaluation groups by user_id (GAUC and nDCG@5 are within-user ranking metrics), so directly optimizing within-user ordering should improve Primary more than calibrated pointwise probability fitting. Distinction from prior attempts: the only supplied sibling (node_001) modified features.py (finer duration bins, popularity buckets, crosses) and lost 0.0041 Primary; no loss-formulation experiment has been supplied in this lineage, and features.py must remain exactly as in the parent here.

Implementation:
1. model.py: add a new method FM.step_pair(Xp, Xn) alongside the existing step() (leave step(), logits(), predict(), Predictor, load_predictor, and the checkpoint contract untouched). Behavior: B = len(Xp); stack X_all = np.concatenate([Xp, Xn], axis=0); compute z_all, E, S = self.logits(X_all); split z_p = z_all[:B], z_n = z_all[B:]; s = sigmoid(z_n - z_p).astype(np.float32); per-row logit gradients g_all = np.concatenate([-s, s]) / B; accumulate gW via np.add.at(gW, X_all, g_all[:, None]) and gV via np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E)); add self.l2 * self.V and self.l2 * self.W; apply the identical Adam update already used in step() (b1=0.9, b2=0.999, eps=1e-8, shared self.t/mV/vV/mW/vW so resume state stays the same shape and key set as vars(model)); leave self.b unchanged (the bias cancels in pairwise differences). Return the mean pairwise loss float(np.mean(-np.log(sigmoid(z_p - z_n) + 1e-9))).
2. train.py: after transforming Xtr and ytr, build per-user pair structures once (training rows only, no validation/test access): group training row indices by user_id (row[1]); for each user collect positive indices (ytr == 1) and negative indices (ytr == 0); keep only users having at least one of each; store a flat concatenated negative-index array with per-user start offsets and counts, an array pos_idx of all eligible positive row indices, and a parallel array mapping each positive to its user's offset/count.
3. Replace the per-epoch pointwise loop with pairwise training: each epoch, sample one negative per eligible positive using the existing rng (neg_choice = neg_start + (rng.random(len(pos_idx)) * neg_count).astype(np.int64), clipped to neg_count-1), shuffle the pair order with rng.permutation(len(pos_idx)), and iterate in mini-batches of config['bs'] pairs calling model.step_pair(Xtr[pos_batch], Xtr[neg_batch]); collect the returned losses for the existing epoch log line.
4. Keep everything else identical: same evaluate(...) call on validation with model.predict(Xva), same best-primary checkpoint selection, patience/early stopping, atomic save_checkpoint, payload fields (version, config, features_state, model_state, training_state, context, validation, best_epoch), and resume validation logic. If no eligible users produce pairs (should not happen), fall back to the existing pointwise step loop for that epoch so training never crashes.
Expected runtime is comparable to the 34 s baseline (pairs per epoch ≈ number of positives, each batch touching 2x bs rows), well inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668873 | 0.536475 | 0.602674 | +0.001205 | 23 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
model.py | 19 +++++++++++++++++++
 train.py | 43 ++++++++++++++++++++++++++++++++++++++++---
 2 files changed, 59 insertions(+), 3 deletions(-)
```

```diff
diff --git a/model.py b/model.py
index 495d48e..de9d383 100644
--- a/model.py
+++ b/model.py
@@ -65,6 +65,25 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
+    def step_pair(self, Xp, Xn):
+        B = len(Xp)
+        X_all = np.concatenate([Xp, Xn], axis=0)
+        z_all, E, S = self.logits(X_all)
+        z_p = z_all[:B]; z_n = z_all[B:]
+        s = sigmoid(z_n - z_p).astype(np.float32)
+        g_all = np.concatenate([-s, s]) / B
+        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        np.add.at(gW, X_all, g_all[:, None])
+        np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E))
+        gV += self.l2 * self.V; gW += self.l2 * self.W
+        self.t += 1
+        b1, b2, eps = 0.9, 0.999, 1e-8
+        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M *= b1; M += (1 - b1) * G
+            Vv *= b2; Vv += (1 - b2) * (G * G)
+            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        return float(np.mean(-np.log(sigmoid(z_p - z_n) + 1e-9)))
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index 0451b1a..b483c3b 100644
--- a/train.py
+++ b/train.py
@@ -122,12 +122,49 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     Xtr = transform(train_rows, features)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
+
+    user_pos = {}
+    user_neg = {}
+    for i, row in enumerate(train_rows):
+        uid = row[1]
+        if ytr[i] == 1:
+            user_pos.setdefault(uid, []).append(i)
+        else:
+            user_neg.setdefault(uid, []).append(i)
+    eligible_users = [u for u in user_pos if u in user_neg and len(user_neg[u]) > 0]
+    pos_idx_list = []
+    map_start = []
+    map_count = []
+    neg_flat_list = []
+    offset = 0
+    for u in eligible_users:
+        negs = user_neg[u]
+        neg_flat_list.extend(negs)
+        for p in user_pos[u]:
+            pos_idx_list.append(p)
+            map_start.append(offset)
+            map_count.append(len(negs))
+        offset += len(negs)
+    pos_idx = np.asarray(pos_idx_list, dtype=np.int64)
+    neg_start = np.asarray(map_start, dtype=np.int64)
+    neg_count = np.asarray(map_count, dtype=np.int64)
+    neg_flat = np.asarray(neg_flat_list, dtype=np.int64)
+
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
-        order = rng.permutation(len(ytr))
-        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                  for i in range(0, len(order), config['bs'])]
+        if len(pos_idx) > 0:
+            rel = np.minimum((rng.random(len(pos_idx)) * neg_count).astype(np.int64), neg_count - 1)
+            neg_choice = neg_flat[neg_start + rel]
+            order = rng.permutation(len(pos_idx))
+            pos_ord = pos_idx[order]
+            neg_ord = neg_choice[order]
+            losses = [model.step_pair(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
+                      for i in range(0, len(pos_ord), config['bs'])]
+        else:
+            order = rng.permutation(len(ytr))
+            losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
+                      for i in range(0, len(order), config['bs'])]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

---

## Iteration 3: `node_003`

**Status** `success` · **Parent** `node_002` · **Commit** `a32c04101f19`

### Hypothesis

```text
SELECTED CHANGE
Experiment (backbone change, keeping the parent's per-user pairwise BPR training loop, features.py, and config.py DEFAULTS exactly as they are): replace the plain FM second-order term with a Field-weighted Factorization Machine (FwFM) that learns one scalar importance weight per field pair. Hypothesis: with only 5 fields (user_id, video_id, author_id, tab, duration-bin), the uniform sum-of-all-pairs interaction in the current FM forces noisy pairs (e.g. user x tab, tab x duration-bin) to contribute as strongly as the informative user x video / user x author pairs; because GAUC and nDCG@5 rank within a user, item-independent terms cancel and the relative weighting of the user-item interaction pairs directly drives the metric, so learning 10 field-pair weights should improve within-user ordering at negligible parameter cost. Distinction from supplied prior attempts: node_001 changed features.py encodings (failed) and node_002 changed the loss to pairwise BPR (current parent); no backbone/architecture experiment has been supplied in this lineage, and this change touches only the interaction form, not the loss, features, or hyperparameters.

Implementation:
1. model.py, FM.__init__: add an optional argument fields=5 (default keeps all existing call sites working); store self.F = fields; precompute self.iu, self.ju = np.triu_indices(self.F, 1) (P = 10 pairs); initialize self.R = np.ones(P, dtype=np.float32) so the model starts numerically equivalent to the current FM; add Adam state self.mR = np.zeros_like(self.R), self.vR = np.zeros_like(self.R).
2. model.py, FM.logits(X): compute E = self.V[X] (B,F,k); D = (E[:, self.iu, :] * E[:, self.ju, :]).sum(-1) (B,P); inter = D @ self.R; build the symmetric pair-weight matrix M = np.zeros((F,F), float32) with M[self.iu, self.ju] = self.R and M[self.ju, self.iu] = self.R (zero diagonal); C = np.einsum('ij,bjk->bik', M, E) (B,F,k), the per-field partner sum used for gradients. Return (z, E, C, D) where z = self.b + self.W[X].sum(1) + inter.
3. model.py, FM.step(X, y) and FM.step_pair(Xp, Xn): update both to the new signature. Replace the old (S[:, None, :] - E) embedding gradient with the FwFM gradient np.add.at(gV, X_all, g_all[:, None, None] * C); keep np.add.at(gW, X_all, g_all[:, None]); add gR = D.T @ g_all (shape P) plus self.l2 * self.R; keep gV += self.l2*self.V and gW += self.l2*self.W; apply the identical single Adam update block (b1=0.9, b2=0.999, eps=1e-8, shared self.t incremented once per step) extended to include the triple (self.R, gR, self.mR, self.vR). Keep step()'s bias update self.b -= self.lr * g.sum() and keep step_pair() leaving self.b untouched, and keep both return values (BCE mean loss and mean pairwise -log sigmoid(z_p - z_n)) unchanged.
4. model.py, FM.predict: unchanged behavior (still uses logits(...)[0]).
5. model.py, Predictor.__init__: restore weights for ('V', 'W', 'b', 'R') instead of ('V', 'W', 'b'), keeping the existing shape/finiteness validation for each; raise the same clear error on missing or incompatible entries.
6. train.py: include 'R' in the best-checkpoint model_state dict (payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V','W','b','R')}) and add 'R', 'mR', 'vR' to the nonfinite training-state check tuple. Everything else in train.py (pair construction, per-epoch negative sampling, evaluate(...) call, best-primary selection, patience, atomic save_checkpoint, payload fields, resume validation via set(state['latest']) == set(vars(model))) stays exactly as is; the new attributes are picked up automatically by vars(model).
Expected runtime is roughly 1.5-2x the parent's 22 s (10 explicit pair dot products instead of the squared-sum trick), i.e. well inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668640 | 0.536115 | 0.602377 | -0.000297 | 30 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
model.py | 32 +++++++++++++++++++++-----------
 train.py |  4 ++--
 2 files changed, 23 insertions(+), 13 deletions(-)
```

```diff
diff --git a/model.py b/model.py
index de9d383..85e4bc1 100644
--- a/model.py
+++ b/model.py
@@ -32,7 +32,7 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, fields=5):
         rng = np.random.default_rng(seed)
         self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
@@ -41,24 +41,33 @@ class FM:
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
         self.t = 0
+        self.F = fields
+        self.iu, self.ju = np.triu_indices(self.F, 1)
+        self.R = np.ones(len(self.iu), dtype=np.float32)
+        self.mR = np.zeros_like(self.R); self.vR = np.zeros_like(self.R)
 
     def logits(self, X):
         E = self.V[X]                                   # (B,F,k)
-        S = E.sum(1)                                    # (B,k)
-        inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        D = (E[:, self.iu, :] * E[:, self.ju, :]).sum(-1)   # (B,P)
+        inter = D @ self.R
+        M = np.zeros((self.F, self.F), dtype=np.float32)
+        M[self.iu, self.ju] = self.R
+        M[self.ju, self.iu] = self.R
+        C = np.einsum('ij,bjk->bik', M, E)
+        return self.b + self.W[X].sum(1) + inter, E, C, D
 
     def step(self, X, y):
         B = len(y)
-        z, E, S = self.logits(X)
+        z, E, C, D = self.logits(X)
         g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
+        np.add.at(gV, X, g[:, None, None] * C)
         gV += self.l2 * self.V; gW += self.l2 * self.W
+        gR = D.T @ g + self.l2 * self.R
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW), (self.R, gR, self.mR, self.vR)):
             M *= b1; M += (1 - b1) * G
             Vv *= b2; Vv += (1 - b2) * (G * G)
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
@@ -68,17 +77,18 @@ class FM:
     def step_pair(self, Xp, Xn):
         B = len(Xp)
         X_all = np.concatenate([Xp, Xn], axis=0)
-        z_all, E, S = self.logits(X_all)
+        z_all, E, C, D = self.logits(X_all)
         z_p = z_all[:B]; z_n = z_all[B:]
         s = sigmoid(z_n - z_p).astype(np.float32)
         g_all = np.concatenate([-s, s]) / B
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X_all, g_all[:, None])
-        np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E))
+        np.add.at(gV, X_all, g_all[:, None, None] * C)
         gV += self.l2 * self.V; gW += self.l2 * self.W
+        gR = D.T @ g_all + self.l2 * self.R
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW), (self.R, gR, self.mR, self.vR)):
             M *= b1; M += (1 - b1) * G
             Vv *= b2; Vv += (1 - b2) * (G * G)
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
@@ -106,7 +116,7 @@ class Predictor:
         self.features = state['features_state']
         self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         weights = state['model_state']
-        for name in ('V', 'W', 'b'):
+        for name in ('V', 'W', 'b', 'R'):
             value = weights[name]
             if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
                 raise ValueError('incompatible or nonfinite model weights: ' + name)
diff --git a/train.py b/train.py
index b483c3b..d9cc51a 100644
--- a/train.py
+++ b/train.py
@@ -168,11 +168,11 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
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

**Status** `success` · **Parent** `node_002` · **Commit** `625ac89175dc`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss formulation follow-up on the parent's pairwise BPR training): replace the 1-negative pairwise BPR objective with an in-user sampled-softmax (listwise cross-entropy) objective that scores each positive against M sampled in-user negatives, keeping the plain FM backbone (model.FM.logits with the squared-sum trick), features.py, and all other train.py logic unchanged. Hypothesis: GAUC and especially nDCG@5 are top-heavy within-user ranking metrics; contrasting each positive against several same-user negatives per update (softmax over 1+M scores) gives a lower-variance, top-focused gradient than a single random pair, so it should push the correct item above more competitors than BPR. Distinction from supplied prior attempts: node_002 (the parent) introduced single-negative pairwise BPR and node_003 changed the backbone to FwFM (slightly worse); no multi-negative/listwise loss has been tried in this lineage, and this change touches only the loss and negative sampling, not the features, backbone, or optimizer.

Implementation:
1. config.py: add a new key negs=8 to DEFAULTS (keeping k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0 unchanged) and include 'negs' in the integer-validation loop in resolve() so a non-int or value < 1 raises ValueError. Keep the unknown-key check behavior as is.
2. model.py: add a new method FM.step_list(Xp, Xn) next to the existing step() and step_pair() (leave step(), step_pair(), logits(), predict(), Predictor, read_checkpoint, and load_predictor untouched). Xp has shape (B, F) int32; Xn has shape (B, M, F) int32. Behavior: build X_all = np.concatenate([Xp[:, None, :], Xn], axis=1).reshape(B * (1 + M), F); call z_all, E, S = self.logits(X_all); reshape Z = z_all.reshape(B, 1 + M); compute a numerically stable row-wise softmax P = exp(Z - Z.max(1, keepdims=True)) / sum(...); form per-row logit gradients G = P.copy(); G[:, 0] -= 1.0; G /= B; g_all = G.reshape(-1).astype(np.float32); accumulate gW via np.add.at(gW, X_all, g_all[:, None]) and gV via np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E)); add gV += self.l2 * self.V and gW += self.l2 * self.W; apply the identical Adam update block already used in step_pair (b1=0.9, b2=0.999, eps=1e-8, single self.t increment per call, shared self.mV/vV/mW/vW so vars(model) keeps the same key set and shapes for the resume contract); leave self.b unchanged (a constant per-group offset cancels in the softmax). Return the mean listwise loss float(np.mean(logsumexp(Z, axis=1) - Z[:, 0])) computed stably with the row max.
3. train.py: keep the existing per-user pair structures (pos_idx, neg_start, neg_count, neg_flat) exactly as built today, but sample M = config['negs'] negatives per positive each epoch with the existing rng: rel = np.minimum((rng.random((len(pos_idx), M)) * neg_count[:, None]).astype(np.int64), (neg_count - 1)[:, None]); neg_choice = neg_flat[neg_start[:, None] + rel] giving shape (P, M) (sampling with replacement is fine for users with fewer than M negatives). Shuffle group order with order = rng.permutation(len(pos_idx)) as now, and iterate mini-batches of config['bs'] groups calling model.step_list(Xtr[pos_ord[i:i+bs]], Xtr[neg_ord[i:i+bs]]) where neg_ord = neg_choice[order]; collect returned losses for the existing epoch log line. Keep the existing pointwise model.step fallback branch when len(pos_idx) == 0.
4. Keep everything else identical: same evaluate(...) call on validation with model.predict(Xva), same best-primary checkpoint selection and payload['model_state'] over ('V','W','b'), same nonfinite check tuple, patience/early stopping, atomic save_checkpoint, payload fields, and resume validation via set(state['latest']) == set(vars(model)).
Runtime: each step processes 9x bs rows instead of 2x bs with the same number of steps per epoch, so expect roughly 3-5x the parent's 22.7 s (about 70-120 s), well inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670133 | 0.536906 | 0.603519 | +0.000845 | 55 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 25 +++++++++++++++++++++++++
 train.py  |  8 +++++---
 3 files changed, 32 insertions(+), 5 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 147c6ac..26ccf76 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index de9d383..4e5afe6 100644
--- a/model.py
+++ b/model.py
@@ -84,6 +84,31 @@ class FM:
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         return float(np.mean(-np.log(sigmoid(z_p - z_n) + 1e-9)))
 
+    def step_list(self, Xp, Xn):
+        B, M = Xn.shape[0], Xn.shape[1]
+        X_all = np.concatenate([Xp[:, None, :], Xn], axis=1).reshape(B * (1 + M), -1)
+        z_all, E, S = self.logits(X_all)
+        Z = z_all.reshape(B, 1 + M)
+        m = Z.max(1, keepdims=True)
+        expz = np.exp(Z - m)
+        P = expz / expz.sum(1, keepdims=True)
+        G = P.copy()
+        G[:, 0] -= 1.0
+        G /= B
+        g_all = G.reshape(-1).astype(np.float32)
+        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        np.add.at(gW, X_all, g_all[:, None])
+        np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E))
+        gV += self.l2 * self.V; gW += self.l2 * self.W
+        self.t += 1
+        b1, b2, eps = 0.9, 0.999, 1e-8
+        for P_, G_, M_, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M_ *= b1; M_ += (1 - b1) * G_
+            Vv *= b2; Vv += (1 - b2) * (G_ * G_)
+            P_ -= self.lr * (M_ / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        logsumexp = m.squeeze(1) + np.log(expz.sum(1))
+        return float(np.mean(logsumexp - Z[:, 0]))
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index b483c3b..48b5404 100644
--- a/train.py
+++ b/train.py
@@ -154,12 +154,14 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         if bad >= config['patience']:
             break
         if len(pos_idx) > 0:
-            rel = np.minimum((rng.random(len(pos_idx)) * neg_count).astype(np.int64), neg_count - 1)
-            neg_choice = neg_flat[neg_start + rel]
+            M = config['negs']
+            rel = np.minimum((rng.random((len(pos_idx), M)) * neg_count[:, None]).astype(np.int64),
+                              (neg_count - 1)[:, None])
+            neg_choice = neg_flat[neg_start[:, None] + rel]
             order = rng.permutation(len(pos_idx))
             pos_ord = pos_idx[order]
             neg_ord = neg_choice[order]
-            losses = [model.step_pair(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
+            losses = [model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
                       for i in range(0, len(pos_ord), config['bs'])]
         else:
             order = rng.permutation(len(ytr))
```

---

## Iteration 5: `node_005`

**Status** `success` · **Parent** `node_004` · **Commit** `61c9be42a6c3`

### Hypothesis

```text
SELECTED CHANGE
Experiment (optimization/parameter-averaging subsystem, applied on top of the parent's in-user sampled-softmax listwise FM training, which stays unchanged): add an exponential moving average (Polyak averaging) of the FM parameters during training and let per-epoch validation choose between raw and EMA weights for checkpoint selection. Hypothesis: the listwise objective resamples config['negs'] random in-user negatives every epoch, so the Adam updates on sparse embeddings are noisy and the raw end-of-epoch iterate sits in a high-variance region; a bias-corrected EMA of the weights averages away this sampling noise and should give a better within-user ordering (GAUC and nDCG@5) than any single iterate, while validation-based selection between raw and EMA makes the change safe if averaging does not help. Distinction from supplied prior attempts: node_002 and node_004 changed only the loss formulation (BPR, then sampled softmax), node_003 changed the backbone (FwFM, slightly worse), and the one supplied feature experiment was on the pointwise genesis baseline; no parameter-averaging, checkpoint-averaging, or learning-rate/optimizer-smoothing experiment has been supplied anywhere in this lineage.

Implementation:
1. config.py: add a new key ema=0.99 to DEFAULTS (keep k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8 unchanged). Validate it in resolve() alongside the existing float checks: raise ValueError('invalid ema') if it is not finite or not 0 < ema < 1. Keep the unknown-key check as is.
2. model.py (FM only; do not touch logits(), step(), step_pair(), step_list() gradient math, Predictor, read_checkpoint, or load_predictor): in __init__ add zero-initialized averaging buffers self.eV = np.zeros_like(self.V), self.eW = np.zeros_like(self.W), self.eb = np.float32(0.0) and a counter self.et = 0. Add method update_ema(self, decay): self.et += 1; self.eV *= decay; self.eV += (1 - decay) * self.V; self.eW *= decay; self.eW += (1 - decay) * self.W; self.eb = np.float32(decay * self.eb + (1 - decay) * self.b). Add method ema_weights(self, decay) returning a dict with keys 'V','W','b' holding bias-corrected float32 copies (c = 1 - decay ** self.et; V=(self.eV / c).astype(np.float32), W=(self.eW / c).astype(np.float32), b=np.float32(self.eb / c)), falling back to plain copies of V, W, b when self.et == 0. Add method predict_ema(self, X, decay, bs=200_000) that temporarily swaps self.V/self.W/self.b with the bias-corrected arrays from ema_weights(decay) inside a try/finally, calls self.predict(X, bs), and always restores the originals so training state is unaffected.
3. train.py: replace the list comprehension over mini-batches with an explicit loop that appends the returned loss and then calls model.update_ema(config['ema']) after every model.step_list(...) call (do the same in the pointwise model.step fallback branch), so averaging runs at optimizer-step granularity. At the end of each epoch compute two validations on the same frozen validation rows and grouping: validation_raw = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva)) and validation_ema = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict_ema(Xva, config['ema'])). Select validation = whichever has the higher 'primary' (prefer raw on ties) and remember the matching weight source. Keep the existing best/patience logic exactly as is (best + 1e-5 threshold, bad counter, patience/early stopping), but when a new best is recorded set payload['model_state'] to a deepcopy of the selected variant's weights: {'V','W','b'} taken from the model attributes for the raw variant or from model.ema_weights(config['ema']) for the EMA variant, and keep payload['best_epoch'] = epoch. Extend the nonfinite guard tuple to ('V','W','b','mV','vV','mW','vW','eV','eW','eb'). Keep payload['training_state'] = dict(epoch, best, bad, rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model))) unchanged in form (it will now also carry eV/eW/eb/et, which keeps set(state['latest']) == set(vars(model)) valid on resume), keep payload['validation'] = the selected validation dict, keep the same payload key set (do not add new payload fields), keep atomic save_checkpoint and the resume path unchanged, and extend the existing epoch log line to print both primaries and which variant was selected.
Runtime: one extra validation forward pass per epoch plus O(dim*k) EMA arithmetic per optimizer step; expect roughly 1.5-2x the parent's 55 s (about 80-110 s), far inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670368 | 0.536819 | 0.603593 | +0.000074 | 69 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 model.py  | 29 +++++++++++++++++++++++++++++
 train.py  | 33 +++++++++++++++++++++++++--------
 3 files changed, 57 insertions(+), 9 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 26ccf76..9b674c5 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99)
 
 
 def resolve(overrides):
@@ -36,4 +36,6 @@ def resolve(overrides):
     for key in ('lr', 'l2'):
         if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
             raise ValueError(f'invalid {key}')
+    if not math.isfinite(config['ema']) or not 0 < config['ema'] < 1:
+        raise ValueError('invalid ema')
     return config
diff --git a/model.py b/model.py
index 4e5afe6..773ef8c 100644
--- a/model.py
+++ b/model.py
@@ -41,6 +41,35 @@ class FM:
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
         self.t = 0
+        self.eV = np.zeros_like(self.V)
+        self.eW = np.zeros_like(self.W)
+        self.eb = np.float32(0.0)
+        self.et = 0
+
+    def update_ema(self, decay):
+        self.et += 1
+        self.eV *= decay
+        self.eV += (1 - decay) * self.V
+        self.eW *= decay
+        self.eW += (1 - decay) * self.W
+        self.eb = np.float32(decay * self.eb + (1 - decay) * self.b)
+
+    def ema_weights(self, decay):
+        if self.et == 0:
+            return dict(V=self.V.copy(), W=self.W.copy(), b=np.float32(self.b))
+        c = 1 - decay ** self.et
+        return dict(V=(self.eV / c).astype(np.float32),
+                    W=(self.eW / c).astype(np.float32),
+                    b=np.float32(self.eb / c))
+
+    def predict_ema(self, X, decay, bs=200_000):
+        weights = self.ema_weights(decay)
+        V0, W0, b0 = self.V, self.W, self.b
+        try:
+            self.V, self.W, self.b = weights['V'], weights['W'], weights['b']
+            return self.predict(X, bs)
+        finally:
+            self.V, self.W, self.b = V0, W0, b0
 
     def logits(self, X):
         E = self.V[X]                                   # (B,F,k)
diff --git a/train.py b/train.py
index 48b5404..0a6dfa1 100644
--- a/train.py
+++ b/train.py
@@ -161,23 +161,40 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             order = rng.permutation(len(pos_idx))
             pos_ord = pos_idx[order]
             neg_ord = neg_choice[order]
-            losses = [model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
-                      for i in range(0, len(pos_ord), config['bs'])]
+            losses = []
+            for i in range(0, len(pos_ord), config['bs']):
+                loss = model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
+                losses.append(loss)
+                model.update_ema(config['ema'])
         else:
             order = rng.permutation(len(ytr))
-            losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                      for i in range(0, len(order), config['bs'])]
-        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
+            losses = []
+            for i in range(0, len(order), config['bs']):
+                loss = model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
+                losses.append(loss)
+                model.update_ema(config['ema'])
+        validation_raw = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
+        validation_ema = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows],
+                                   model.predict_ema(Xva, config['ema']))
+        if validation_ema['primary'] > validation_raw['primary']:
+            validation, variant = validation_ema, 'ema'
+        else:
+            validation, variant = validation_raw, 'raw'
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            if variant == 'ema':
+                payload['model_state'] = copy.deepcopy(model.ema_weights(config['ema']))
+            else:
+                payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+        if not all(np.isfinite(getattr(model, key)).all()
+                   for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'eV', 'eW', 'eb')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
             rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
         payload['validation'] = validation
         save_checkpoint(checkpoint_path, payload)
-        print(f'epoch={epoch} loss={np.mean(losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
+        print(f'epoch={epoch} loss={np.mean(losses):.6f} primary_raw={validation_raw["primary"]:.6f} '
+              f'primary_ema={validation_ema["primary"]:.6f} selected={variant} checkpoint saved', flush=True)
```

---

## Iteration 6: `node_006`

**Status** `success` · **Parent** `node_004` · **Commit** `ccf32be2b69b`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem, applied on top of the parent's in-user sampled-softmax listwise FM training, which stays exactly as is): add two leakage-safe, out-of-fold target-encoded categorical fields to features.py — a bucketized smoothed long_view rate for video_id and one for author_id — raising the FM input from 5 to 7 fields. Hypothesis: GAUC and nDCG@5 are within-user ranking metrics, so only item-side signal separates candidates inside a user's group; the video/author ID embeddings are undertrained for rare items, and an explicit historical long_view propensity bucket gives the FM a strong, immediately usable item-quality signal for exactly those rows. Distinction from prior supplied attempts: the only supplied feature experiment (node_001, on the pointwise genesis baseline) used finer duration bins, count-based popularity buckets, and ID crosses — no label statistics; this uses out-of-fold label-derived encodings on the current listwise-loss model, and no feature change has been tried anywhere on this parent (siblings covered loss formulation, FwFM backbone, and EMA weight averaging only).

Implementation:
1. features.py — fit(rows): keep the existing duration quantile edges and the 5 existing vocabs unchanged. Additionally, read the label at index 6 when present (rows shorter than 7 contribute no statistics) and compute, with a deterministic fold assignment fold = row_index % 5 (5 folds): per video_id and per author_id, the total row count, total positive count, and per-fold count/positive count (store as small numpy int64 arrays of length 5 inside dicts keyed by id, e.g. state['video_stats'] and state['author_stats'], plus scalar totals). Store the global training long_view mean as state['prior']. Define constants ALPHA = 20.0 (smoothing) and NBINS = 16 in features.py. Compute the full-data smoothed rate r = (pos + ALPHA * prior) / (count + ALPHA) for every training row's video and author, and store two arrays of bin edges state['video_edges'] and state['author_edges'] = np.quantile(rates, np.linspace(0, 1, NBINS + 1)[1:-1]). Extend dims to [len(v) + 1 for v in vocabs] + [NBINS + 1, NBINS + 1], recompute state['offsets'] = np.cumsum([0] + dims[:-1]).astype(np.int32) over all 7 fields and state['dim'] = sum(dims).
2. features.py — transform(rows, state, oof=False): return an (len(rows), 7) int32 array. Columns 0-4 stay exactly as today. For columns 5 and 6, look up the row's video_id / author_id stats; when oof=True use leave-one-fold-out counts for that row's fold (count = total_count - fold_count[n % 5], pos = total_pos - fold_pos[n % 5], using the row's position n in the supplied list), otherwise use the full totals; if the id is unseen or the resulting count is 0, emit the dedicated last bucket index NBINS, else bucket = int(np.searchsorted(edges, (pos + ALPHA * prior) / (count + ALPHA))). Add the corresponding state['offsets'][5] / [6]. The default oof=False must keep model.Predictor.predict(rows) working unchanged on label-free rows.
3. train.py: build Xtr with transform(train_rows, features, oof=True) and keep Xva = transform(valid_rows, features) (non-OOF). Everything else in train.py is unchanged: same per-user positive/negative structures, same config['negs']=8 sampled-softmax step_list loop, same evaluate(...) call, best-primary checkpoint selection, patience/early stopping, nonfinite guard, payload fields, atomic save, and resume logic.
4. model.py and config.py stay unchanged (FM.logits already handles any number of fields F; step_list already reshapes with -1). Do not add config keys.
Runtime: ~40% more per-step work from 7 instead of 5 fields plus slightly heavier transform; expect roughly 70-100 s versus the parent's 55 s, far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670176 | 0.536748 | 0.603462 | -0.000058 | 67 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 84 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 train.py    |  2 +-
 2 files changed, 82 insertions(+), 4 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..ec26867 100644
--- a/features.py
+++ b/features.py
@@ -25,11 +25,50 @@ while preserving the input-row contract and leakage constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import numpy as np
 
+ALPHA = 20.0
+NBINS = 16
+NFOLDS = 5
+
 
 def raw(row, edges):
     return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
 
 
+def _accumulate(rows):
+    video_stats = {}
+    author_stats = {}
+    total_count = 0
+    total_pos = 0
+    for n, row in enumerate(rows):
+        if len(row) < 7:
+            continue
+        y = int(row[6])
+        fold = n % NFOLDS
+        vid = row[2]
+        aid = row[3]
+        vs = video_stats.get(vid)
+        if vs is None:
+            vs = dict(count=0, pos=0, fold_count=np.zeros(NFOLDS, dtype=np.int64),
+                      fold_pos=np.zeros(NFOLDS, dtype=np.int64))
+            video_stats[vid] = vs
+        vs['count'] += 1
+        vs['pos'] += y
+        vs['fold_count'][fold] += 1
+        vs['fold_pos'][fold] += y
+        as_ = author_stats.get(aid)
+        if as_ is None:
+            as_ = dict(count=0, pos=0, fold_count=np.zeros(NFOLDS, dtype=np.int64),
+                       fold_pos=np.zeros(NFOLDS, dtype=np.int64))
+            author_stats[aid] = as_
+        as_['count'] += 1
+        as_['pos'] += y
+        as_['fold_count'][fold] += 1
+        as_['fold_pos'][fold] += y
+        total_count += 1
+        total_pos += y
+    return video_stats, author_stats, total_count, total_pos
+
+
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
     vocabs = [{} for _ in range(5)]
@@ -37,15 +76,54 @@ def fit(rows):
         for i, value in enumerate(raw(row, edges)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
-    dims = [len(v) + 1 for v in vocabs]
+
+    video_stats, author_stats, total_count, total_pos = _accumulate(rows)
+    prior = (total_pos / total_count) if total_count > 0 else 0.0
+
+    video_rates = []
+    for vs in video_stats.values():
+        video_rates.append((vs['pos'] + ALPHA * prior) / (vs['count'] + ALPHA))
+    author_rates = []
+    for as_ in author_stats.values():
+        author_rates.append((as_['pos'] + ALPHA * prior) / (as_['count'] + ALPHA))
+
+    qs = np.linspace(0, 1, NBINS + 1)[1:-1]
+    video_edges = np.quantile(video_rates, qs) if video_rates else np.zeros(NBINS - 1)
+    author_edges = np.quantile(author_rates, qs) if author_rates else np.zeros(NBINS - 1)
+
+    dims = [len(v) + 1 for v in vocabs] + [NBINS + 1, NBINS + 1]
     return dict(edges=edges, vocabs=vocabs,
+                video_stats=video_stats, author_stats=author_stats, prior=prior,
+                video_edges=video_edges, author_edges=author_edges,
                 offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
 
 
-def transform(rows, state):
-    result = np.empty((len(rows), 5), dtype=np.int32)
+def _bucket(stats, key, n, edges, prior, oof):
+    st = stats.get(key)
+    if st is None:
+        return NBINS
+    if oof:
+        fold = n % NFOLDS
+        count = st['count'] - st['fold_count'][fold]
+        pos = st['pos'] - st['fold_pos'][fold]
+    else:
+        count = st['count']
+        pos = st['pos']
+    if count <= 0:
+        return NBINS
+    r = (pos + ALPHA * prior) / (count + ALPHA)
+    return int(np.searchsorted(edges, r))
+
+
+def transform(rows, state, oof=False):
+    result = np.empty((len(rows), 7), dtype=np.int32)
+    prior = state['prior']
     for n, row in enumerate(rows):
         for i, value in enumerate(raw(row, state['edges'])):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
+        vbucket = _bucket(state['video_stats'], row[2], n, state['video_edges'], prior, oof)
+        abucket = _bucket(state['author_stats'], row[3], n, state['author_edges'], prior, oof)
+        result[n, 5] = vbucket + state['offsets'][5]
+        result[n, 6] = abucket + state['offsets'][6]
     return result
diff --git a/train.py b/train.py
index 48b5404..b79805d 100644
--- a/train.py
+++ b/train.py
@@ -119,7 +119,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
-    Xtr = transform(train_rows, features)
+    Xtr = transform(train_rows, features, oof=True)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
```

---

## Iteration 7: `node_007`

**Status** `success` · **Parent** `node_004` · **Commit** `c68a41c2a402`

### Hypothesis

```text
SELECTED CHANGE
Experiment (backbone/optimization hyperparameter subsystem, first hyperparameter experiment in this lineage): keep the parent's in-user sampled-softmax listwise FM training, features.py, and model.py exactly as they are, and instead give the model a substantially larger effective optimization budget by editing only config.py DEFAULTS: change lr from 0.001 to 0.003, epochs from 40 to 120, and patience from 4 to 8; leave k=16, l2=1e-6, bs=8192, seed=0, and negs=8 unchanged, and leave resolve()'s validation logic unchanged (the existing int/float checks already cover these keys).

Hypothesis: with bs=8192 groups and at most 40 epochs, the FM performs only on the order of a thousand Adam updates, so sparse embeddings for infrequent video_id/author_id values receive very few updates and the model is under-trained rather than over-fit. Raising the learning rate and allowing many more epochs (with a longer patience so the existing best-primary early stopping still governs when to stop) should let within-user score separation converge further and improve GAUC and nDCG@5. Increasing epochs rather than shrinking the batch is deliberate: each optimizer step already pays a dense O(dim*k) cost for the l2 term and the Adam update, so more epochs at the same batch size buys more progress per second than more, smaller steps.

Implementation details: only config.py is modified; train.py's loop, checkpoint payload, resume validation (which compares model.lr to config['lr'] and epoch/bad against config['epochs']/config['patience']), evaluate(...) call on the frozen validation rows, best-primary selection, and atomic save must remain byte-for-byte compatible in behavior. No new config keys, no schedule or per-epoch mutation of model.lr (that would break the resume check), and no changes to features, loss, or architecture.

Distinction from supplied prior attempts: node_002 and node_004 changed only the loss formulation (pairwise BPR, then sampled softmax with negs=8), node_003 changed the backbone to FwFM, sibling node_005 added EMA weight averaging (+0.0001), and sibling node_006 added out-of-fold target-encoded features (-0.0001); no experiment anywhere in the supplied lineage or siblings has altered lr, epochs, patience, bs, or k. Runtime: the parent ran 55 s; a full 120-epoch run should land around 120-200 s, far inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668068 | 0.535744 | 0.601906 | -0.001613 | 60 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

```diff
diff --git a/config.py b/config.py
index 26ccf76..c8f7748 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8)
+DEFAULTS = dict(k=16, lr=0.003, l2=1e-6, epochs=120, bs=8192, patience=8, seed=0, negs=8)
 
 
 def resolve(overrides):
```

---

## Iteration 8: `node_008`

**Status** `success` · **Parent** `node_004` · **Commit** `bbec42dcf3d9`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem, applied on top of the parent's in-user sampled-softmax listwise FM training, which stays unchanged): add two label-free, strictly-prior-history personalization fields to features.py that capture how much the user has previously been exposed to this video's author, raising the FM input from 5 to 7 fields. Hypothesis: GAUC/nDCG@5 are within-user ranking metrics, so only signals that vary across a user's own candidates can help; the current 5 fields carry no user-item behavioral affinity, and a user's past exposure to an author is a strong personalized preference proxy that also generalizes to cold videos (whose video_id embedding falls in the unknown bucket). Distinction from supplied prior attempts: sibling node_006 added out-of-fold label-derived target encodings for video/author (item-quality statistics, neutral) and node_001 (on the pointwise genesis baseline) added finer duration bins, count-based popularity buckets and ID crosses; this experiment adds no label statistics and no global popularity, only user-x-author co-occurrence counts computed from strictly earlier dates. No other sibling touched features on this parent (they covered EMA averaging and lr/epochs).

Implementation (edit features.py only; config.py, model.py, train.py and requirements.txt stay unchanged - FM.logits/step_list/predict already handle any number of fields F, and transform's (rows, state) signature is preserved so model.Predictor.predict keeps working on label-free rows):
1. features.py module constants: COUNT_EDGES = np.array([1, 2, 3, 5, 9, 17], dtype=np.int64) (7 buckets via np.searchsorted(COUNT_EDGES, count, side='right')) and SHARE_EDGES = np.array([0.001, 0.01, 0.03, 0.08, 0.2, 0.5], dtype=np.float64) (7 buckets, plus a dedicated bucket index 7 when the user has zero prior-history rows), i.e. field 5 has cardinality 7 and field 6 has cardinality 8.
2. features.py fit(rows): keep the existing duration quantile edges, the 5 string vocabs, and their behavior exactly as today. Additionally build a compact, vectorizable prior-history index using only training rows and only indices 0 (date), 1 (user_id) and 3 (author_id) - never the label: dates = sorted(set(r[0] for r in rows)) stored as state['dates'] (a plain list); date rank of a row = bisect.bisect_left(dates, row[0]) so ranks lie in [0, len(dates)] and any later (validation/inference) date maps to len(dates); D = len(dates) + 1; A = len(vocabs[2]) + 1 (author vocab size including the unknown slot); for every training row compute u = vocabs[0].get(user, len(vocabs[0])) and a = vocabs[2].get(author, len(vocabs[2])), then key_ua = (u * A + a) * D + rank and key_u = u * D + rank as int64. Store state['ua_keys'] = np.sort(array of key_ua) and state['u_keys'] = np.sort(array of key_u) (two int64 arrays of length len(rows)), plus state['ndates'] = len(dates), state['nauthors'] = A. Extend dims to [len(v) + 1 for v in vocabs] + [7, 8], recompute state['offsets'] = np.cumsum([0] + dims[:-1]).astype(np.int32) over all 7 fields, and state['dim'] = sum(dims).
3. features.py transform(rows, state): return an (len(rows), 7) int32 array; columns 0-4 are produced exactly as today. For columns 5-6, first build per-row int64 arrays u, a and rank (rank = bisect.bisect_left(state['dates'], row[0]); unseen ids map to the vocab's unknown index as in the existing lookup), then compute counts fully vectorized with two np.searchsorted calls each: base_ua = (u * state['nauthors'] + a) * D and c_ua = np.searchsorted(state['ua_keys'], base_ua + rank, 'left') - np.searchsorted(state['ua_keys'], base_ua, 'left'); base_u = u * D and c_u = np.searchsorted(state['u_keys'], base_u + rank, 'left') - np.searchsorted(state['u_keys'], base_u, 'left'), where D = state['ndates'] + 1. Because the count uses rank strictly below the row's own date rank, only impressions from strictly earlier dates are counted (same-day rows, including the row itself, are excluded), so no leakage or self-inclusion is possible. Column 5 = np.searchsorted(COUNT_EDGES, c_ua, 'right') + state['offsets'][5]; column 6 = 7 where c_u == 0, else np.searchsorted(SHARE_EDGES, c_ua / np.maximum(c_u, 1), 'right'), plus state['offsets'][6]. Cast to int32.
4. Preserve everything else: train.py keeps Xtr = transform(train_rows, features), Xva = transform(valid_rows, features), the per-user positive/negative structures, config['negs']=8 sampled-softmax step_list loop, evaluate(...) on the frozen validation rows/groups, best-primary checkpoint selection, patience/early stopping, nonfinite guard, payload key set, atomic save, and resume logic unchanged. The new state entries are plain numpy arrays/lists so the pickled checkpoint stays serializable and small (two int64 arrays of length n_train).
Runtime: ~40% more per-step work from 7 instead of 5 fields plus a vectorized history lookup during transform; expect roughly 75-95 s versus the parent's 55 s, far inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671384 | 0.537380 | 0.604382 | +0.000863 | 79 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 50 ++++++++++++++++++++++++++++++++++++++++++++++++--
 1 file changed, 48 insertions(+), 2 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..8dedf0a 100644
--- a/features.py
+++ b/features.py
@@ -23,8 +23,12 @@ while preserving the input-row contract and leakage constraints.
 """
 
 # Reference implementation: replaceable while preserving the contracts above.
+import bisect
 import numpy as np
 
+COUNT_EDGES = np.array([1, 2, 3, 5, 9, 17], dtype=np.int64)
+SHARE_EDGES = np.array([0.001, 0.01, 0.03, 0.08, 0.2, 0.5], dtype=np.float64)
+
 
 def raw(row, edges):
     return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
@@ -37,15 +41,57 @@ def fit(rows):
         for i, value in enumerate(raw(row, edges)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
-    dims = [len(v) + 1 for v in vocabs]
+
+    dates = sorted(set(r[0] for r in rows))
+    D = len(dates) + 1
+    A = len(vocabs[2]) + 1
+
+    ua_keys = np.empty(len(rows), dtype=np.int64)
+    u_keys = np.empty(len(rows), dtype=np.int64)
+    for n, row in enumerate(rows):
+        rank = bisect.bisect_left(dates, row[0])
+        u = vocabs[0].get(row[1], len(vocabs[0]))
+        a = vocabs[2].get(row[3], len(vocabs[2]))
+        ua_keys[n] = (u * A + a) * D + rank
+        u_keys[n] = u * D + rank
+
+    dims = [len(v) + 1 for v in vocabs] + [7, 8]
     return dict(edges=edges, vocabs=vocabs,
+                dates=dates, ndates=len(dates), nauthors=A,
+                ua_keys=np.sort(ua_keys), u_keys=np.sort(u_keys),
                 offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 5), dtype=np.int32)
+    result = np.empty((len(rows), 7), dtype=np.int32)
     for n, row in enumerate(rows):
         for i, value in enumerate(raw(row, state['edges'])):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
+
+    dates = state['dates']
+    A = state['nauthors']
+    D = state['ndates'] + 1
+    n = len(rows)
+    u = np.empty(n, dtype=np.int64)
+    a = np.empty(n, dtype=np.int64)
+    rank = np.empty(n, dtype=np.int64)
+    for i, row in enumerate(rows):
+        u[i] = state['vocabs'][0].get(row[1], len(state['vocabs'][0]))
+        a[i] = state['vocabs'][2].get(row[3], len(state['vocabs'][2]))
+        rank[i] = bisect.bisect_left(dates, row[0])
+
+    base_ua = (u * A + a) * D
+    c_ua = (np.searchsorted(state['ua_keys'], base_ua + rank, 'left') -
+            np.searchsorted(state['ua_keys'], base_ua, 'left'))
+    base_u = u * D
+    c_u = (np.searchsorted(state['u_keys'], base_u + rank, 'left') -
+           np.searchsorted(state['u_keys'], base_u, 'left'))
+
+    col5 = np.searchsorted(COUNT_EDGES, c_ua, 'right') + state['offsets'][5]
+    share = c_ua / np.maximum(c_u, 1)
+    col6 = np.where(c_u == 0, 7, np.searchsorted(SHARE_EDGES, share, 'right')) + state['offsets'][6]
+
+    result[:, 5] = col5.astype(np.int32)
+    result[:, 6] = col6.astype(np.int32)
     return result
```

---

## Iteration 9: `node_009`

**Status** `success` · **Parent** `node_008` · **Commit** `5b49f76538ad`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering follow-up on node_008, which added label-free user×author exposure-count features): add two PERSONALIZED, label-based prior-history propensity fields computed strictly from earlier dates, raising the FM input from 7 to 9 fields. Hypothesis: GAUC/nDCG@5 only reward signals that vary across a user's own candidate items; the parent added how OFTEN a user saw an author but nothing about how the user actually RESPONDED. Per-user long_view rates on the candidate's author and on the candidate's duration bucket are directly aligned with the target, vary within a user's candidate list, and complement (rather than duplicate) FM's latent user×author / user×duration interactions. Distinction from supplied prior attempts: node_006 added out-of-fold ITEM-level label target encodings (video/author quality, constant across users, neutral) and node_008 added label-free exposure counts/shares; no per-user label-conditioned prior-history feature has been tried in this lineage. No other change to loss, backbone, or hyperparameters.

Edit features.py only (config.py, model.py, train.py, requirements.txt unchanged: FM.logits/step_list/predict and Predictor already handle any field count F, and transform(rows, state) keeps its signature and must never read row[6]).

1. Module constants: SMOOTH_M = 5.0 and RATE_MULTIPLIERS = np.array([0.4, 0.7, 0.9, 1.1, 1.4, 2.0]); keep COUNT_EDGES and SHARE_EDGES as they are. Add two small module helpers: _pack(keys) -> (uniq, cum) where uniq, counts = np.unique(np.asarray(keys, dtype=np.int64), return_counts=True) and cum = np.concatenate([[0], np.cumsum(counts)]).astype(np.int64); and _range_count(uniq, cum, lo, hi) -> cum[np.searchsorted(uniq, hi, 'left')] - cum[np.searchsorted(uniq, lo, 'left')] (vectorized over arrays lo/hi).

2. fit(rows): keep the existing quantile edges, 5 string vocabs, dates/ndates/nauthors, ua_keys, u_keys and their behavior exactly as today. Additionally, in the same row loop compute the duration bucket db = int(np.searchsorted(edges, row[5])) with NB = len(edges) + 1 (= 11), the label y = int(row[6]) if len(row) > 6 else 0, and the same rank = bisect.bisect_left(dates, row[0]), u, a already used. Build three key lists: ua_pos_key = (u * A + a) * D + rank for rows with y == 1; ud_key = (u * NB + db) * D + rank for all rows; ud_pos_key = same as ud_key for rows with y == 1. Store them compressed via _pack as state['ua_pos'] = _pack(...), state['ud'] = _pack(...), state['ud_pos'] = _pack(...) (unique keys + cumulative counts, so the pickled checkpoint stays small). Store state['nbuckets'] = NB, state['prior'] = float(mean of y over rows) (fallback 0.5 if rows have no label column), and state['rate_edges'] = np.clip(state['prior'] * RATE_MULTIPLIERS, 1e-6, 0.999). Extend dims to [len(v) + 1 for v in vocabs] + [7, 8, 8, 8] (9 fields), recompute offsets = np.cumsum([0] + dims[:-1]).astype(np.int32) and dim = sum(dims). Because every count uses ranks strictly below the row's own date rank, same-day rows (including the row itself) are excluded, so the label statistics use strictly prior history and cannot leak.

3. transform(rows, state): return an (len(rows), 9) int32 array; columns 0-6 exactly as today (unchanged logic and offsets indices 0-6). For the new columns, additionally compute a vectorized duration bucket db = np.searchsorted(state['edges'], np.fromiter((r[5] for r in rows), dtype=np.float64, count=len(rows))) reusing the already-computed u and rank arrays, with D = state['ndates'] + 1, A = state['nauthors'], NB = state['nbuckets'].
   - base_ua = (u * A + a) * D (already available): p_ua = _range_count(*state['ua_pos'], base_ua, base_ua + rank); reuse the existing c_ua exposure count. Smoothed rate r_ua = (p_ua + SMOOTH_M * state['prior']) / (c_ua + SMOOTH_M). Column 7 = np.where(c_ua == 0, 7, np.searchsorted(state['rate_edges'], r_ua, 'right')) + state['offsets'][7].
   - base_ud = (u * NB + db) * D: c_ud = _range_count(*state['ud'], base_ud, base_ud + rank) and p_ud = _range_count(*state['ud_pos'], base_ud, base_ud + rank); r_ud = (p_ud + SMOOTH_M * state['prior']) / (c_ud + SMOOTH_M). Column 8 = np.where(c_ud == 0, 7, np.searchsorted(state['rate_edges'], r_ud, 'right')) + state['offsets'][8].
   Cast both new columns to int32.

4. Preserve everything else exactly: train.py still calls fit(train_rows), transform(train_rows/valid_rows, features), the per-user positive/negative pair structures, config['negs'] = 8 sampled-softmax step_list loop, evaluate(...) on the frozen validation rows/groups, best-primary checkpoint selection, patience/early stopping, nonfinite guard, payload key set, atomic save and resume logic. Only training rows are used for fitting; validation/test rows are never read during fit and their later dates simply map to rank = len(dates) so they see the full training history.

Runtime: ~9/7 more per-step embedding work plus three extra vectorized searchsorted lookups per transform; expect roughly 95-125 s versus the parent's 79 s, far inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670041 | 0.537083 | 0.603562 | -0.000820 | 98 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 53 ++++++++++++++++++++++++++++++++++++++++++++++++++---
 1 file changed, 50 insertions(+), 3 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 8dedf0a..c634dfa 100644
--- a/features.py
+++ b/features.py
@@ -28,6 +28,19 @@ import numpy as np
 
 COUNT_EDGES = np.array([1, 2, 3, 5, 9, 17], dtype=np.int64)
 SHARE_EDGES = np.array([0.001, 0.01, 0.03, 0.08, 0.2, 0.5], dtype=np.float64)
+SMOOTH_M = 5.0
+RATE_MULTIPLIERS = np.array([0.4, 0.7, 0.9, 1.1, 1.4, 2.0])
+
+
+def _pack(keys):
+    uniq, counts = np.unique(np.asarray(keys, dtype=np.int64), return_counts=True)
+    cum = np.concatenate([[0], np.cumsum(counts)]).astype(np.int64)
+    return uniq, cum
+
+
+def _range_count(uniq, cum, lo, hi):
+    return (cum[np.searchsorted(uniq, hi, 'left')] -
+            cum[np.searchsorted(uniq, lo, 'left')])
 
 
 def raw(row, edges):
@@ -46,24 +59,42 @@ def fit(rows):
     D = len(dates) + 1
     A = len(vocabs[2]) + 1
 
+    NB = len(edges) + 1
     ua_keys = np.empty(len(rows), dtype=np.int64)
     u_keys = np.empty(len(rows), dtype=np.int64)
+    ua_pos_keys = []
+    ud_keys = np.empty(len(rows), dtype=np.int64)
+    ud_pos_keys = []
+    ys = np.empty(len(rows), dtype=np.float64)
+    has_label = len(rows) > 0 and len(rows[0]) > 6
     for n, row in enumerate(rows):
         rank = bisect.bisect_left(dates, row[0])
         u = vocabs[0].get(row[1], len(vocabs[0]))
         a = vocabs[2].get(row[3], len(vocabs[2]))
+        db = int(np.searchsorted(edges, row[5]))
+        y = int(row[6]) if len(row) > 6 else 0
+        ys[n] = y
         ua_keys[n] = (u * A + a) * D + rank
         u_keys[n] = u * D + rank
-
-    dims = [len(v) + 1 for v in vocabs] + [7, 8]
+        ud_key = (u * NB + db) * D + rank
+        ud_keys[n] = ud_key
+        if y == 1:
+            ua_pos_keys.append((u * A + a) * D + rank)
+            ud_pos_keys.append(ud_key)
+
+    dims = [len(v) + 1 for v in vocabs] + [7, 8, 8, 8]
+    prior = float(ys.mean()) if has_label else 0.5
     return dict(edges=edges, vocabs=vocabs,
                 dates=dates, ndates=len(dates), nauthors=A,
                 ua_keys=np.sort(ua_keys), u_keys=np.sort(u_keys),
+                ua_pos=_pack(ua_pos_keys), ud=_pack(ud_keys), ud_pos=_pack(ud_pos_keys),
+                nbuckets=NB, prior=prior,
+                rate_edges=np.clip(prior * RATE_MULTIPLIERS, 1e-6, 0.999),
                 offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 7), dtype=np.int32)
+    result = np.empty((len(rows), 9), dtype=np.int32)
     for n, row in enumerate(rows):
         for i, value in enumerate(raw(row, state['edges'])):
             vocab = state['vocabs'][i]
@@ -94,4 +125,20 @@ def transform(rows, state):
 
     result[:, 5] = col5.astype(np.int32)
     result[:, 6] = col6.astype(np.int32)
+
+    NB = state['nbuckets']
+    db = np.searchsorted(state['edges'], np.fromiter((r[5] for r in rows), dtype=np.float64, count=len(rows)))
+
+    p_ua = _range_count(*state['ua_pos'], base_ua, base_ua + rank)
+    r_ua = (p_ua + SMOOTH_M * state['prior']) / (c_ua + SMOOTH_M)
+    col7 = np.where(c_ua == 0, 7, np.searchsorted(state['rate_edges'], r_ua, 'right')) + state['offsets'][7]
+
+    base_ud = (u * NB + db) * D
+    c_ud = _range_count(*state['ud'], base_ud, base_ud + rank)
+    p_ud = _range_count(*state['ud_pos'], base_ud, base_ud + rank)
+    r_ud = (p_ud + SMOOTH_M * state['prior']) / (c_ud + SMOOTH_M)
+    col8 = np.where(c_ud == 0, 7, np.searchsorted(state['rate_edges'], r_ud, 'right')) + state['offsets'][8]
+
+    result[:, 7] = col7.astype(np.int32)
+    result[:, 8] = col8.astype(np.int32)
     return result
```

---

## Iteration 10: `node_010`

**Status** `success` · **Parent** `node_008` · **Commit** `2c063a6566a9`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model-backbone subsystem, applied on top of node_008's current code: in-user sampled-softmax listwise FM training with 7 label-free feature fields, all of which stay unchanged): upgrade the plain FM into a DeepFM-style model by adding a small shared MLP tower over the concatenated field embeddings whose scalar output is added to the existing FM logit, trained jointly by the existing listwise sampled-softmax loss. Hypothesis: the current score is a strictly bilinear function of the 7 field embeddings; a nonlinear tower over the same embeddings can capture higher-order user x item x context effects (e.g. user embedding combined with duration bucket, tab, and the new prior-exposure buckets) that pairwise FM interactions cannot express, which should raise within-user ordering quality (GAUC and especially top-heavy nDCG@5). Distinction from supplied prior attempts: the only backbone experiment in this lineage was node_003 (FwFM field-pair weighting) on the older pointwise-pairwise code state, which merely reweighted existing second-order terms and added no nonlinearity; siblings of the parent explored only features (node_009, label-based propensity, failed) and earlier loss/hyperparameter changes. No deep/MLP component has ever been supplied here.

Implementation (edit config.py, model.py, train.py; features.py and requirements.txt unchanged):
1. config.py: add hidden=64 to DEFAULTS (keep k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8) and include 'hidden' in the integer-validation tuple in resolve() so non-int or <1 raises ValueError.
2. model.py FM.__init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, nfields=7, hidden=64): keep V, W, b and their Adam moments exactly as today; additionally create, from the same seeded rng, W1 = rng.normal(0, sqrt(2.0/(nfields*k)), (nfields*k, hidden)).astype(np.float32), b1 = np.zeros(hidden, np.float32), w2 = rng.normal(0, 0.01, hidden).astype(np.float32) (no output bias: a constant offset cancels in within-user ranking), plus zero-initialized Adam moments mW1/vW1, mb1/vb1, mw2/vw2, and store self.nfields = nfields, self.hidden = hidden. All new arrays are float32 so vars(model) stays picklable and shape/finiteness checkable.
3. model.py FM.logits(X): keep E = self.V[X], S = E.sum(1) and the squared-sum interaction term; additionally compute A0 = E.reshape(len(X), -1), H = np.maximum(A0 @ self.W1 + self.b1, 0.0), deep = H @ self.w2, and return z = self.b + self.W[X].sum(1) + inter + deep together with E, S, H (a 4-tuple). Update step() and step_pair() to unpack the 4-tuple (their FM-only gradient math stays as today; these are legacy/fallback paths that are not used when in-user pairs exist). predict() keeps using logits(...)[0], so inference automatically includes the deep term.
4. model.py FM.step_list(Xp, Xn): keep the current listwise construction (X_all, Z reshape, stable row softmax, G = P with G[:,0] -= 1, G /= B, g_all = G.reshape(-1).astype(np.float32)) and add MLP backprop using the returned H and A0 = E.reshape(len(X_all), -1): gw2 = H.T @ g_all; dH = (g_all[:, None] * self.w2[None, :]) * (H > 0); gb1 = dH.sum(0); gW1 = A0.T @ dH; dA0 = (dH @ self.W1.T).reshape(E.shape). Perform a single combined embedding scatter np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E) + dA0) plus the existing np.add.at(gW, X_all, g_all[:, None]). Add L2: gV += self.l2*self.V, gW += self.l2*self.W, gW1 += self.l2*self.W1, gw2 += self.l2*self.w2 (none on b1). Increment self.t once and apply the identical Adam update (b1=0.9, b2=0.999, eps=1e-8) over the five parameter/moment pairs (V,mV,vV), (W,mW,vW), (W1,mW1,vW1), (b1,mb1,vb1), (w2,mw2,vw2). Return the same mean listwise loss float(np.mean(logsumexp(Z,1) - Z[:,0])).
5. model.py Predictor.__init__: construct FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], nfields=len(self.features['offsets']), hidden=config['hidden']) and restore the weight names ('V','W','b','W1','b1','w2') with the existing shape/finiteness validation; load_predictor and read_checkpoint signatures unchanged.
6. train.py: pass nfields=len(features['offsets']) and hidden=config['hidden'] at both FM construction sites (resume branch and fresh branch); change payload['model_state'] to copy ('V','W','b','W1','b1','w2'); extend the nonfinite guard tuple to ('V','W','b','W1','b1','w2','mV','vV','mW','vW','mW1','vW1','mb1','vb1','mw2','vw2'). Everything else stays identical: fit/transform calls, per-user positive/negative structures, negs=8 sampled-softmax epoch loop, evaluate(...) on the frozen validation rows/groups, best-primary selection, patience/early stopping, atomic save_checkpoint, payload key set, and the resume check set(state['latest']) == set(vars(model)) (which now automatically covers the new attributes).
Runtime: two extra small dense matmuls (N x 112 by 112 x 64) forward and backward per step with N = 9*bs rows; expect roughly 150-220 s versus the parent's 79 s, well inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670923 | 0.537116 | 0.604020 | -0.000362 | 68 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 42 +++++++++++++++++++++++++++++++++---------
 train.py  | 11 +++++++----
 3 files changed, 42 insertions(+), 15 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 26ccf76..953efa9 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, hidden=64)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs', 'hidden'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 4e5afe6..2024b88 100644
--- a/model.py
+++ b/model.py
@@ -32,7 +32,7 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, nfields=7, hidden=64):
         rng = np.random.default_rng(seed)
         self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
@@ -40,17 +40,29 @@ class FM:
         self.lr, self.l2 = lr, l2
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
+        self.nfields = nfields
+        self.hidden = hidden
+        self.W1 = rng.normal(0, np.sqrt(2.0 / (nfields * k)), (nfields * k, hidden)).astype(np.float32)
+        self.b1 = np.zeros(hidden, dtype=np.float32)
+        self.w2 = rng.normal(0, 0.01, hidden).astype(np.float32)
+        self.mW1 = np.zeros_like(self.W1); self.vW1 = np.zeros_like(self.W1)
+        self.mb1 = np.zeros_like(self.b1); self.vb1 = np.zeros_like(self.b1)
+        self.mw2 = np.zeros_like(self.w2); self.vw2 = np.zeros_like(self.w2)
         self.t = 0
 
     def logits(self, X):
         E = self.V[X]                                   # (B,F,k)
         S = E.sum(1)                                    # (B,k)
         inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        A0 = E.reshape(len(X), -1)
+        H = np.maximum(A0 @ self.W1 + self.b1, 0.0)
+        deep = H @ self.w2
+        z = self.b + self.W[X].sum(1) + inter + deep
+        return z, E, S, H
 
     def step(self, X, y):
         B = len(y)
-        z, E, S = self.logits(X)
+        z, E, S, H = self.logits(X)
         g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
@@ -68,7 +80,7 @@ class FM:
     def step_pair(self, Xp, Xn):
         B = len(Xp)
         X_all = np.concatenate([Xp, Xn], axis=0)
-        z_all, E, S = self.logits(X_all)
+        z_all, E, S, H = self.logits(X_all)
         z_p = z_all[:B]; z_n = z_all[B:]
         s = sigmoid(z_n - z_p).astype(np.float32)
         g_all = np.concatenate([-s, s]) / B
@@ -87,7 +99,7 @@ class FM:
     def step_list(self, Xp, Xn):
         B, M = Xn.shape[0], Xn.shape[1]
         X_all = np.concatenate([Xp[:, None, :], Xn], axis=1).reshape(B * (1 + M), -1)
-        z_all, E, S = self.logits(X_all)
+        z_all, E, S, H = self.logits(X_all)
         Z = z_all.reshape(B, 1 + M)
         m = Z.max(1, keepdims=True)
         expz = np.exp(Z - m)
@@ -96,13 +108,23 @@ class FM:
         G[:, 0] -= 1.0
         G /= B
         g_all = G.reshape(-1).astype(np.float32)
+        A0 = E.reshape(len(X_all), -1)
+        gw2 = H.T @ g_all
+        dH = (g_all[:, None] * self.w2[None, :]) * (H > 0)
+        gb1 = dH.sum(0)
+        gW1 = A0.T @ dH
+        dA0 = (dH @ self.W1.T).reshape(E.shape)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X_all, g_all[:, None])
-        np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E))
+        np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E) + dA0)
         gV += self.l2 * self.V; gW += self.l2 * self.W
+        gW1 += self.l2 * self.W1; gw2 += self.l2 * self.w2
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P_, G_, M_, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+        pairs = ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW),
+                 (self.W1, gW1, self.mW1, self.vW1), (self.b1, gb1, self.mb1, self.vb1),
+                 (self.w2, gw2, self.mw2, self.vw2))
+        for P_, G_, M_, Vv in pairs:
             M_ *= b1; M_ += (1 - b1) * G_
             Vv *= b2; Vv += (1 - b2) * (G_ * G_)
             P_ -= self.lr * (M_ / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
@@ -112,6 +134,7 @@ class FM:
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
+
 def read_checkpoint(path):
     with open(path, 'rb') as stream:
         state = pickle.load(stream)
@@ -129,9 +152,10 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'],
+                         seed=config['seed'], nfields=len(self.features['offsets']), hidden=config['hidden'])
         weights = state['model_state']
-        for name in ('V', 'W', 'b'):
+        for name in ('V', 'W', 'b', 'W1', 'b1', 'w2'):
             value = weights[name]
             if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
                 raise ValueError('incompatible or nonfinite model weights: ' + name)
diff --git a/train.py b/train.py
index 48b5404..c5f9a19 100644
--- a/train.py
+++ b/train.py
@@ -98,7 +98,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'],
+                    nfields=len(features['offsets']), hidden=config['hidden'])
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +116,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'],
+                    nfields=len(features['offsets']), hidden=config['hidden'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -170,11 +172,12 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b', 'W1', 'b1', 'w2')}
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+        if not all(np.isfinite(getattr(model, key)).all() for key in
+                    ('V', 'W', 'b', 'W1', 'b1', 'w2', 'mV', 'vV', 'mW', 'vW', 'mW1', 'vW1', 'mb1', 'vb1', 'mw2', 'vw2')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
             rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
```

---

## Iteration 11: `node_011`

**Status** `success` · **Parent** `node_008` · **Commit** `13300aa82744`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss-formulation subsystem, applied on top of node_008's current code: 7 label-free feature fields + in-user sampled-softmax listwise FM with negs=8, all of which stay unchanged): make the listwise objective metric-aligned by weighting each training group (each positive row) with the inverse of its user's positive count, so every eligible user contributes equally to each epoch's gradient instead of proportionally to how many positives they have. Hypothesis: GAUC and nDCG@5 average a per-user ranking score with equal weight per user, while the current loop samples one softmax group per positive row, so heavy users (many long_views) dominate the parameter updates and light users - who are equally weighted in the metric - are under-fit; equalizing user contribution should raise the per-user-averaged Primary. Distinction from supplied prior attempts: node_002 and node_004 changed the loss FORM (pointwise BCE -> BPR -> sampled softmax) but always used uniform per-example weighting; the parent's siblings changed features (node_009, label-based propensities) and the backbone (node_010, DeepFM MLP); no per-user / per-example loss reweighting has been supplied anywhere in this lineage.

Implementation (edit model.py and train.py only; config.py, features.py and requirements.txt unchanged):
1. model.py: change the signature to FM.step_list(self, Xp, Xn, w=None) and keep every other method (step, step_pair, logits, predict, Predictor, read_checkpoint, load_predictor) exactly as today. Inside step_list keep the current construction of X_all, the 3-tuple logits call, Z = z_all.reshape(B, 1 + M), the numerically stable row-wise softmax P, and G = P.copy(); G[:, 0] -= 1.0. Then, if w is not None, multiply the per-group gradient rows by the weights: wv = np.asarray(w, dtype=np.float32); G *= wv[:, None]. Keep G /= B afterwards (weights are normalized to mean 1 in train.py, so the gradient scale and Adam behavior stay comparable to the parent). Keep g_all = G.reshape(-1).astype(np.float32), the np.add.at scatters into gW and gV, gV += self.l2 * self.V, gW += self.l2 * self.W, the single self.t increment, and the identical Adam block (b1=0.9, b2=0.999, eps=1e-8, shared self.mV/vV/mW/vW) so vars(model) keeps exactly the same key set and shapes for the resume contract; self.b stays untouched. For the return value compute per-group losses L = (m.squeeze(1) + np.log(expz.sum(1))) - Z[:, 0] and return float(np.mean(L * wv)) when w is not None, else float(np.mean(L)).
2. train.py: while building the existing per-user pair structures, also build a parallel weight array. For each eligible user u, let np_u = len(user_pos[u]) and append 1.0 / np_u once per positive of that user to a list pos_weight_list (in the same order as pos_idx_list). After the loop, pos_weight = np.asarray(pos_weight_list, dtype=np.float32); if len(pos_weight) > 0 and pos_weight.sum() > 0: pos_weight *= np.float32(len(pos_weight) / pos_weight.sum()) so the mean weight is 1.0.
3. train.py epoch loop: keep the same negative sampling (M = config['negs'], rel/neg_choice logic), the same order = rng.permutation(len(pos_idx)), pos_ord and neg_ord; additionally compute w_ord = pos_weight[order] and call model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]], w_ord[i:i + config['bs']]) in the same mini-batch comprehension, collecting the returned losses for the existing epoch log line. Keep the pointwise model.step fallback branch when len(pos_idx) == 0 unchanged.
4. Preserve everything else exactly: fit/transform calls, evaluate(...) on the frozen validation rows/groups, best-primary checkpoint selection, payload['model_state'] over ('V','W','b'), the nonfinite guard tuple, patience/early stopping, atomic save_checkpoint, payload fields, and the resume check set(state['latest']) == set(vars(model)).
Runtime: identical work per step (only an elementwise multiply added), so expect roughly the parent's 79 s, far inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.666475 | 0.535652 | 0.601063 | -0.003319 | 58 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
model.py | 11 ++++++++---
 train.py | 10 +++++++++-
 2 files changed, 17 insertions(+), 4 deletions(-)
```

```diff
diff --git a/model.py b/model.py
index 4e5afe6..d14eac0 100644
--- a/model.py
+++ b/model.py
@@ -84,7 +84,7 @@ class FM:
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         return float(np.mean(-np.log(sigmoid(z_p - z_n) + 1e-9)))
 
-    def step_list(self, Xp, Xn):
+    def step_list(self, Xp, Xn, w=None):
         B, M = Xn.shape[0], Xn.shape[1]
         X_all = np.concatenate([Xp[:, None, :], Xn], axis=1).reshape(B * (1 + M), -1)
         z_all, E, S = self.logits(X_all)
@@ -94,6 +94,9 @@ class FM:
         P = expz / expz.sum(1, keepdims=True)
         G = P.copy()
         G[:, 0] -= 1.0
+        if w is not None:
+            wv = np.asarray(w, dtype=np.float32)
+            G *= wv[:, None]
         G /= B
         g_all = G.reshape(-1).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
@@ -106,8 +109,10 @@ class FM:
             M_ *= b1; M_ += (1 - b1) * G_
             Vv *= b2; Vv += (1 - b2) * (G_ * G_)
             P_ -= self.lr * (M_ / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
-        logsumexp = m.squeeze(1) + np.log(expz.sum(1))
-        return float(np.mean(logsumexp - Z[:, 0]))
+        L = (m.squeeze(1) + np.log(expz.sum(1))) - Z[:, 0]
+        if w is not None:
+            return float(np.mean(L * wv))
+        return float(np.mean(L))
 
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
diff --git a/train.py b/train.py
index 48b5404..8e630c8 100644
--- a/train.py
+++ b/train.py
@@ -136,19 +136,25 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     map_start = []
     map_count = []
     neg_flat_list = []
+    pos_weight_list = []
     offset = 0
     for u in eligible_users:
         negs = user_neg[u]
         neg_flat_list.extend(negs)
+        np_u = len(user_pos[u])
         for p in user_pos[u]:
             pos_idx_list.append(p)
             map_start.append(offset)
             map_count.append(len(negs))
+            pos_weight_list.append(1.0 / np_u)
         offset += len(negs)
     pos_idx = np.asarray(pos_idx_list, dtype=np.int64)
     neg_start = np.asarray(map_start, dtype=np.int64)
     neg_count = np.asarray(map_count, dtype=np.int64)
     neg_flat = np.asarray(neg_flat_list, dtype=np.int64)
+    pos_weight = np.asarray(pos_weight_list, dtype=np.float32)
+    if len(pos_weight) > 0 and pos_weight.sum() > 0:
+        pos_weight *= np.float32(len(pos_weight) / pos_weight.sum())
 
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
@@ -161,7 +167,9 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             order = rng.permutation(len(pos_idx))
             pos_ord = pos_idx[order]
             neg_ord = neg_choice[order]
-            losses = [model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
+            w_ord = pos_weight[order]
+            losses = [model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]],
+                                       w_ord[i:i + config['bs']])
                       for i in range(0, len(pos_ord), config['bs'])]
         else:
             order = rng.permutation(len(ytr))
```

---

## Iteration 12: `node_012`

**Status** `success` · **Parent** `node_008` · **Commit** `9649041abe90`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (feature engineering, continuing the only direction that gained on this branch: label-free strictly-prior-history personalization). Edit features.py ONLY (config.py, model.py, train.py, requirements.txt stay exactly as supplied; FM.logits/step_list/predict and Predictor already handle any field count F, and transform(rows, state) keeps its signature and must never read row[6]). Hypothesis: node_008 showed that label-free user×author exposure counts help within-user ranking, but it captures only cumulative volume; two complementary prior-history signals are still missing and both vary across a user's own candidate list: (a) WHEN the user last saw this author (exposure recency / fatigue-vs-affinity), and (b) how much of the user's past consumption lies in the candidate's duration bucket (duration-preference profile, directly relevant to a duration-dependent long_view target). Adding these should sharpen top-of-list ordering (GAUC and nDCG@5). Distinction from supplied prior attempts: sibling node_009 added LABEL-based per-user propensity rates (failed) and node_008 added label-free author counts/shares; this change adds no label statistics, no global popularity, and no ID crosses (unlike node_001 on the old pointwise genesis baseline) - it adds only a temporal recency field and a user-duration-profile field. Fields grow from 7 to 9.

Implementation details:
1. Module constants in features.py: keep COUNT_EDGES and SHARE_EDGES unchanged; add GAP_EDGES = np.array([1, 2, 4, 8, 16, 32], dtype=np.int64) (7 gap buckets, index 7 reserved for 'no prior exposure to this author') and DSHARE_EDGES = np.array([0.02, 0.05, 0.10, 0.18, 0.30, 0.50], dtype=np.float64) (7 share buckets, index 7 reserved for 'user has no prior history').
2. fit(rows): keep the existing quantile edges, the 5 string vocabs, dates/ndates/nauthors, ua_keys, u_keys and all current behavior exactly as today. Additionally, in the same row loop, compute NB = len(edges) + 1 and the duration bucket db = int(np.searchsorted(edges, row[5])), and build ud_keys[n] = (u * NB + db) * D + rank using the same u, rank and D = len(dates) + 1 already computed. Store state['ud_keys'] = np.sort(ud_keys) (int64, length len(rows)) and state['nbuckets'] = NB. Extend dims to [len(v) + 1 for v in vocabs] + [7, 8, 8, 8] and recompute state['offsets'] = np.cumsum([0] + dims[:-1]).astype(np.int32) and state['dim'] = sum(dims). Only training rows are read in fit, and every count/lookup uses ranks strictly below the row's own date rank, so same-day rows (including the row itself) are excluded and no leakage is possible.
3. transform(rows, state): return an (len(rows), 9) int32 array. Columns 0-6 are produced by exactly the current code path (same vocab lookups, same c_ua / c_u searchsorted counts, same COUNT_EDGES/SHARE_EDGES bucketing and offsets 5 and 6). Reuse the already-computed u, a, rank, base_ua, base_u, c_u arrays and D = state['ndates'] + 1.
   - Column 7 (user×duration-bucket profile): compute durations = np.fromiter((r[5] for r in rows), dtype=np.float64, count=len(rows)) and db = np.searchsorted(state['edges'], durations).astype(np.int64); base_ud = (u * state['nbuckets'] + db) * D; c_ud = np.searchsorted(state['ud_keys'], base_ud + rank, 'left') - np.searchsorted(state['ud_keys'], base_ud, 'left'); share_ud = c_ud / np.maximum(c_u, 1); col7 = np.where(c_u == 0, 7, np.searchsorted(DSHARE_EDGES, share_ud, 'right')) + state['offsets'][7].
   - Column 8 (user×author exposure recency): start_ua = np.searchsorted(state['ua_keys'], base_ua, 'left'); pos_ua = np.searchsorted(state['ua_keys'], base_ua + rank, 'left'); has_prior = pos_ua > start_ua; last_rank = state['ua_keys'][np.maximum(pos_ua - 1, 0)] - base_ua; gap = rank - last_rank; col8 = np.where(has_prior, np.searchsorted(GAP_EDGES, np.maximum(gap, 1), 'right'), 7) + state['offsets'][8] (mask guarantees the pos_ua-1 index is only used where has_prior is true).
   - Cast both new columns to int32 and assign to result[:, 7] and result[:, 8].
4. Preserve everything else exactly: train.py still calls fit(train_rows) and transform(train_rows/valid_rows, features), the per-user positive/negative structures, the config['negs']=8 in-user sampled-softmax step_list loop, evaluate(...) on the frozen validation rows/groups, best-primary checkpoint selection, patience/early stopping, nonfinite guard, payload key set, atomic save and resume logic. New state entries are plain numpy arrays/ints so the pickled checkpoint stays serializable and small.
Runtime: ~9/7 more per-step embedding work plus two extra vectorized searchsorted lookups per transform; expect roughly 95-115 s versus the parent's 79 s, far inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671572 | 0.537457 | 0.604515 | +0.000133 | 97 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 29 +++++++++++++++++++++++++++--
 1 file changed, 27 insertions(+), 2 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 8dedf0a..6c42a97 100644
--- a/features.py
+++ b/features.py
@@ -28,6 +28,8 @@ import numpy as np
 
 COUNT_EDGES = np.array([1, 2, 3, 5, 9, 17], dtype=np.int64)
 SHARE_EDGES = np.array([0.001, 0.01, 0.03, 0.08, 0.2, 0.5], dtype=np.float64)
+GAP_EDGES = np.array([1, 2, 4, 8, 16, 32], dtype=np.int64)
+DSHARE_EDGES = np.array([0.02, 0.05, 0.10, 0.18, 0.30, 0.50], dtype=np.float64)
 
 
 def raw(row, edges):
@@ -46,24 +48,29 @@ def fit(rows):
     D = len(dates) + 1
     A = len(vocabs[2]) + 1
 
+    NB = len(edges) + 1
     ua_keys = np.empty(len(rows), dtype=np.int64)
     u_keys = np.empty(len(rows), dtype=np.int64)
+    ud_keys = np.empty(len(rows), dtype=np.int64)
     for n, row in enumerate(rows):
         rank = bisect.bisect_left(dates, row[0])
         u = vocabs[0].get(row[1], len(vocabs[0]))
         a = vocabs[2].get(row[3], len(vocabs[2]))
         ua_keys[n] = (u * A + a) * D + rank
         u_keys[n] = u * D + rank
+        db = int(np.searchsorted(edges, row[5]))
+        ud_keys[n] = (u * NB + db) * D + rank
 
-    dims = [len(v) + 1 for v in vocabs] + [7, 8]
+    dims = [len(v) + 1 for v in vocabs] + [7, 8, 8, 8]
     return dict(edges=edges, vocabs=vocabs,
                 dates=dates, ndates=len(dates), nauthors=A,
                 ua_keys=np.sort(ua_keys), u_keys=np.sort(u_keys),
+                ud_keys=np.sort(ud_keys), nbuckets=NB,
                 offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 7), dtype=np.int32)
+    result = np.empty((len(rows), 9), dtype=np.int32)
     for n, row in enumerate(rows):
         for i, value in enumerate(raw(row, state['edges'])):
             vocab = state['vocabs'][i]
@@ -94,4 +101,22 @@ def transform(rows, state):
 
     result[:, 5] = col5.astype(np.int32)
     result[:, 6] = col6.astype(np.int32)
+
+    durations = np.fromiter((r[5] for r in rows), dtype=np.float64, count=len(rows))
+    db = np.searchsorted(state['edges'], durations).astype(np.int64)
+    base_ud = (u * state['nbuckets'] + db) * D
+    c_ud = (np.searchsorted(state['ud_keys'], base_ud + rank, 'left') -
+            np.searchsorted(state['ud_keys'], base_ud, 'left'))
+    share_ud = c_ud / np.maximum(c_u, 1)
+    col7 = np.where(c_u == 0, 7, np.searchsorted(DSHARE_EDGES, share_ud, 'right')) + state['offsets'][7]
+
+    start_ua = np.searchsorted(state['ua_keys'], base_ua, 'left')
+    pos_ua = np.searchsorted(state['ua_keys'], base_ua + rank, 'left')
+    has_prior = pos_ua > start_ua
+    last_rank = state['ua_keys'][np.maximum(pos_ua - 1, 0)] - base_ua
+    gap = rank - last_rank
+    col8 = np.where(has_prior, np.searchsorted(GAP_EDGES, np.maximum(gap, 1), 'right'), 7) + state['offsets'][8]
+
+    result[:, 7] = col7.astype(np.int32)
+    result[:, 8] = col8.astype(np.int32)
     return result
```

---

## Iteration 13: `node_013`

**Status** `success` · **Parent** `node_012` · **Commit** `f945df24ef34`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (model-backbone subsystem, first deep component in this lineage): add a DeepFM-style MLP tower on top of the parent's plain FM, keeping features.py (9 label-free fields), the in-user sampled-softmax listwise objective (negs=8), the frozen splits/target/evaluator, and all train.py control flow otherwise unchanged. Hypothesis: feature engineering on this branch is saturating (node_012 gained only +0.0001) and the linear+2nd-order FM can only express additive pairwise dot products, so a small nonlinear MLP over the concatenated field embeddings should capture higher-order combinations (e.g. duration bucket x user-duration-profile x author-exposure recency) that matter for within-user long_view ordering. Distinction from prior attempts: node_003 tried FwFM (linear per-field-pair reweighting of the same bilinear form, on the old 5-field pairwise-BPR code) and node_011 tried listwise loss reweighting (failed); no deep/nonlinear component has ever been added, and sibling work on node_008 covered only EMA and lr/epochs. Implementation:
1. config.py: add hidden=64 to DEFAULTS (all other defaults unchanged: k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8) and add 'hidden' to the integer-validation tuple in resolve() so a non-int or value < 1 raises ValueError.
2. model.py FM.__init__: extend the signature to FM(dim, k=16, lr=0.001, l2=1e-6, seed=0, nfields=9, hidden=64) and, using the same rng, create float32 parameters W1 shape (nfields*k, hidden) initialized rng.normal(0, sqrt(2/(nfields*k))), b1 = zeros(hidden), w2 shape (hidden,) initialized rng.normal(0, 0.01) (so the deep head starts near zero and acts as a residual on the FM score); no output bias. Also create matching Adam moment buffers mW1/vW1, mb1/vb1, mw2/vw2 as zeros_like, so vars(model) stays a self-consistent key set for the resume contract.
3. model.py FM.logits(X, cache=False): keep E = self.V[X], S = E.sum(1) and the squared-sum interaction exactly as now, then compute h0 = E.reshape(len(X), -1), a1 = h0 @ self.W1 + self.b1, h1 = np.maximum(a1, 0), z_deep = h1 @ self.w2, and return z = self.b + self.W[X].sum(1) + inter + z_deep. Return (z, E, S) when cache is False (so predict(), step() and step_pair() keep working unchanged) and (z, E, S, (h0, a1, h1)) when cache is True.
4. model.py FM.step_list(Xp, Xn): call z_all, E, S, (h0, a1, h1) = self.logits(X_all, cache=True); compute the softmax row gradients g_all exactly as today; add deep gradients gw2 = h1.T @ g_all, da1 = (g_all[:, None] * self.w2[None, :]) * (a1 > 0), gW1 = h0.T @ da1, gb1 = da1.sum(0), dh0 = (da1 @ self.W1.T).reshape(E.shape); accumulate the embedding gradient with a single np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E) + dh0) and keep the existing np.add.at(gW, ...); add L2 as gV += l2*V, gW += l2*W, gW1 += l2*W1, gw2 += l2*w2 (no L2 on b1); increment self.t exactly once and apply the identical Adam update (b1=0.9, b2=0.999, eps=1e-8) to the extended parameter list ((V,gV,mV,vV), (W,gW,mW,vW), (W1,gW1,mW1,vW1), (b1,gb1,mb1,vb1), (w2,gw2,mw2,vw2)). Keep all arrays float32 and return the same mean listwise loss value. Leave step() and step_pair() otherwise untouched (they remain the unused fallback path).
5. model.py Predictor.__init__: construct FM with nfields=len(self.features['offsets']) and hidden=config['hidden'] alongside the existing k/lr/l2/seed, and validate/assign over the names ('V', 'W', 'b', 'W1', 'b1', 'w2') using the same shape and np.isfinite checks. load_predictor and read_checkpoint contracts stay unchanged.
6. train.py: construct FM at both the resume and fresh sites with nfields=len(features['offsets']) and hidden=config['hidden']; save payload['model_state'] as deep copies of ('V', 'W', 'b', 'W1', 'b1', 'w2'); extend the nonfinite guard tuple to ('V', 'W', 'b', 'W1', 'b1', 'w2', 'mV', 'vV', 'mW', 'vW', 'mW1', 'vW1', 'mb1', 'vb1', 'mw2', 'vw2'). Everything else (pair/negative structures, negs=8 sampled-softmax loop, evaluate(...) on validation, best-primary selection, patience, atomic save, resume validation via set(state['latest']) == set(vars(model))) stays identical.
Runtime: each step adds two small matmuls forward and backward on a (bs*(1+negs)) x (9*16) activation matrix; expect roughly 150-350 s versus the parent's 97 s, comfortably inside candidate_timeout_s and the remaining budget. requirements.txt is unchanged (numpy only).

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671071 | 0.536974 | 0.604023 | -0.000492 | 91 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 46 ++++++++++++++++++++++++++++++++++------------
 train.py  | 11 +++++++----
 3 files changed, 43 insertions(+), 18 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 26ccf76..953efa9 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, hidden=64)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs', 'hidden'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 4e5afe6..0f1dc1c 100644
--- a/model.py
+++ b/model.py
@@ -32,7 +32,7 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, nfields=9, hidden=64):
         rng = np.random.default_rng(seed)
         self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
@@ -40,13 +40,26 @@ class FM:
         self.lr, self.l2 = lr, l2
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
+        self.W1 = rng.normal(0, np.sqrt(2.0 / (nfields * k)), (nfields * k, hidden)).astype(np.float32)
+        self.b1 = np.zeros(hidden, dtype=np.float32)
+        self.w2 = rng.normal(0, 0.01, (hidden,)).astype(np.float32)
+        self.mW1 = np.zeros_like(self.W1); self.vW1 = np.zeros_like(self.W1)
+        self.mb1 = np.zeros_like(self.b1); self.vb1 = np.zeros_like(self.b1)
+        self.mw2 = np.zeros_like(self.w2); self.vw2 = np.zeros_like(self.w2)
         self.t = 0
 
-    def logits(self, X):
+    def logits(self, X, cache=False):
         E = self.V[X]                                   # (B,F,k)
         S = E.sum(1)                                    # (B,k)
         inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        h0 = E.reshape(len(X), -1)
+        a1 = h0 @ self.W1 + self.b1
+        h1 = np.maximum(a1, 0)
+        z_deep = h1 @ self.w2
+        z = self.b + self.W[X].sum(1) + inter + z_deep
+        if cache:
+            return z, E, S, (h0, a1, h1)
+        return z, E, S
 
     def step(self, X, y):
         B = len(y)
@@ -87,7 +100,7 @@ class FM:
     def step_list(self, Xp, Xn):
         B, M = Xn.shape[0], Xn.shape[1]
         X_all = np.concatenate([Xp[:, None, :], Xn], axis=1).reshape(B * (1 + M), -1)
-        z_all, E, S = self.logits(X_all)
+        z_all, E, S, (h0, a1, h1) = self.logits(X_all, cache=True)
         Z = z_all.reshape(B, 1 + M)
         m = Z.max(1, keepdims=True)
         expz = np.exp(Z - m)
@@ -96,16 +109,24 @@ class FM:
         G[:, 0] -= 1.0
         G /= B
         g_all = G.reshape(-1).astype(np.float32)
+        gw2 = h1.T @ g_all
+        da1 = (g_all[:, None] * self.w2[None, :]) * (a1 > 0)
+        gW1 = h0.T @ da1
+        gb1 = da1.sum(0)
+        dh0 = (da1 @ self.W1.T).reshape(E.shape)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X_all, g_all[:, None])
-        np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E))
+        np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E) + dh0)
         gV += self.l2 * self.V; gW += self.l2 * self.W
+        gW1 += self.l2 * self.W1; gw2 += self.l2 * self.w2
         self.t += 1
-        b1, b2, eps = 0.9, 0.999, 1e-8
-        for P_, G_, M_, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M_ *= b1; M_ += (1 - b1) * G_
-            Vv *= b2; Vv += (1 - b2) * (G_ * G_)
-            P_ -= self.lr * (M_ / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        b1c, b2c, eps = 0.9, 0.999, 1e-8
+        for P_, G_, M_, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW),
+                               (self.W1, gW1, self.mW1, self.vW1), (self.b1, gb1, self.mb1, self.vb1),
+                               (self.w2, gw2, self.mw2, self.vw2)):
+            M_ *= b1c; M_ += (1 - b1c) * G_
+            Vv *= b2c; Vv += (1 - b2c) * (G_ * G_)
+            P_ -= self.lr * (M_ / (1 - b1c ** self.t)) / (np.sqrt(Vv / (1 - b2c ** self.t)) + eps)
         logsumexp = m.squeeze(1) + np.log(expz.sum(1))
         return float(np.mean(logsumexp - Z[:, 0]))
 
@@ -129,9 +150,10 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'],
+                         nfields=len(self.features['offsets']), hidden=config['hidden'])
         weights = state['model_state']
-        for name in ('V', 'W', 'b'):
+        for name in ('V', 'W', 'b', 'W1', 'b1', 'w2'):
             value = weights[name]
             if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
                 raise ValueError('incompatible or nonfinite model weights: ' + name)
diff --git a/train.py b/train.py
index 48b5404..c5f9a19 100644
--- a/train.py
+++ b/train.py
@@ -98,7 +98,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'],
+                    nfields=len(features['offsets']), hidden=config['hidden'])
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +116,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'],
+                    nfields=len(features['offsets']), hidden=config['hidden'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -170,11 +172,12 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b', 'W1', 'b1', 'w2')}
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+        if not all(np.isfinite(getattr(model, key)).all() for key in
+                    ('V', 'W', 'b', 'W1', 'b1', 'w2', 'mV', 'vV', 'mW', 'vW', 'mW1', 'vW1', 'mb1', 'vb1', 'mw2', 'vw2')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
             rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
```

---

## Iteration 14: `node_014`

**Status** `success` · **Parent** `node_012` · **Commit** `2930f1536fbd`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (loss formulation, on top of the parent node_012 code exactly as supplied: 9 label-free fields in features.py, plain FM backbone, in-user sampled-softmax listwise training with negs=8). Hypothesis: in the parent, training rows are used ONLY through per-user positive/negative pairs, so every row belonging to a user with no positives (or no negatives) never produces a gradient, and each positive contributes just one softmax group per epoch. Adding a small-weight pointwise binary cross-entropy term over ALL training rows, interleaved with the listwise groups, gives gradient coverage to video/author/tab/duration and prior-history buckets that only appear in single-class users' rows and acts as a global regularizer on the embeddings, while the in-user listwise term keeps driving within-user ordering. This should improve GAUC/nDCG@5 mainly on cold or rarely-updated IDs. Distinction from supplied prior attempts: node_002 replaced pointwise with BPR, node_004 replaced BPR with the listwise softmax, and node_011 only reweighted the existing listwise loss (failed); no experiment has combined pointwise and listwise objectives, and this is not a features, backbone (node_003 FwFM, node_013 DeepFM MLP both worse) or hyperparameter change.

Implementation:
1. config.py: add aux=0.3 to DEFAULTS (all other defaults unchanged: k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8). Extend the float validation loop to `for key in ('lr', 'l2', 'aux')`, keeping the existing condition (finite, >= 0, and lr != 0) so aux=0 cleanly disables the auxiliary term.
2. model.py: change FM.step's signature to step(self, X, y, scale=1.0) and scale the per-row logit gradient by `scale` (g = (scale * (sigmoid(z) - y) / B).astype(np.float32)); everything else in step (L2 terms, single self.t increment, identical Adam update over V and W, self.b -= self.lr * g.sum(), returned unscaled mean BCE) stays exactly as now. Leave logits(), step_pair(), step_list(), predict(), Predictor, read_checkpoint and load_predictor untouched; vars(model) keeps the same key set and shapes so the resume/checkpoint contract is unchanged.
3. train.py: inside the `if len(pos_idx) > 0:` branch, keep the existing per-epoch negative sampling (rel/neg_choice with config['negs']), the rng.permutation(len(pos_idx)) group shuffle and the pos_ord/neg_ord arrays. Instead of running only the listwise batches, build a combined per-epoch schedule: (a) listwise tasks = the batch start offsets i in range(0, len(pos_ord), config['bs']); (b) if config['aux'] > 0, pointwise tasks = batch start offsets over point_ord = rng.permutation(len(ytr)) in steps of config['bs']. Concatenate the two task lists, shuffle their execution order with rng.permutation(total_tasks), and execute in that shuffled order so the two objectives are interleaved within the epoch (validation is therefore never measured right after a solid block of pointwise updates). Listwise tasks call model.step_list(Xtr[pos_ord[i:i+bs]], Xtr[neg_ord[i:i+bs]]) and append to `losses`; pointwise tasks call model.step(Xtr[point_ord[j:j+bs]], ytr[point_ord[j:j+bs]], scale=config['aux']) and append to a separate `aux_losses` list.
4. Keep the existing pointwise-only fallback branch (len(pos_idx) == 0) unchanged, and keep everything else identical: same evaluate(...) on the frozen validation rows/groups, best-primary checkpoint selection, payload['model_state'] over ('V','W','b'), nonfinite guard tuple, patience/early stopping, atomic save_checkpoint, payload fields and resume validation via set(state['latest']) == set(vars(model)). Extend the epoch log line to also print mean(aux_losses) when it is non-empty (e.g. `aux=...`), guarding against an empty list.
Runtime: one extra pass over all training rows per epoch (bs-sized pointwise batches) on top of the ~9x-per-positive listwise work; expect roughly 120-150 s versus the parent's 97 s, well inside candidate_timeout_s and the remaining budget. requirements.txt and features.py stay unchanged.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670624 | 0.537200 | 0.603912 | -0.000602 | 82 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  |  4 ++--
 train.py  | 25 ++++++++++++++++++++++---
 3 files changed, 26 insertions(+), 7 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 26ccf76..4ad47bf 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, aux=0.3)
 
 
 def resolve(overrides):
@@ -33,7 +33,7 @@ def resolve(overrides):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
-    for key in ('lr', 'l2'):
+    for key in ('lr', 'l2', 'aux'):
         if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
             raise ValueError(f'invalid {key}')
     return config
diff --git a/model.py b/model.py
index 4e5afe6..47ac613 100644
--- a/model.py
+++ b/model.py
@@ -48,10 +48,10 @@ class FM:
         inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
         return self.b + self.W[X].sum(1) + inter, E, S
 
-    def step(self, X, y):
+    def step(self, X, y, scale=1.0):
         B = len(y)
         z, E, S = self.logits(X)
-        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
+        g = ((scale * (sigmoid(z) - y)) / B).astype(np.float32)    # (B,)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
         np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
diff --git a/train.py b/train.py
index 48b5404..8d89d78 100644
--- a/train.py
+++ b/train.py
@@ -161,12 +161,30 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             order = rng.permutation(len(pos_idx))
             pos_ord = pos_idx[order]
             neg_ord = neg_choice[order]
-            losses = [model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
-                      for i in range(0, len(pos_ord), config['bs'])]
+            bs = config['bs']
+            list_starts = list(range(0, len(pos_ord), bs))
+            if config['aux'] > 0:
+                point_ord = rng.permutation(len(ytr))
+                point_starts = list(range(0, len(point_ord), bs))
+            else:
+                point_ord = np.empty(0, dtype=np.int64)
+                point_starts = []
+            tasks = [('list', i) for i in list_starts] + [('point', j) for j in point_starts]
+            exec_order = rng.permutation(len(tasks))
+            losses = []
+            aux_losses = []
+            for idx in exec_order:
+                kind, s = tasks[idx]
+                if kind == 'list':
+                    losses.append(model.step_list(Xtr[pos_ord[s:s + bs]], Xtr[neg_ord[s:s + bs]]))
+                else:
+                    aux_losses.append(model.step(Xtr[point_ord[s:s + bs]], ytr[point_ord[s:s + bs]],
+                                                  scale=config['aux']))
         else:
             order = rng.permutation(len(ytr))
             losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
                       for i in range(0, len(order), config['bs'])]
+            aux_losses = []
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
@@ -180,4 +198,5 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
         payload['validation'] = validation
         save_checkpoint(checkpoint_path, payload)
-        print(f'epoch={epoch} loss={np.mean(losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
+        aux_str = f' aux={np.mean(aux_losses):.6f}' if aux_losses else ''
+        print(f'epoch={epoch} loss={np.mean(losses):.6f}{aux_str} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
```

---

## Iteration 15: `node_015`

**Status** `success` · **Parent** `node_012` · **Commit** `f76419850b6f`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (feature encoding / ID-vocabulary regularization -- a subsystem never touched in this lineage; all prior feature work only ADDED new derived fields, and the backbone/loss subsystems have now each failed twice from this parent). Hypothesis: with a temporal split, the plain FM's video_id field currently gives every unseen validation video the vocabulary's 'unknown' slot, whose embedding and linear weight receive ZERO gradient during training (no training row ever maps there), so cold videos are scored with an essentially random/untrained prior while warm videos carry learned scores; additionally, video ids seen only once or twice in training get pure-noise embeddings. Since GAUC/nDCG@5 rank a user's mixed list of warm and cold videos, giving the shared cold bucket a properly trained prior (and denoising ultra-rare video embeddings) should improve within-user ordering at essentially zero extra compute. Distinction from supplied prior attempts: node_001 (popularity count buckets + crosses, on the old pointwise genesis code), node_006 (label target encodings), node_008 and node_012 (label-free user-history fields) all added NEW fields while leaving vocabulary construction untouched; this experiment adds no field and instead changes how the existing video_id field is encoded. No sibling of node_012 (node_013 DeepFM MLP, node_014 aux pointwise loss) touched features.py.

Implementation (edit config.py, features.py, train.py only; model.py and requirements.txt unchanged):
1. config.py: add min_video=3 to DEFAULTS (all other defaults unchanged: k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8) and add 'min_video' to the integer-validation tuple in resolve() so it must be an int >= 1 (min_video=1 exactly reproduces current behavior).
2. features.py: change the signature to fit(rows, min_video=3), keeping every other behavior identical (same duration quantile edges, same raw() ordering, same dates/ndates/nauthors, same ua_keys/u_keys/ud_keys history construction using vocabs[0] and vocabs[2], same dims/offsets/dim computation). Before building the vocabs, count training occurrences of the video id: video_counts = {} accumulated over row[2] for all training rows. Then, in the existing vocab-building loop, skip inserting a value into vocabs[1] when video_counts[value] < min_video (i.e. `if i == 1 and video_counts[value] < min_video: continue`); all other fields (user_id, author_id, tab, duration bucket) keep their full vocabularies so the prior-history keys and their counts are bit-for-bit unchanged. dims stays [len(v) + 1 for v in vocabs] + [7, 8, 8, 8], so the extra slot per field still exists and now serves as a trained shared 'rare/cold video' bucket.
3. features.py transform(rows, state): leave the code exactly as it is -- rare training videos and unseen validation videos both fall through vocab.get(value, len(vocab)) into that same shared bucket, and columns 5-8 (author exposure count, author share, user-duration profile share, author recency gap) are unaffected. No label or same-day information is used anywhere; leakage properties are unchanged.
4. train.py: change the fresh-training call to features = fit(train_rows, config['min_video']). Everything else stays identical: resume path, per-user positive/negative structures, config['negs']=8 in-user sampled-softmax step_list loop, evaluate(...) on the frozen validation rows/groups, best-primary checkpoint selection, patience/early stopping, nonfinite guard, payload key set (config already records min_video), atomic save, and resume validation via set(state['latest']) == set(vars(model)). Optionally print the resulting video vocabulary size once as a diagnostic to stdout.
Runtime: strictly cheaper than the parent (smaller embedding table, same number of steps); expect roughly 90-100 s versus the parent's 97 s, far inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671154 | 0.537311 | 0.604232 | -0.000282 | 73 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py   | 4 ++--
 features.py | 7 ++++++-
 train.py    | 3 ++-
 3 files changed, 10 insertions(+), 4 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 26ccf76..ec2e578 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, min_video=3)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs', 'min_video'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/features.py b/features.py
index 6c42a97..a8ef110 100644
--- a/features.py
+++ b/features.py
@@ -36,11 +36,16 @@ def raw(row, edges):
     return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
 
 
-def fit(rows):
+def fit(rows, min_video=3):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
+    video_counts = {}
+    for row in rows:
+        video_counts[row[2]] = video_counts.get(row[2], 0) + 1
     vocabs = [{} for _ in range(5)]
     for row in rows:
         for i, value in enumerate(raw(row, edges)):
+            if i == 1 and video_counts[value] < min_video:
+                continue
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
 
diff --git a/train.py b/train.py
index 48b5404..8529a51 100644
--- a/train.py
+++ b/train.py
@@ -114,7 +114,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             raise ValueError('invalid checkpoint training progress/settings')
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
-        features = fit(train_rows)
+        features = fit(train_rows, config['min_video'])
+        print(f'video vocabulary size: {len(features["vocabs"][1])}', flush=True)
         model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
```

---

## Iteration 16: `node_016`

**Status** `success` · **Parent** `node_012` · **Commit** `b82f95ec90f8`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (optimizer / regularization subsystem — never touched in this lineage): change the embedding-table update in the listwise training path from a DENSE Adam+L2 update over every row of V and W to a SPARSE ("lazy") Adam update that touches only the feature rows present in the current mini-batch. Edit model.py only; config.py, features.py, train.py and requirements.txt stay exactly as supplied (DEFAULTS remain k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8), and vars(model) keeps the identical key set/shapes so the checkpoint/resume contract in train.py is unchanged.

Hypothesis: today step_list adds `gV += self.l2 * self.V; gW += self.l2 * self.W` over the whole table and then applies Adam to every row every step. For a row that received no batch gradient, its gradient is the pure L2 term, and Adam's per-parameter normalization (m / sqrt(v) ≈ sign) turns that tiny term into a full-size step of magnitude ~lr = 0.001 toward zero. Since embeddings are initialized at std 0.01, every rarely-updated row — long-tail video_id/author_id slots and, critically, the embeddings of low-activity users — is driven to ~0 and then oscillates as noise between its infrequent real updates. Because GAUC averages per user and user×item interaction terms are the only user-specific signal that varies inside a user's candidate list, erasing the embeddings of infrequent users/items should be directly costing within-user ranking quality. Lazy updates preserve learned tail parameters and also cut per-step memory traffic, so the run should be no slower than the parent's 97 s.

Implementation (model.py, FM.step_list only; leave logits(), predict(), step(), step_pair(), Predictor, read_checkpoint and load_predictor untouched so the unused pointwise/BPR fallbacks keep their current behavior):
1. Keep the forward pass, softmax gradient construction and returned loss exactly as now (X_all build, Z reshape, stable softmax, G[:,0] -= 1, G /= B, g_all float32, and the logsumexp-based return value).
2. Accumulate gradients as today with np.add.at into gW and gV (or, equivalently and faster, compute idx, inv = np.unique(X_all, return_inverse=True), reshape inv to X_all's shape, and accumulate into compact buffers of shape (len(idx),) and (len(idx), k)).
3. Compute idx = np.unique(X_all) (sorted unique int indices present in the batch). Form the regularized gradients only for those rows: gVi = gV[idx] + self.l2 * self.V[idx] and gWi = gW[idx] + self.l2 * self.W[idx]. No L2 or Adam step is applied to any row outside idx.
4. Increment self.t exactly once per call as now, and apply the same Adam math (b1=0.9, b2=0.999, eps=1e-8, global bias correction bc1 = 1 - b1**self.t, bc2 = 1 - b2**self.t) restricted to idx: self.mV[idx] = b1*self.mV[idx] + (1-b1)*gVi; self.vV[idx] = b2*self.vV[idx] + (1-b2)*(gVi*gVi); self.V[idx] -= self.lr * (self.mV[idx]/bc1) / (np.sqrt(self.vV[idx]/bc2) + eps); identically for W with mW/vW. Keep all stored arrays float32 (cast the update expression back to float32 on assignment/in-place subtraction). Leave self.b unchanged, as now.
5. Everything else in the pipeline is untouched: features.py's 9 label-free fields, the per-user positive/negative structures, the negs=8 in-user sampled-softmax loop, evaluate(...) on the frozen validation rows/groups, best-primary checkpoint selection, patience/early stopping, the nonfinite guard over ('V','W','b','mV','vV','mW','vW'), payload fields, atomic save and resume validation.

Distinction from supplied prior attempts: siblings of this parent tried a DeepFM MLP head (node_013, worse), an auxiliary pointwise BCE term (node_014, worse) and min-count video vocabulary pruning (node_015, worse); earlier siblings covered weight EMA and lr/epochs, and the lineage covered loss reformulations and added history features. None changed how the optimizer applies updates or where L2 is applied — this experiment changes the update rule itself while keeping loss, features, backbone and all hyperparameter values fixed.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671595 | 0.537453 | 0.604524 | +0.000010 | 119 s |

### Errors and recovery

**Repair attempt 1** — the runner reported an error and the agent was given the diagnostic to correct its own change:

```text
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        request['overrides'], request['context'])
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Admin\Documents\ml-loop\storage\ensemble-001\run-1\workspace\train.py", line 164, in train
    losses = [model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
              ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Admin\Documents\ml-loop\storage\ensemble-001\run-1\workspace\model.py", line 103, in step_list
    np.add.at(gW_c, inv, g_all)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^
ValueError: array is not broadcastable to correct shape
```

Recovered after 1 repair(s); the candidate then evaluated successfully.

### Code diff

```text
model.py | 24 ++++++++++++++++--------
 1 file changed, 16 insertions(+), 8 deletions(-)
```

```diff
diff --git a/model.py b/model.py
index 4e5afe6..6ced5f2 100644
--- a/model.py
+++ b/model.py
@@ -96,16 +96,24 @@ class FM:
         G[:, 0] -= 1.0
         G /= B
         g_all = G.reshape(-1).astype(np.float32)
-        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
-        np.add.at(gW, X_all, g_all[:, None])
-        np.add.at(gV, X_all, g_all[:, None, None] * (S[:, None, :] - E))
-        gV += self.l2 * self.V; gW += self.l2 * self.W
+        idx, inv = np.unique(X_all, return_inverse=True)
+        inv = inv.reshape(X_all.shape)
+        gW_c = np.zeros(len(idx), dtype=np.float32)
+        gV_c = np.zeros((len(idx), self.V.shape[1]), dtype=np.float32)
+        np.add.at(gW_c, inv, g_all[:, None])
+        np.add.at(gV_c, inv, g_all[:, None, None] * (S[:, None, :] - E))
+        gVi = gV_c + self.l2 * self.V[idx]
+        gWi = gW_c + self.l2 * self.W[idx]
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
-        for P_, G_, M_, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
-            M_ *= b1; M_ += (1 - b1) * G_
-            Vv *= b2; Vv += (1 - b2) * (G_ * G_)
-            P_ -= self.lr * (M_ / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        bc1 = 1 - b1 ** self.t
+        bc2 = 1 - b2 ** self.t
+        self.mV[idx] = (b1 * self.mV[idx] + (1 - b1) * gVi).astype(np.float32)
+        self.vV[idx] = (b2 * self.vV[idx] + (1 - b2) * (gVi * gVi)).astype(np.float32)
+        self.V[idx] -= (self.lr * (self.mV[idx] / bc1) / (np.sqrt(self.vV[idx] / bc2) + eps)).astype(np.float32)
+        self.mW[idx] = (b1 * self.mW[idx] + (1 - b1) * gWi).astype(np.float32)
+        self.vW[idx] = (b2 * self.vW[idx] + (1 - b2) * (gWi * gWi)).astype(np.float32)
+        self.W[idx] -= (self.lr * (self.mW[idx] / bc1) / (np.sqrt(self.vW[idx] / bc2) + eps)).astype(np.float32)
         logsumexp = m.squeeze(1) + np.log(expz.sum(1))
         return float(np.mean(logsumexp - Z[:, 0]))
```

---

## Iteration 17: `node_017`

**Status** `success` · **Parent** `node_012` · **Commit** `27ae651b0ecc`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (negative-sampling design inside the existing in-user sampled-softmax objective; train.py ONLY — config.py, features.py, model.py and requirements.txt stay exactly as supplied). Change WHICH negatives form each softmax group: instead of drawing the M = config['negs'] = 8 negatives uniformly from all of a user's label-0 training rows across the whole training window, draw them from the same user's label-0 rows on the SAME DATE as the positive (row[0]), falling back to that user's full negative pool only when the user-day has no negatives, so no positive currently used for training is dropped.

Hypothesis: fields 5-8 added by node_008/node_012 (user×author exposure count, author share, user×duration-bucket share, author recency gap) are time-dependent by construction. Contrasting a day-1 positive against a day-20 negative lets the softmax explain part of the label difference with calendar drift in these history counters rather than with genuine within-context preference, which injects a spurious, non-transferable signal. Same-day negatives hold the user's state and history-counter scale fixed, so the gradient isolates item-level affinity/quality, and it also matches the evaluation setting where a user's candidates come from a common later time window. This should sharpen within-user ordering (GAUC and nDCG@5) at essentially unchanged cost.

Implementation in train.py (replace only the block that builds user_pos/user_neg/eligible_users/pos_idx/neg_start/neg_count/neg_flat, keeping their names, dtypes (int64) and downstream use identical):
1. In a single pass over train_rows with ytr: build day_neg = dict mapping (row[1], row[0]) -> list of row indices with ytr[i] == 0; user_neg = dict mapping row[1] -> list of row indices with ytr[i] == 0; and pos_list = list of (i, row[1], row[0]) for rows with ytr[i] == 1.
2. Build the flat negative pool with de-duplicated group storage: neg_flat_list = [], group_span = {} mapping a pool key to (start, count). For each positive (i, uid, date): pool = day_neg.get((uid, date)); if pool is non-empty use key = ('D', uid, date) else pool = user_neg.get(uid) and key = ('U', uid); if pool is empty or None, skip this positive. If key not in group_span: start = len(neg_flat_list); neg_flat_list.extend(pool); group_span[key] = (start, len(pool)). Append i to pos_idx_list, and the stored start/count to map_start/map_count.
3. Convert to pos_idx, neg_start, neg_count, neg_flat as int64 numpy arrays exactly as today.
4. Leave the per-epoch loop untouched: same rel = np.minimum((rng.random((len(pos_idx), M)) * neg_count[:, None]).astype(np.int64), (neg_count - 1)[:, None]), neg_choice = neg_flat[neg_start[:, None] + rel], rng.permutation group shuffle, config['bs'] batching, model.step_list calls, the len(pos_idx) == 0 pointwise fallback branch, evaluate(...) on the frozen validation rows/groups, best-primary checkpoint selection, patience/early stopping, nonfinite guard, payload['model_state'] over ('V','W','b'), atomic save_checkpoint and resume validation.
5. Print one diagnostic line to stdout before the epoch loop: total training groups, how many use a same-day negative pool, and how many fall back to the user-level pool.

Distinction from supplied prior attempts: node_004 introduced the in-user uniform sampled softmax (negs=8) and no later experiment changed the negative pool; node_011 reweighted the listwise loss (failed), node_014 added an auxiliary pointwise BCE term (failed), node_013 added a DeepFM MLP head (failed), node_015 pruned the video vocabulary (failed), node_016 changed the Adam update to sparse/lazy (flat). This experiment changes only the composition of each softmax group's negatives and leaves loss form, backbone, features, optimizer and all hyperparameters identical.

Runtime: identical step count and shapes as the parent (~97 s), well inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669509 | 0.536716 | 0.603112 | -0.001402 | 81 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
train.py | 48 ++++++++++++++++++++++++++++++++++++------------
 1 file changed, 36 insertions(+), 12 deletions(-)
```

```diff
diff --git a/train.py b/train.py
index 48b5404..fb6e32b 100644
--- a/train.py
+++ b/train.py
@@ -123,28 +123,52 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
 
-    user_pos = {}
+    day_neg = {}
     user_neg = {}
+    pos_list = []
     for i, row in enumerate(train_rows):
         uid = row[1]
+        date = row[0]
         if ytr[i] == 1:
-            user_pos.setdefault(uid, []).append(i)
+            pos_list.append((i, uid, date))
         else:
+            day_neg.setdefault((uid, date), []).append(i)
             user_neg.setdefault(uid, []).append(i)
-    eligible_users = [u for u in user_pos if u in user_neg and len(user_neg[u]) > 0]
+
     pos_idx_list = []
     map_start = []
     map_count = []
     neg_flat_list = []
-    offset = 0
-    for u in eligible_users:
-        negs = user_neg[u]
-        neg_flat_list.extend(negs)
-        for p in user_pos[u]:
-            pos_idx_list.append(p)
-            map_start.append(offset)
-            map_count.append(len(negs))
-        offset += len(negs)
+    group_span = {}
+    n_day = 0
+    n_user = 0
+    for i, uid, date in pos_list:
+        pool = day_neg.get((uid, date))
+        if pool:
+            key = ('D', uid, date)
+            used_day = True
+        else:
+            pool = user_neg.get(uid)
+            key = ('U', uid)
+            used_day = False
+        if not pool:
+            continue
+        if key not in group_span:
+            start = len(neg_flat_list)
+            neg_flat_list.extend(pool)
+            group_span[key] = (start, len(pool))
+        start, count = group_span[key]
+        pos_idx_list.append(i)
+        map_start.append(start)
+        map_count.append(count)
+        if used_day:
+            n_day += 1
+        else:
+            n_user += 1
+
+    print(f'training groups: total={len(pos_idx_list)}, same-day pool={n_day}, user-level fallback={n_user}',
+          flush=True)
+
     pos_idx = np.asarray(pos_idx_list, dtype=np.int64)
     neg_start = np.asarray(map_start, dtype=np.int64)
     neg_count = np.asarray(map_count, dtype=np.int64)
```

---

## Iteration 18: `node_018`

**Status** `success` · **Parent** `node_005` · **Commit** `a956ea530606`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (feature-engineering subsystem, which has never been touched on this branch: features.py here is still the untouched 5-field genesis reference; edit features.py ONLY — config.py, model.py, train.py and requirements.txt stay exactly as supplied). Hypothesis: within-user ranking (GAUC, nDCG@5) can only be improved by signals that vary across items inside a user's group, and the current encoding gives the model nothing but raw IDs plus a 10-bin video-duration bucket, so rare videos/authors are pure cold-start. Adding leakage-free, strictly-prior-date exposure-history features (user–author affinity and item/author popularity) should give the FM generalizable item-side and personalized-affinity evidence and lift Primary on top of the parent's listwise sampled-softmax + EMA training. Distinction from the closest supplied prior attempts: node_001 added static duration bins/popularity buckets/crosses on the pointwise genesis baseline and lost Primary; the other-branch nodes node_008/node_012 did unspecified 'label-free' feature work on a parent without EMA; the memory-flagged failure node_017 changed negative sampling, not features. This experiment is specifically a time-aware, strictly-prior-history count encoding (searchsorted over per-key sorted training date codes), which is a different design from static full-corpus popularity buckets, and it is applied to a parent whose features.py is the unmodified reference.

Implementation (features.py only):
1. In fit(rows): keep the existing duration quantile edges computation unchanged. Additionally build a date-ordering table: dates = sorted(set(r[0] for r in rows)) stored in the fitted state, and define a helper that maps any row date to a code via bisect.bisect_left(dates, row[0]) (an unseen later date maps to len(dates), which is correct and monotone).
2. Build three strictly-prior-history tables from TRAINING ROWS ONLY, each as a compact pair (codes, index): a concatenated np.int32 array 'codes' holding, per key group, the sorted date codes of that key's training rows, plus a dict 'index' mapping key -> (start, end) integer offsets into that array. Tables: (a) 'ua' keyed by (row[1], row[3]) = (user_id, author_id); (b) 'vid' keyed by row[2] = video_id; (c) 'aut' keyed by row[3] = author_id. Use this compact form (not one numpy array per key) so features_state stays small, since train.py pickles it into the checkpoint every epoch.
3. Change raw(row, edges) to raw(row, state) where state carries edges, dates and the three tables. For a row, compute code = bisect.bisect_left(state['dates'], row[0]) and, for each table, look up (start, end) for the key (0 if the key is absent) and take c = int(np.searchsorted(state[t]['codes'][start:end], code)), i.e. the number of training impressions of that key on STRICTLY EARLIER dates. This is label-free and leakage-free: a training row never counts itself or same-day rows, and validation/inference rows (later dates) see the full training history.
4. Bucketize counts with a log helper: bucket(c, cap) = 0 if c <= 0 else min(int(math.log2(c)) + 1, cap); use cap=6 for the user–author count, cap=8 for the video count and cap=8 for the author count. raw() now returns 8 string tokens: the existing 5 (user_id, video_id, author_id, tab, duration-quantile-bin) plus 'ua'+str(bucket(c_ua,6)), 'vp'+str(bucket(c_vid,8)), 'ap'+str(bucket(c_aut,8)).
5. Update fit() to build 8 vocabs (edges and tables must be computed BEFORE the vocab pass, then iterate rows calling raw(row, partial_state) to fill the vocabs), set dims = [len(v)+1 for v in vocabs], offsets = np.cumsum([0]+dims[:-1]).astype(np.int32), dim = sum(dims), and return the state dict containing edges, dates, the three tables, vocabs, offsets and dim. Update transform() to allocate np.empty((len(rows), 8), dtype=np.int32) and use raw(row, state) with the existing unseen-value fallback vocab.get(value, len(vocab)) + offsets[i], preserving input row order.
6. Do not change any interface used elsewhere: fit(rows) / transform(rows, state) signatures, the fitted state being serializable inside the single checkpoint, the train.train and model.load_predictor contracts, the frozen splits, long_view target, ranking groups and evaluation. No config/model/train edits are required (model.FM.logits, step_list and Predictor infer the field count from X.shape).
Runtime: field count goes 5 -> 8 (about 60% more gather/scatter work per listwise step) plus a few seconds of one-time history-table construction and searchsorted lookups during fit/transform; expect roughly 110-140 s versus the parent's 68.6 s, comfortably inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671799 | 0.537578 | 0.604689 | +0.001095 | 125 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 68 +++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 1 file changed, 60 insertions(+), 8 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..06e1008 100644
--- a/features.py
+++ b/features.py
@@ -23,29 +23,81 @@ while preserving the input-row contract and leakage constraints.
 """
 
 # Reference implementation: replaceable while preserving the contracts above.
+import bisect
+import math
+from collections import defaultdict
+
 import numpy as np
 
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+def _bucket(c, cap):
+    if c <= 0:
+        return 0
+    return min(int(math.log2(c)) + 1, cap)
+
+
+def _build_table(rows, keyfunc, dates):
+    groups = defaultdict(list)
+    for row in rows:
+        code = bisect.bisect_left(dates, row[0])
+        groups[keyfunc(row)].append(code)
+    codes_parts = []
+    index = {}
+    offset = 0
+    for key, values in groups.items():
+        values.sort()
+        codes_parts.append(np.asarray(values, dtype=np.int32))
+        index[key] = (offset, offset + len(values))
+        offset += len(values)
+    codes = np.concatenate(codes_parts) if codes_parts else np.empty(0, dtype=np.int32)
+    return dict(codes=codes, index=index)
+
+
+def _lookup(table, key, code):
+    se = table['index'].get(key)
+    if se is None:
+        return 0
+    start, end = se
+    sub = table['codes'][start:end]
+    return int(np.searchsorted(sub, code))
+
+
+def raw(row, state):
+    code = bisect.bisect_left(state['dates'], row[0])
+    c_ua = _lookup(state['ua'], (row[1], row[3]), code)
+    c_vid = _lookup(state['vid'], row[2], code)
+    c_aut = _lookup(state['aut'], row[3], code)
+    bin_idx = str(int(np.searchsorted(state['edges'], row[5])))
+    return [row[1], row[2], row[3], row[4], bin_idx,
+            'ua' + str(_bucket(c_ua, 6)),
+            'vp' + str(_bucket(c_vid, 8)),
+            'ap' + str(_bucket(c_aut, 8))]
 
 
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    dates = sorted(set(r[0] for r in rows))
+    ua = _build_table(rows, lambda r: (r[1], r[3]), dates)
+    vid = _build_table(rows, lambda r: r[2], dates)
+    aut = _build_table(rows, lambda r: r[3], dates)
+
+    partial_state = dict(edges=edges, dates=dates, ua=ua, vid=vid, aut=aut)
+
+    vocabs = [{} for _ in range(8)]
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
+        for i, value in enumerate(raw(row, partial_state)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
-    return dict(edges=edges, vocabs=vocabs,
-                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
+    offsets = np.cumsum([0] + dims[:-1]).astype(np.int32)
+    return dict(edges=edges, dates=dates, ua=ua, vid=vid, aut=aut,
+                vocabs=vocabs, offsets=offsets, dim=sum(dims))
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 5), dtype=np.int32)
+    result = np.empty((len(rows), 8), dtype=np.int32)
     for n, row in enumerate(rows):
-        for i, value in enumerate(raw(row, state['edges'])):
+        for i, value in enumerate(raw(row, state)):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
     return result
```

---

## Iteration 19: `node_019`

**Status** `success` · **Parent** `node_018` · **Commit** `0574ad93dc14`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (feature engineering, continuing the only direction that has produced a gain on this branch; edit features.py ONLY — config.py, model.py, train.py, requirements.txt stay exactly as supplied). Hypothesis: GAUC and nDCG@5 are within-user ranking metrics, so only signals that differ across items inside a user's group can reorder them. The parent's features add absolute prior-exposure COUNTS (user-author, video, author), but nothing tells the model how well an item's length matches the user's own consumption habit, how old the item is, or whether it is currently trending. Adding (a) a user-relative duration mismatch bin, (b) an item-age (freshness) bin, and (c) a short-window trending-popularity bin should give globally shared, cold-start-friendly item-side and user-conditional evidence that plain ID embeddings and total counts cannot express, lifting Primary above the parent's 0.60469.

Implementation (features.py only; keep fit(rows)/transform(rows, state)/raw() usable exactly as now, keep the existing 8 tokens, the edges quantiles, the `dates` list, the ua/vid/aut prior-count tables, the `_bucket` helper, and the serializable-state contract unchanged):
1. In fit(), after the existing tables are built, add a per-user duration prefix table `udur` built from TRAINING ROWS ONLY: for every training row compute code = bisect.bisect_left(dates, row[0]) and value = math.log2(1.0 + max(row[5], 0)); group by row[1] (user_id); within each group sort by code; store a flat np.int32 array `codes` of the sorted codes, a flat np.float32 array `cum` holding the within-group cumulative sum of the sorted values, and an `index` dict user_id -> (start, end) offsets into those flat arrays (same compact layout as _build_table so the state stays small when train.py pickles it every epoch).
2. Extend raw(row, state) to return 11 tokens: the current 8 plus
   a) 'rd' token (user-relative duration): let (start, end) = udur['index'].get(row[1]); if absent use token 'rdna'; else idx = int(np.searchsorted(udur['codes'][start:end], code)) (strictly earlier dates only); if idx == 0 use 'rdna'; else mean_prior = float(udur['cum'][start + idx - 1]) / idx and delta = math.log2(1.0 + max(row[5], 0)) - mean_prior; token = 'rd' + str(int(np.clip(round(delta * 2.0), -8, 8))) (half-log2 steps, 17 possible bins).
   b) 'vf' token (item age): reuse the existing vid table; if row[2] is absent from vid['index'] use 'vfnew'; else age = code - int(vid['codes'][start]) (first training impression date code of that video) and token = 'vf' + str(_bucket(age, 6)) with age <= 0 mapping to 'vf0'.
   c) 'vr' token (short-window trending popularity): reuse the same vid slice sub = vid['codes'][start:end]; hi = int(np.searchsorted(sub, code)), lo = int(np.searchsorted(sub, code - 3)); recent = hi - lo; token = 'vr' + str(_bucket(recent, 6)); use 'vr0' when the video key is absent.
3. Update fit() to build the partial_state including `udur` BEFORE the vocab pass, use 11 vocabs, dims = [len(v)+1 for v in vocabs], offsets = np.cumsum([0]+dims[:-1]).astype(np.int32), dim = sum(dims), and return a state dict containing edges, dates, ua, vid, aut, udur, vocabs, offsets, dim. Update transform() to allocate np.empty((len(rows), 11), dtype=np.int32) with the same unseen-value fallback vocab.get(value, len(vocab)) + offsets[i], preserving input row order.
4. Leakage/contract safety: all three new signals use exposure metadata (dates and duration_ms) only, never the long_view target; the user-duration mean uses strictly earlier date codes (idx computed with searchsorted before the row's own code), so a training row never sees itself or same-day rows, and validation/inference rows (later dates) see the full training history. No changes to splits, target, grouping, evaluation, train.train, or model.load_predictor; model.FM.logits/step_list/Predictor infer the field count from X.shape[1], so no other file needs editing.

Distinction from the closest supplied prior attempts: node_018 (the parent) added absolute strictly-prior COUNT buckets (user-author, video, author) — this experiment adds no new count-of-key feature but instead user-relative duration matching, item age since first exposure, and a 3-day recent-popularity window; node_001 added static full-corpus duration bins/popularity buckets and crosses on the pointwise genesis baseline, which is neither time-windowed nor user-relative. No supplied experiment has tried recency/age or user-normalized duration features.

Runtime: field count 8 -> 11 (about 35% more gather/scatter work per listwise step) plus two extra searchsorted lookups per row during fit/transform; expect roughly 150-190 s versus the parent's 124.7 s, comfortably inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.671054 | 0.537565 | 0.604309 | -0.000380 | 160 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 66 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----
 1 file changed, 61 insertions(+), 5 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 06e1008..5acc910 100644
--- a/features.py
+++ b/features.py
@@ -62,16 +62,71 @@ def _lookup(table, key, code):
     return int(np.searchsorted(sub, code))
 
 
+def _build_udur(rows, dates):
+    groups = defaultdict(list)
+    for row in rows:
+        code = bisect.bisect_left(dates, row[0])
+        value = math.log2(1.0 + max(row[5], 0))
+        groups[row[1]].append((code, value))
+    codes_parts = []
+    cum_parts = []
+    index = {}
+    offset = 0
+    for key, pairs in groups.items():
+        pairs.sort(key=lambda p: p[0])
+        codes = np.asarray([p[0] for p in pairs], dtype=np.int32)
+        cum = np.cumsum([p[1] for p in pairs]).astype(np.float32)
+        codes_parts.append(codes)
+        cum_parts.append(cum)
+        index[key] = (offset, offset + len(pairs))
+        offset += len(pairs)
+    codes = np.concatenate(codes_parts) if codes_parts else np.empty(0, dtype=np.int32)
+    cum = np.concatenate(cum_parts) if cum_parts else np.empty(0, dtype=np.float32)
+    return dict(codes=codes, cum=cum, index=index)
+
+
 def raw(row, state):
     code = bisect.bisect_left(state['dates'], row[0])
     c_ua = _lookup(state['ua'], (row[1], row[3]), code)
     c_vid = _lookup(state['vid'], row[2], code)
     c_aut = _lookup(state['aut'], row[3], code)
     bin_idx = str(int(np.searchsorted(state['edges'], row[5])))
+
+    udur = state['udur']
+    se = udur['index'].get(row[1])
+    if se is None:
+        rd_token = 'rdna'
+    else:
+        start, end = se
+        idx = int(np.searchsorted(udur['codes'][start:end], code))
+        if idx == 0:
+            rd_token = 'rdna'
+        else:
+            mean_prior = float(udur['cum'][start + idx - 1]) / idx
+            delta = math.log2(1.0 + max(row[5], 0)) - mean_prior
+            rd_token = 'rd' + str(int(np.clip(round(delta * 2.0), -8, 8)))
+
+    vid = state['vid']
+    vse = vid['index'].get(row[2])
+    if vse is None:
+        vf_token = 'vfnew'
+        vr_token = 'vr0'
+    else:
+        vstart, vend = vse
+        first_code = int(vid['codes'][vstart])
+        age = code - first_code
+        vf_token = 'vf0' if age <= 0 else 'vf' + str(_bucket(age, 6))
+        sub = vid['codes'][vstart:vend]
+        hi = int(np.searchsorted(sub, code))
+        lo = int(np.searchsorted(sub, code - 3))
+        recent = hi - lo
+        vr_token = 'vr' + str(_bucket(recent, 6))
+
     return [row[1], row[2], row[3], row[4], bin_idx,
             'ua' + str(_bucket(c_ua, 6)),
             'vp' + str(_bucket(c_vid, 8)),
-            'ap' + str(_bucket(c_aut, 8))]
+            'ap' + str(_bucket(c_aut, 8)),
+            rd_token, vf_token, vr_token]
 
 
 def fit(rows):
@@ -80,22 +135,23 @@ def fit(rows):
     ua = _build_table(rows, lambda r: (r[1], r[3]), dates)
     vid = _build_table(rows, lambda r: r[2], dates)
     aut = _build_table(rows, lambda r: r[3], dates)
+    udur = _build_udur(rows, dates)
 
-    partial_state = dict(edges=edges, dates=dates, ua=ua, vid=vid, aut=aut)
+    partial_state = dict(edges=edges, dates=dates, ua=ua, vid=vid, aut=aut, udur=udur)
 
-    vocabs = [{} for _ in range(8)]
+    vocabs = [{} for _ in range(11)]
     for row in rows:
         for i, value in enumerate(raw(row, partial_state)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
     offsets = np.cumsum([0] + dims[:-1]).astype(np.int32)
-    return dict(edges=edges, dates=dates, ua=ua, vid=vid, aut=aut,
+    return dict(edges=edges, dates=dates, ua=ua, vid=vid, aut=aut, udur=udur,
                 vocabs=vocabs, offsets=offsets, dim=sum(dims))
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 8), dtype=np.int32)
+    result = np.empty((len(rows), 11), dtype=np.int32)
     for n, row in enumerate(rows):
         for i, value in enumerate(raw(row, state)):
             vocab = state['vocabs'][i]
```

---

## Iteration 20: `node_020`

**Status** `success` · **Parent** `node_018` · **Commit** `982b6c9d7732`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (model-averaging / ensembling subsystem in score space — never tried on this branch; edit config.py, model.py and train.py; leave features.py and requirements.txt exactly as supplied). Hypothesis: the current single FM is trained with a high-variance objective (per-epoch resampled in-user negatives) over very sparse ID embeddings, so a single trajectory's parameters are noisy; node_005 showed that weight-space EMA along ONE trajectory gives almost nothing (+0.00007), but averaging the scores of INDEPENDENTLY initialized and independently negative-sampled models captures init + sampling diversity that weight-space averaging cannot, and should reduce ranking noise and lift within-user ordering (GAUC and nDCG@5) on top of the parent's listwise sampled-softmax + EMA + prior-history features. Distinction from the closest supplied prior attempts: node_005 added EMA weight averaging of a single model (kept unchanged here), node_003 replaced the backbone with FwFM, node_017 changed negative sampling and node_019 added more feature tokens; no supplied experiment trains multiple models or averages predictions.

Implementation:
1. config.py: add key members=2 to DEFAULTS (keep k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99 unchanged) and include 'members' in the existing integer-validation loop so a non-int or value < 1 raises ValueError. Keep the unknown-key check as is.
2. model.py (do not change FM.logits, step, step_pair, step_list, update_ema, ema_weights, predict_ema, predict, read_checkpoint, or the load_predictor signature): change Predictor to consume an ensemble checkpoint. state['model_state'] is now a dict of the form {'members': [ {'V','W','b'}, ... ]}. Predictor.__init__ builds one FM per member with FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed']) and assigns each member's V/W/b after validating shape match and np.isfinite for every array (raise ValueError('incompatible or nonfinite model weights: ' + name) on failure); raise a clear ValueError if 'members' is missing or empty. Predictor.predict(rows) transforms rows once with transform(rows, self.features) and returns the plain arithmetic mean of the member logit vectors (no per-batch standardization, so scores stay independent of batch composition), still returning np.empty(0, dtype=np.float32) for empty input and preserving row order.
3. train.py: train config['members'] FM instances sequentially inside the existing epoch loop instead of one. Construct models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + m) for m in range(config['members'])] and one independent generator per member, rngs = [np.random.default_rng([config['seed'], m]) for m in range(config['members'])], so each member draws its own negatives and shuffles. Keep the per-user pair structures (pos_idx, neg_start, neg_count, neg_flat) built exactly as now (shared across members). In each epoch, for every member that has not early-stopped (its own bad counter < config['patience']): sample its (P, negs) negatives with its own rng, permute, run the existing mini-batch loop calling model.step_list(...) followed by model.update_ema(config['ema']) after every step, then compute that member's validation_raw = evaluate(..., model.predict(Xva)) and validation_ema = evaluate(..., model.predict_ema(Xva, config['ema'])) on the same frozen validation rows/grouping, select the higher-primary variant (prefer raw on ties) and, if it beats that member's own best by more than 1e-5, store that member's best weights (deepcopy of {'V','W','b'} from the model, or from model.ema_weights(config['ema']) for the ema variant) and reset its bad counter, else increment it. Keep the pointwise model.step fallback branch (with update_ema) for the len(pos_idx) == 0 case, per member. After all members have been processed in an epoch, set payload['model_state'] = {'members': [best weights of each member (falling back to the member's current weights if it has no best yet)]}, compute the ensemble validation by averaging the member best-weight logit vectors on Xva (build the same averaged score used at inference, e.g. by instantiating model.Predictor-equivalent scoring or by averaging model.predict outputs after temporarily loading each member's best weights) and store it in payload['validation'], set payload['best_epoch'] = the epoch index at which the last member improvement occurred, keep payload key set unchanged (version, config, features_state, model_state, training_state, context, validation, best_epoch), keep the atomic save_checkpoint call and one log line per epoch reporting each member's raw/ema primaries plus the ensemble primary. Break out of the epoch loop when every member has bad >= config['patience'].
4. Resume/consistency: extend payload['training_state'] to dict(epoch=epoch, best=<list of per-member bests>, bad=<list of per-member bad counters>, rng=[r.bit_generator.state for r in rngs], latest=[copy.deepcopy(vars(m)) for m in models]) and update the resume branch to rebuild config['members'] FM instances, require len(state['latest']) == config['members'] and set(entry) == set(vars(model)) for each member (raise ValueError('incomplete optimizer/model state') otherwise), restore each member's arrays with the existing shape/finite checks, restore each generator state, and keep the existing epoch/bad/best sanity checks generalized over the per-member lists. Apply the existing nonfinite guard over ('V','W','b','mV','vV','mW','vW','eV','eW','eb') to every member. Keep Predictor(payload) validation before resuming.
Everything else (features.py encoding, listwise sampled-softmax loss with negs=8, EMA decay, splits, long_view target, ranking groups, evaluation) stays exactly as supplied. Runtime: two members roughly double the parent's 124.7 s training work plus two extra validation passes per epoch, i.e. about 230-270 s, well inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.672447 | 0.537976 | 0.605211 | +0.000523 | 183 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |   4 +-
 model.py  |  22 +++++---
 train.py  | 175 ++++++++++++++++++++++++++++++++++++++++----------------------
 3 files changed, 131 insertions(+), 70 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 9b674c5..96c30a0 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99, members=2)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negs', 'members'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 773ef8c..158e037 100644
--- a/model.py
+++ b/model.py
@@ -158,13 +158,19 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
         weights = state['model_state']
-        for name in ('V', 'W', 'b'):
-            value = weights[name]
-            if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
-                raise ValueError('incompatible or nonfinite model weights: ' + name)
-            setattr(self.model, name, value)
+        members = weights.get('members') if isinstance(weights, dict) else None
+        if not members:
+            raise ValueError('missing or empty ensemble members in model_state')
+        self.models = []
+        for member in members:
+            model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+            for name in ('V', 'W', 'b'):
+                value = member[name]
+                if np.shape(value) != np.shape(getattr(model, name)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite model weights: ' + name)
+                setattr(model, name, value)
+            self.models.append(model)
 
     def predict(self, rows):
         """Return one finite real-valued score per row, preserving input order.
@@ -175,7 +181,9 @@ class Predictor:
         """
         if not len(rows):
             return np.empty(0, dtype=np.float32)
-        return self.model.predict(transform(rows, self.features))
+        X = transform(rows, self.features)
+        scores = np.mean([model.predict(X) for model in self.models], axis=0)
+        return scores.astype(np.float32)
 
 
 def load_predictor(checkpoint_path):
diff --git a/train.py b/train.py
index 0a6dfa1..fe8b838 100644
--- a/train.py
+++ b/train.py
@@ -73,6 +73,15 @@ from features import fit, transform
 from model import FM, Predictor, read_checkpoint
 
 
+def FM_predict_with(model, weights, X):
+    V0, W0, b0 = model.V, model.W, model.b
+    try:
+        model.V, model.W, model.b = weights['V'], weights['W'], weights['b']
+        return model.predict(X)
+    finally:
+        model.V, model.W, model.b = V0, W0, b0
+
+
 def save_checkpoint(path, payload):
     temporary = None
     try:
@@ -89,7 +98,8 @@ def save_checkpoint(path, payload):
 
 def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     config = resolve(overrides)
-    rng = np.random.default_rng(config['seed'])
+    n_members = config['members']
+    rngs = [np.random.default_rng([config['seed'], m]) for m in range(n_members)]
     if Path(checkpoint_path).exists():
         payload = read_checkpoint(checkpoint_path)
         if payload['config'] != config or payload['context'] != context:
@@ -97,28 +107,49 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         Predictor(payload)  # Validate inference weights before resuming.
         features = payload['features_state']
         state = payload['training_state']
-        rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
-        if set(state['latest']) != set(vars(model)):
+        if len(state['latest']) != n_members:
             raise ValueError('incomplete optimizer/model state')
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
+        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + m)
+                  for m in range(n_members)]
+        for m, model in enumerate(models):
+            entry = state['latest'][m]
+            if set(entry) != set(vars(model)):
+                raise ValueError('incomplete optimizer/model state')
+            for key, value in entry.items():
+                if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite latest state: ' + key)
+                setattr(model, key, value)
+        for m, r in enumerate(rngs):
+            r.bit_generator.state = state['rng'][m]
+        best_list, bad_list, epoch = state['best'], state['bad'], state['epoch']
+        if len(best_list) != n_members or len(bad_list) != n_members:
             raise ValueError('invalid checkpoint training progress/settings')
-        print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
+        for m, model in enumerate(models):
+            best, bad = best_list[m], bad_list[m]
+            if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
+                    or type(bad) is not int or not 0 <= bad <= config['patience']
+                    or not np.isfinite(best) or not 0 <= best <= 1
+                    or model.lr != config['lr'] or model.l2 != config['l2']
+                    or type(model.t) is not int or model.t < 1):
+                raise ValueError('invalid checkpoint training progress/settings')
+        best_weights = payload.get('model_state', {}).get('members') if 'model_state' in payload else None
+        best = list(best_list)
+        bad = list(bad_list)
+        print(f'resume: completed epoch={epoch}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
-        best, bad, epoch = -1.0, 0, 0
+        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + m)
+                  for m in range(n_members)]
+        best = [-1.0] * n_members
+        bad = [0] * n_members
+        epoch = 0
         payload = dict(version=1, config=config, features_state=features, context=context)
+        best_weights = None
         print('fresh training', flush=True)
+    if best_weights is None:
+        best_weights = [None] * n_members
+    else:
+        best_weights = [copy.deepcopy(w) for w in best_weights]
     Xtr = transform(train_rows, features)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
@@ -150,51 +181,73 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     neg_count = np.asarray(map_count, dtype=np.int64)
     neg_flat = np.asarray(neg_flat_list, dtype=np.int64)
 
+    best_epoch = payload.get('best_epoch', 0)
+    valid_uids = [r[1] for r in valid_rows]
+    valid_y = [r[6] for r in valid_rows]
+
     for epoch in range(epoch + 1, config['epochs'] + 1):
-        if bad >= config['patience']:
+        if all(b >= config['patience'] for b in bad):
             break
-        if len(pos_idx) > 0:
-            M = config['negs']
-            rel = np.minimum((rng.random((len(pos_idx), M)) * neg_count[:, None]).astype(np.int64),
-                              (neg_count - 1)[:, None])
-            neg_choice = neg_flat[neg_start[:, None] + rel]
-            order = rng.permutation(len(pos_idx))
-            pos_ord = pos_idx[order]
-            neg_ord = neg_choice[order]
-            losses = []
-            for i in range(0, len(pos_ord), config['bs']):
-                loss = model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
-                losses.append(loss)
-                model.update_ema(config['ema'])
-        else:
-            order = rng.permutation(len(ytr))
-            losses = []
-            for i in range(0, len(order), config['bs']):
-                loss = model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                losses.append(loss)
-                model.update_ema(config['ema'])
-        validation_raw = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
-        validation_ema = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows],
-                                   model.predict_ema(Xva, config['ema']))
-        if validation_ema['primary'] > validation_raw['primary']:
-            validation, variant = validation_ema, 'ema'
-        else:
-            validation, variant = validation_raw, 'raw'
-        if validation['primary'] > best + 1e-5:
-            best, bad = validation['primary'], 0
-            if variant == 'ema':
-                payload['model_state'] = copy.deepcopy(model.ema_weights(config['ema']))
+        log_parts = []
+        for m in range(n_members):
+            if bad[m] >= config['patience']:
+                continue
+            model = models[m]
+            r = rngs[m]
+            if len(pos_idx) > 0:
+                M = config['negs']
+                rel = np.minimum((r.random((len(pos_idx), M)) * neg_count[:, None]).astype(np.int64),
+                                  (neg_count - 1)[:, None])
+                neg_choice = neg_flat[neg_start[:, None] + rel]
+                order = r.permutation(len(pos_idx))
+                pos_ord = pos_idx[order]
+                neg_ord = neg_choice[order]
+                losses = []
+                for i in range(0, len(pos_ord), config['bs']):
+                    loss = model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
+                    losses.append(loss)
+                    model.update_ema(config['ema'])
             else:
-                payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
-            payload['best_epoch'] = epoch
-        else:
-            bad += 1
-        if not all(np.isfinite(getattr(model, key)).all()
-                   for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'eV', 'eW', 'eb')):
-            raise ValueError('nonfinite training state; keeping last valid checkpoint')
-        payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
-            rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
-        payload['validation'] = validation
+                order = r.permutation(len(ytr))
+                losses = []
+                for i in range(0, len(order), config['bs']):
+                    loss = model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
+                    losses.append(loss)
+                    model.update_ema(config['ema'])
+            validation_raw = evaluate(valid_uids, valid_y, model.predict(Xva))
+            validation_ema = evaluate(valid_uids, valid_y, model.predict_ema(Xva, config['ema']))
+            if validation_ema['primary'] > validation_raw['primary']:
+                validation, variant = validation_ema, 'ema'
+            else:
+                validation, variant = validation_raw, 'raw'
+            if validation['primary'] > best[m] + 1e-5:
+                best[m], bad[m] = validation['primary'], 0
+                if variant == 'ema':
+                    best_weights[m] = copy.deepcopy(model.ema_weights(config['ema']))
+                else:
+                    best_weights[m] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+                best_epoch = epoch
+            else:
+                bad[m] += 1
+            if not all(np.isfinite(getattr(model, key)).all()
+                       for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'eV', 'eW', 'eb')):
+                raise ValueError('nonfinite training state; keeping last valid checkpoint')
+            log_parts.append(f'member={m} loss={np.mean(losses):.6f} primary_raw={validation_raw["primary"]:.6f} '
+                              f'primary_ema={validation_ema["primary"]:.6f} selected={variant}')
+
+        current_weights = [best_weights[m] if best_weights[m] is not None
+                            else {key: copy.deepcopy(getattr(models[m], key)) for key in ('V', 'W', 'b')}
+                            for m in range(n_members)]
+        ensemble_scores = np.mean([FM_predict_with(models[m], current_weights[m], Xva) for m in range(n_members)],
+                                   axis=0)
+        ensemble_validation = evaluate(valid_uids, valid_y, ensemble_scores)
+
+        payload['model_state'] = {'members': [copy.deepcopy(w) for w in current_weights]}
+        payload['best_epoch'] = best_epoch
+        payload['validation'] = ensemble_validation
+        payload['training_state'] = dict(epoch=epoch, best=list(best), bad=list(bad),
+            rng=[r.bit_generator.state for r in rngs],
+            latest=[copy.deepcopy(vars(m)) for m in models])
         save_checkpoint(checkpoint_path, payload)
-        print(f'epoch={epoch} loss={np.mean(losses):.6f} primary_raw={validation_raw["primary"]:.6f} '
-              f'primary_ema={validation_ema["primary"]:.6f} selected={variant} checkpoint saved', flush=True)
+        print(f'epoch={epoch} ' + ' | '.join(log_parts) +
+              f' | ensemble_primary={ensemble_validation["primary"]:.6f} checkpoint saved', flush=True)
```

---

## Iteration 21: `node_021`

**Status** `success` · **Parent** `node_020` · **Commit** `52a281a3146b`

### Hypothesis

```text
SELECTED CHANGE
EXPERIMENT (loss-formulation subsystem: temperature-scaled in-user sampled softmax). Hypothesis: the parent already trains each ensemble member with an in-user sampled-softmax over 1 positive plus negs=8 uniformly sampled same-user negatives at an implicit temperature of 1.0, which spreads gradient mass roughly evenly across all sampled negatives. GAUC and especially nDCG@5 are top-heavy within-user metrics, so sharpening the softmax (temperature tau < 1) concentrates the gradient on the currently highest-scoring (hardest) in-user negatives and should push the positive above the items that actually occupy the top of each user's list. Because Adam normalizes per-parameter gradient scale, tau mainly re-weights negatives rather than changing the effective step size, so this is a cheap, low-risk knob. Distinction from supplied prior attempts: node_004 introduced the multi-negative softmax loss itself (tau implicitly 1.0) and node_017 on another branch changed the negative SAMPLING distribution (flagged as a failure); no supplied experiment has changed the softmax temperature / hard-negative weighting of the existing loss. Runtime must stay essentially identical to the parent's 182.7 s.

Implementation (edit config.py, model.py, train.py; leave features.py and requirements.txt exactly as supplied):
1. config.py: add key tau=0.5 to DEFAULTS (keep k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99, members=2 unchanged). Validate it next to the existing ema check: raise ValueError('invalid tau') if it is not finite or tau <= 0. Keep the unknown-key check as is.
2. model.py: change FM.step_list(self, Xp, Xn) to FM.step_list(self, Xp, Xn, tau=1.0), leaving logits(), step(), step_pair(), update_ema(), ema_weights(), predict_ema(), predict(), read_checkpoint(), Predictor and load_predictor untouched. Inside step_list, after computing Z = z_all.reshape(B, 1 + M), form the scaled scores Zs = Z / tau, subtract the row max for stability, compute expz = exp(Zs - m) and P = expz / expz.sum(1, keepdims=True); build the per-row logit gradient as G = P.copy(); G[:, 0] -= 1.0; G /= (tau * B) (the extra 1/tau comes from dZs/dZ), then reshape to g_all and keep the existing np.add.at accumulation into gW and gV, the existing l2 terms, and the identical Adam block with the single self.t increment and shared mV/vV/mW/vW buffers (so vars(model) key set and the resume contract are unchanged). Return the temperature-scaled listwise loss float(np.mean((m.squeeze(1) + np.log(expz.sum(1))) - Zs[:, 0])).
3. train.py: pass the configured temperature at the single call site, i.e. model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]], config['tau']). Everything else stays byte-for-byte equivalent: per-member rngs and negative sampling, model.update_ema(config['ema']) after every step, per-member raw-vs-EMA validation selection, per-member best weights, the {'members': [...]} model_state, ensemble validation via FM_predict_with, payload key set, nonfinite guard, patience/early stopping, atomic save_checkpoint, and the resume path.
Inference is unaffected because the temperature only rescales the training gradient; Predictor still averages raw member logits. Expected wall clock roughly equal to the parent's 182.7 s, comfortably inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.672574 | 0.537937 | 0.605256 | +0.000044 | 169 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 model.py  | 11 ++++++-----
 train.py  |  3 ++-
 3 files changed, 11 insertions(+), 7 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 96c30a0..45b2500 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99, members=2)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99, members=2, tau=0.5)
 
 
 def resolve(overrides):
@@ -38,4 +38,6 @@ def resolve(overrides):
             raise ValueError(f'invalid {key}')
     if not math.isfinite(config['ema']) or not 0 < config['ema'] < 1:
         raise ValueError('invalid ema')
+    if not math.isfinite(config['tau']) or config['tau'] <= 0:
+        raise ValueError('invalid tau')
     return config
diff --git a/model.py b/model.py
index 158e037..5363879 100644
--- a/model.py
+++ b/model.py
@@ -113,17 +113,18 @@ class FM:
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         return float(np.mean(-np.log(sigmoid(z_p - z_n) + 1e-9)))
 
-    def step_list(self, Xp, Xn):
+    def step_list(self, Xp, Xn, tau=1.0):
         B, M = Xn.shape[0], Xn.shape[1]
         X_all = np.concatenate([Xp[:, None, :], Xn], axis=1).reshape(B * (1 + M), -1)
         z_all, E, S = self.logits(X_all)
         Z = z_all.reshape(B, 1 + M)
-        m = Z.max(1, keepdims=True)
-        expz = np.exp(Z - m)
+        Zs = Z / tau
+        m = Zs.max(1, keepdims=True)
+        expz = np.exp(Zs - m)
         P = expz / expz.sum(1, keepdims=True)
         G = P.copy()
         G[:, 0] -= 1.0
-        G /= B
+        G /= (tau * B)
         g_all = G.reshape(-1).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X_all, g_all[:, None])
@@ -136,7 +137,7 @@ class FM:
             Vv *= b2; Vv += (1 - b2) * (G_ * G_)
             P_ -= self.lr * (M_ / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         logsumexp = m.squeeze(1) + np.log(expz.sum(1))
-        return float(np.mean(logsumexp - Z[:, 0]))
+        return float(np.mean(logsumexp - Zs[:, 0]))
 
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
diff --git a/train.py b/train.py
index fe8b838..605b5be 100644
--- a/train.py
+++ b/train.py
@@ -204,7 +204,8 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
                 neg_ord = neg_choice[order]
                 losses = []
                 for i in range(0, len(pos_ord), config['bs']):
-                    loss = model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]])
+                    loss = model.step_list(Xtr[pos_ord[i:i + config['bs']]], Xtr[neg_ord[i:i + config['bs']]],
+                                            config['tau'])
                     losses.append(loss)
                     model.update_ema(config['ema'])
             else:
```

---

## Iteration 22: `node_022`

**Status** `failed` · **Parent** `node_020` · **Commit** `be2bd6b0dd3c`

### Hypothesis

```text
SELECTED CHANGE
Experiment (FM optimizer hyperparameters — the one subsystem never touched anywhere in this lineage; every prior node changed the loss (BPR, sampled softmax, temperature), weight EMA, features, or score-space ensembling, while k=16, lr=0.001, l2=1e-6 have been inherited unchanged since genesis): raise the base Adam learning rate from 0.001 to 0.003 and leave everything else in the parent exactly as supplied.

Hypothesis: each member is trained with a listwise in-user sampled softmax whose gradient reaches only the handful of ID embeddings touched per group, so most sparse embeddings (rare video_id/author_id, the new prior-history buckets) receive very few effective updates before early stopping fires at patience=4. A 3x larger step size lets these rare-ID and history-bucket embeddings reach useful magnitudes within the available epochs, which should sharpen within-user ordering (GAUC and nDCG@5). The existing per-step EMA (decay 0.99, ~100-step average) plus the per-epoch raw-vs-EMA selection already in train.py provides a built-in guard against the extra iterate noise a larger lr introduces, and the 2-member score-space ensemble further averages sampling noise, so this parent is the right place to test a more aggressive step size.

Implementation: edit config.py only. In DEFAULTS change lr=0.001 to lr=0.003, keeping k=16, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99, members=2 exactly as they are, and keep resolve()'s unknown-key check and all existing integer/float/ema validations unchanged (lr must still be finite and > 0). Do not modify features.py, model.py, train.py, or requirements.txt: the listwise step_list objective, per-member independent rngs and negative sampling, update_ema after every step, per-member best-weight selection, {'members': [...]} model_state, ensemble validation via FM_predict_with, checkpoint payload key set, resume path, and the frozen splits/target/groups/evaluation all stay identical, so the learning rate is the only varied factor.

Distinction from the closest supplied prior attempts: sibling node_021 changed the softmax temperature (a loss re-weighting that Adam largely normalizes away, +0.00004), node_005 added weight EMA, node_018/node_019 changed features, and node_020 added ensembling; no supplied experiment has altered lr, k, or l2. Runtime: identical per-epoch cost to the parent and likely fewer epochs before patience triggers, so expect at most the parent's ~183 s and probably less, comfortably inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

No metrics: the candidate did not produce a valid evaluation.

### Errors and recovery

The candidate failed after its repair budget was exhausted. Under best-first selection this leaves the parent's score unchanged and is recorded as an implementation failure, not as evidence against the proposed approach.

### Code diff

```text
config.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

```diff
diff --git a/config.py b/config.py
index 96c30a0..bfc6dc9 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99, members=2)
+DEFAULTS = dict(k=16, lr=0.003, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negs=8, ema=0.99, members=2)
 
 
 def resolve(overrides):
```

