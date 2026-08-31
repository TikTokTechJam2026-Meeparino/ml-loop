# Run log: run-2

Run id `7d05762f263a4080a4ec3bf203232a0c` · evaluation protocol `cfe7881824a34480…` · schema 1

## Summary

| | |
|---|---|
| Candidate iterations | 16 of 50 permitted |
| Candidate outcomes | 16 success |
| Stop reason | `stagnation` |
| Baseline (`genesis`) | Primary 0.601469 |
| Selected (`node_006`) | Primary 0.603938 |
| Validation gain | +0.002469 |
| **Held-out test** | GAUC 0.664980 · nDCG@5 0.531398 · **Primary 0.598189** |
| Test coverage | 23,875 users · 170,588 rows |
| Model calls | 40 |
| Provider-reported tokens | 715,647 |
| Agent wall clock | 50.4 min |
| GPU hours | 0 (CPU only) |

## Manual interventions

**0** operator intervention(s) during this run.

Interventions are counted from the run's own event log: a provider or infrastructure failure pauses the run and records `run.failed`, and further orchestrator activity in the same log means an operator resumed it. Every intervention above is a resume of an unmodified run.

No manual edits were made to candidate code: every commit in the candidate workspace is authored by the agent identity (ML Loop <ml-loop@localhost>). Hypotheses, diffs, parent selection, and stopping were produced by the agent without human editing.

### Provider transport failures (1)

| Time (UTC) | Error | HTTP | Candidate | Attempt |
|---|---|---|---|---|
| 19:51:57 | `Timeout` | 408 | node_008 | 1 |

Transport failures are retried inside the client and do not count as experimental evidence. Only an exhausted retry budget pauses the run.

## Iteration index

| # | Candidate | GAUC | nDCG@5 | Primary | vs parent | Status | Repairs |
|---|---|---|---|---|---|---|---|
| baseline | `genesis` | 0.667133 | 0.535805 | 0.601469 | - | success | 0 |
| 1 | `node_001` | 0.661960 | 0.533151 | 0.597556 | -0.003913 | success | 0 |
| 2 | `node_002` | 0.669656 | 0.536847 | 0.603251 | +0.001783 | success | 0 |
| 3 | `node_003` | 0.667945 | 0.536272 | 0.602109 | -0.001143 | success | 0 |
| 4 | `node_004` | 0.669859 | 0.536526 | 0.603193 | -0.000059 | success | 0 |
| 5 | `node_005` | 0.668677 | 0.536468 | 0.602572 | -0.000679 | success | 0 |
| 6 | `node_006` | 0.670520 | 0.537355 | 0.603938 | +0.000686 | success | 0 |
| 7 | `node_007` | 0.670249 | 0.537152 | 0.603700 | -0.000237 | success | 0 |
| 8 | `node_008` | 0.670741 | 0.537103 | 0.603922 | -0.000016 | success | 0 |
| 9 | `node_009` | 0.670110 | 0.537152 | 0.603631 | -0.000307 | success | 0 |
| 10 | `node_010` | 0.666101 | 0.535328 | 0.600714 | -0.003223 | success | 0 |
| 11 | `node_011` | 0.670418 | 0.537019 | 0.603719 | -0.000219 | success | 0 |
| 12 | `node_012` | 0.668809 | 0.536468 | 0.602638 | +0.001170 | success | 0 |
| 13 | `node_013` | 0.668530 | 0.537157 | 0.602844 | +0.000205 | success | 0 |
| 14 | `node_014` | 0.668984 | 0.536283 | 0.602634 | -0.000210 | success | 0 |
| 15 | `node_015` | 0.669048 | 0.535877 | 0.602463 | -0.000171 | success | 0 |
| 16 | `node_016` | 0.668604 | 0.535723 | 0.602164 | -0.000299 | success | 0 |

---

## Baseline: `genesis`

**Status** `success` · **Parent** `none` · **Commit** `418e27427a97`

### Hypothesis

Supplied reference pipeline. No agent hypothesis; this is the baseline every candidate is measured against.

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667133 | 0.535805 | 0.601469 | - | 36 s |

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

**Status** `success` · **Parent** `genesis` · **Commit** `336e5b52e46d`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem, first branch from genesis): expand the FM input from the 5 base categorical fields to 9 leakage-free fields by adding exposure-count popularity buckets and explicit user-context crosses, plus finer duration binning. Hypothesis: GAUC/nDCG@5 are within-user ranking metrics, so only features that vary inside a user's candidate group can help; the current encoding gives the model only video_id/author_id/tab plus a coarse 10-bin duration bucket, and long_view is strongly duration-dependent, so (a) finer duration resolution, (b) item/author exposure popularity, and (c) dedicated parameters for user x duration-preference and user x tab interactions should sharpen within-user discrimination beyond what the shared k=16 embedding dot products capture. Closest supplied prior attempt: none from this parent (no siblings; genesis is the untouched reference FM), and the memory's feature-engineering result came from a materially more advanced other-run parent.

Edit features.py ONLY (config.py, model.py, train.py, requirements.txt stay exactly as supplied; train.train and model.load_predictor contracts, splits, target, and evaluation are unchanged). Implement:
1. Restructure raw(row, state) to take the fitted state dict and return 9 string field values, and make fit() a two-pass function: pass 1 computes duration quantile edges and exposure counts from training rows only; pass 2 builds per-field vocabularies by iterating raw() over the training rows.
2. Fields (in order): 0 user_id, 1 video_id, 2 author_id, 3 tab, 4 fine duration bucket = str(searchsorted(fine_edges, duration_ms)) with fine_edges = np.quantile(train durations, np.linspace(0,1,33)[1:-1]) (32 bins instead of 10), 5 video popularity bucket = str(min(int(log2(1 + train exposure count of video_id)), 12)), 6 author popularity bucket = str(min(int(log2(1 + train exposure count of author_id)), 12)), 7 cross user_id + '|' + tab, 8 cross user_id + '|' + coarse duration bucket, where coarse_edges = np.quantile(train durations, [0.25, 0.5, 0.75]).
3. Store in the returned state everything transform() needs at inference: fine_edges, coarse_edges, video_count and author_count dicts (unseen ids -> count 0 -> bucket 0), vocabs, offsets = cumsum of [0] + dims[:-1], and dim = sum(dims), keeping the existing '+1 OOV slot per field' convention (dims[i] = len(vocab_i) + 1) so unseen values map to len(vocab) + offset.
4. Apply a minimum-frequency threshold of 5 training occurrences when building the vocabularies for the two high-cardinality cross fields (7 and 8) so rare crosses fall into that field's OOV slot; keep threshold 1 for fields 0-6.
5. Make transform() allocate an (len(rows), 9) int32 array (derive the field count from len(state['vocabs']) rather than hardcoding 5) and otherwise keep its current unseen-value handling and row-order preservation.

No labels may be read in fit() or transform() (counts are exposure counts only). Expected cost is roughly 1.5-2x the 36 s baseline, far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.661960 | 0.533151 | 0.597556 | -0.003913 | 50 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 65 ++++++++++++++++++++++++++++++++++++++++++++++++++-----------
 1 file changed, 54 insertions(+), 11 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..b7bf324 100644
--- a/features.py
+++ b/features.py
@@ -24,28 +24,71 @@ while preserving the input-row contract and leakage constraints.
 
 # Reference implementation: replaceable while preserving the contracts above.
 import numpy as np
+from math import log2
 
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+def raw(row, state):
+    user_id, video_id, author_id, tab, duration_ms = row[1], row[2], row[3], row[4], row[5]
+    fine_edges = state['fine_edges']
+    coarse_edges = state['coarse_edges']
+    video_count = state['video_count']
+    author_count = state['author_count']
+    fine_bucket = str(int(np.searchsorted(fine_edges, duration_ms)))
+    coarse_bucket = str(int(np.searchsorted(coarse_edges, duration_ms)))
+    video_pop = str(min(int(log2(1 + video_count.get(video_id, 0))), 12))
+    author_pop = str(min(int(log2(1 + author_count.get(author_id, 0))), 12))
+    return [
+        user_id,
+        video_id,
+        author_id,
+        tab,
+        fine_bucket,
+        video_pop,
+        author_pop,
+        str(user_id) + '|' + str(tab),
+        str(user_id) + '|' + coarse_bucket,
+    ]
 
 
 def fit(rows):
-    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    durations = [r[5] for r in rows]
+    fine_edges = np.quantile(durations, np.linspace(0, 1, 33)[1:-1])
+    coarse_edges = np.quantile(durations, [0.25, 0.5, 0.75])
+
+    video_count = {}
+    author_count = {}
+    for row in rows:
+        video_count[row[2]] = video_count.get(row[2], 0) + 1
+        author_count[row[3]] = author_count.get(row[3], 0) + 1
+
+    state = dict(fine_edges=fine_edges, coarse_edges=coarse_edges,
+                 video_count=video_count, author_count=author_count)
+
+    counts = [{} for _ in range(9)]
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
-            if value not in vocabs[i]:
-                vocabs[i][value] = len(vocabs[i])
+        for i, value in enumerate(raw(row, state)):
+            counts[i][value] = counts[i].get(value, 0) + 1
+
+    vocabs = []
+    for i in range(9):
+        threshold = 5 if i in (7, 8) else 1
+        vocab = {}
+        for value, count in counts[i].items():
+            if count >= threshold:
+                vocab[value] = len(vocab)
+        vocabs.append(vocab)
+
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

## Iteration 2: `node_002`

**Status** `success` · **Parent** `genesis` · **Commit** `6c9e2125a558`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss-formulation subsystem — untouched from this parent; the only sibling from genesis, node_001, changed features.py encoding and lost -0.0039, so this branch leaves features.py exactly as supplied): replace the pointwise binary-cross-entropy objective of the reference FM with an in-user pairwise BPR ranking objective, so the model is optimized directly for the within-user ordering that GAUC and nDCG@5 measure instead of for calibrated per-row long_view probability. Hypothesis: GAUC/nDCG@5 only depend on the ranking of items inside each user's group; pointwise logloss spends capacity on global calibration and on between-user differences that the metrics ignore, so training on sampled (positive, negative) pairs drawn from the same user_id should improve the primary metric with the same 5-field encoding and k=16 embeddings. Closest supplied prior attempt: none from this parent for loss formulation (the sibling was feature engineering); memory reports pairwise/sampled-softmax losses only from an unrelated, materially more advanced other-run lineage.

Edit model.py, train.py, and config.py only (features.py and requirements.txt stay exactly as supplied; train.train and model.load_predictor signatures, checkpoint layout with version/config/features_state/model_state/training_state/context, atomic saving, splits, target, and evaluation via agent.sandbox.protocol.evaluate are unchanged).

1. model.py: keep FM.logits, FM.predict, Predictor, and read_checkpoint unchanged; add a new method FM.step_pair(self, Xp, Xn) that (a) computes zp, Ep, Sp = self.logits(Xp) and zn, En, Sn = self.logits(Xn), (b) sets d = zp - zn and s = sigmoid(-d), g = (s / B).astype(np.float32) with B = len(Xp), (c) accumulates gW with np.add.at(gW, Xp, -g[:, None]) and np.add.at(gW, Xn, g[:, None]), and gV with np.add.at(gV, Xp, -g[:, None, None] * (Sp[:, None, :] - Ep)) and np.add.at(gV, Xn, g[:, None, None] * (Sn[:, None, :] - En)), (d) adds the existing L2 terms gV += self.l2 * self.V; gW += self.l2 * self.W, (e) performs exactly the same Adam update (b1=0.9, b2=0.999, eps=1e-8, self.t += 1) over (V, gV, mV, vV) and (W, gW, mW, vW) as FM.step, leaving self.b untouched (the global bias cancels in the pairwise difference), and (f) returns float(np.mean(-np.log(sigmoid(d) + 1e-9))). Keep FM.step in place so the class interface and vars(model) key set used by the checkpoint resume logic are unchanged.

2. train.py: after Xtr/ytr/Xva are built, construct pairwise sampling structures from training rows only, using r[1] (user_id) for grouping and r[6] (long_view) for the pos/neg split: group training row indices by user_id, keep only users having at least one positive and at least one negative, build (i) pos_idx = int32 array of those users' positive row indices repeated config['pairs_per_pos'] times, (ii) neg_flat = int32 concatenation of those users' negative row indices with per-user start offsets and lengths, and (iii) per-pos-entry start/length arrays aligned with pos_idx. Each epoch, vectorize negative sampling as neg_idx = neg_flat[start + (rng.random(len(pos_idx)) * length).astype(np.int64)], shuffle the pairs with rng.permutation(len(pos_idx)), and iterate minibatches of config['bs'] pairs calling model.step_pair(Xtr[pos_batch], Xtr[neg_batch]); collect the returned BPR losses for the existing per-epoch print. If no user yields a valid pair, raise a clear ValueError instead of silently falling back. Everything else in the epoch loop is unchanged: validation via evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva)), best/bad/patience tracking on validation['primary'], nonfinite checks, training_state (epoch/best/bad/rng/latest) capture, and save_checkpoint each epoch. Keep ytr computed as today (it is still used to build the pos/neg groups).

3. config.py: add pairs_per_pos=2 to DEFAULTS and validate it in resolve() as an int >= 1 alongside k/epochs/bs/patience/seed; change DEFAULTS to epochs=60, bs=4096, patience=5, leaving k=16, lr=0.001, l2=1e-6, seed=0 unchanged.

Expected cost is roughly 3-4x the 36 s pointwise baseline (two forward/backward passes per pair batch, more epochs), i.e. well under candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669656 | 0.536847 | 0.603251 | +0.001783 | 32 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 21 +++++++++++++++++++++
 train.py  | 35 ++++++++++++++++++++++++++++++++---
 3 files changed, 55 insertions(+), 5 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 147c6ac..5d2be0e 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'pairs_per_pos'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 495d48e..f2c39f8 100644
--- a/model.py
+++ b/model.py
@@ -65,6 +65,27 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
+    def step_pair(self, Xp, Xn):
+        B = len(Xp)
+        zp, Ep, Sp = self.logits(Xp)
+        zn, En, Sn = self.logits(Xn)
+        d = zp - zn
+        s = sigmoid(-d)
+        g = (s / B).astype(np.float32)
+        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        np.add.at(gW, Xp, -g[:, None])
+        np.add.at(gW, Xn, g[:, None])
+        np.add.at(gV, Xp, -g[:, None, None] * (Sp[:, None, :] - Ep))
+        np.add.at(gV, Xn, g[:, None, None] * (Sn[:, None, :] - En))
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
index 0451b1a..8529995 100644
--- a/train.py
+++ b/train.py
@@ -122,12 +122,41 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     Xtr = transform(train_rows, features)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
+
+    groups = {}
+    for idx, r in enumerate(train_rows):
+        groups.setdefault(r[1], [[], []])[int(r[6])].append(idx)
+
+    pos_list, neg_flat_list, starts, lengths = [], [], [], []
+    offset = 0
+    for _uid, (negs, poss) in groups.items():
+        if not poss or not negs:
+            continue
+        neg_flat_list.extend(negs)
+        for p in poss:
+            for _ in range(config['pairs_per_pos']):
+                pos_list.append(p)
+                starts.append(offset)
+                lengths.append(len(negs))
+        offset += len(negs)
+
+    if not pos_list:
+        raise ValueError('no user has both positive and negative examples for pairwise training')
+
+    pos_idx = np.asarray(pos_list, dtype=np.int32)
+    neg_flat = np.asarray(neg_flat_list, dtype=np.int32)
+    starts = np.asarray(starts, dtype=np.int64)
+    lengths = np.asarray(lengths, dtype=np.int64)
+
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
-        order = rng.permutation(len(ytr))
-        losses = [model.step(Xtr[order[i:i + config['bs']]], ytr[order[i:i + config['bs']]])
-                  for i in range(0, len(order), config['bs'])]
+        neg_idx = neg_flat[starts + (rng.random(len(pos_idx)) * lengths).astype(np.int64)]
+        perm = rng.permutation(len(pos_idx))
+        pos_perm = pos_idx[perm]
+        neg_perm = neg_idx[perm]
+        losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
+                  for i in range(0, len(perm), config['bs'])]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

---

## Iteration 3: `node_003`

**Status** `success` · **Parent** `node_002` · **Commit** `fb50347346d3`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model-backbone subsystem — never touched anywhere in this lineage: genesis and node_002 both use the same plain FM; node_001 changed features and lost -0.0039, node_002 changed the loss to pairwise BPR and gained +0.0018): replace the shared-embedding factorization machine with a field-aware factorization machine (FFM) while keeping the existing in-user pairwise BPR training loop, the 5-field encoding from features.py, and every runner/inference contract unchanged. Hypothesis: with only F=5 fields (user_id, video_id, author_id, tab, duration-quantile bucket), a single embedding per feature forces the same latent vector to serve user↔video, user↔duration and author↔tab interactions; field-specific embeddings let personalization (user↔video/author) and content effects (duration↔tab/author) be modeled separately, which should sharpen the within-user ordering that GAUC/nDCG@5 measure. Closest supplied prior attempts are a feature-encoding change and a loss change; no backbone replacement has been supplied from any parent.

Implementation:
1. model.py: change FM to an FFM. Add a module constant NUM_FIELDS = 5 and give FM.__init__ an extra keyword `fields=NUM_FIELDS` (default used by Predictor and train.py, whose call sites stay unchanged). Allocate self.V = rng.normal(0, 0.01, (dim, fields, k)).astype(np.float32), keep self.W (dim,), self.b, self.lr, self.l2, Adam buffers mV/vV/mW/vW with the same shapes as V/W, and self.t = 0. Store self.F = fields. Rewrite logits(X) so E = self.V[X] has shape (B, F, F, k) with E[b, i, f] = the latent vector of the value in field i used against field f, and z = self.b + self.W[X].sum(1) + sum over all pairs i<j of (E[:, i, j, :] * E[:, j, i, :]).sum(-1); return (z, E) with z first so predict(X) (which uses logits(...)[0]) keeps working. Rewrite step_pair(Xp, Xn) for this parameterization: zp, Ep = logits(Xp); zn, En = logits(Xn); d = zp - zn; s = sigmoid(-d); g = (s / B).astype(np.float32); build gEp = zeros_like(Ep) and gEn = zeros_like(En) by looping over the 10 (i<j) field pairs with gEp[:, i, j, :] += (-g)[:, None] * Ep[:, j, i, :], gEp[:, j, i, :] += (-g)[:, None] * Ep[:, i, j, :] and the mirrored positive-sign updates for gEn; scatter with np.add.at(gV, Xp, gEp), np.add.at(gV, Xn, gEn) (gV has shape (dim, F, k), so gV[X] broadcasts to (B, F, F, k)), and keep the linear terms np.add.at(gW, Xp, -g[:, None]) and np.add.at(gW, Xn, g[:, None]); then gV += self.l2 * self.V; gW += self.l2 * self.W, self.t += 1, and apply exactly the same Adam update (b1=0.9, b2=0.999, eps=1e-8) over (V, gV, mV, vV) and (W, gW, mW, vW), leaving self.b untouched; return float(np.mean(-np.log(sigmoid(d) + 1e-9))) as today. Delete the now-inconsistent pointwise FM.step (train.py only calls step_pair). Lower the predict batch size from 200_000 to 20_000 so the (B, F, F, k) tensor stays small. Leave read_checkpoint, Predictor (it restores V/W/b and shape-checks against the freshly constructed model, which now yields (dim, F, k) for V) and load_predictor unchanged.
2. config.py: change DEFAULTS k from 16 to 8 (FFM stores F=5 vectors per feature, so k=8 keeps parameters and compute in a comparable range) and leave lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2 and the existing validation logic unchanged.
3. train.py: no functional change required — the FM(features['dim'], k=..., lr=..., l2=..., seed=...) construction, pairwise sampling structures, per-epoch step_pair loop, evaluate(...) selection on validation['primary'], nonfinite checks, training_state capture and atomic save_checkpoint all stay as supplied; only adjust if needed for the new constructor default.
Keep features.py and requirements.txt exactly as supplied. Expected cost is roughly 3-6x the current 32 s pairwise run (a few hundred seconds at most), well inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.667945 | 0.536272 | 0.602109 | -0.001143 | 62 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  2 +-
 model.py  | 53 +++++++++++++++++++++++++----------------------------
 2 files changed, 26 insertions(+), 29 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 5d2be0e..90685c1 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2)
+DEFAULTS = dict(k=8, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2)
 
 
 def resolve(overrides):
diff --git a/model.py b/model.py
index f2c39f8..33e98c8 100644
--- a/model.py
+++ b/model.py
@@ -31,10 +31,13 @@ from features import transform
 
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
+NUM_FIELDS = 5
+
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, fields=NUM_FIELDS):
         rng = np.random.default_rng(seed)
-        self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
+        self.F = fields
+        self.V = rng.normal(0, 0.01, (dim, fields, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
         self.b = np.float32(0.0)
         self.lr, self.l2 = lr, l2
@@ -43,40 +46,34 @@ class FM:
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
+        E = self.V[X]                                   # (B,F,F,k): E[b,i,f]
+        z = self.b + self.W[X].sum(1)
+        F = self.F
+        for i in range(F):
+            for j in range(i + 1, F):
+                z = z + (E[:, i, j, :] * E[:, j, i, :]).sum(-1)
+        return z, E
 
     def step_pair(self, Xp, Xn):
         B = len(Xp)
-        zp, Ep, Sp = self.logits(Xp)
-        zn, En, Sn = self.logits(Xn)
+        zp, Ep = self.logits(Xp)
+        zn, En = self.logits(Xn)
         d = zp - zn
         s = sigmoid(-d)
         g = (s / B).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        gEp = np.zeros_like(Ep); gEn = np.zeros_like(En)
+        F = self.F
+        for i in range(F):
+            for j in range(i + 1, F):
+                gEp[:, i, j, :] += (-g)[:, None] * Ep[:, j, i, :]
+                gEp[:, j, i, :] += (-g)[:, None] * Ep[:, i, j, :]
+                gEn[:, i, j, :] += g[:, None] * En[:, j, i, :]
+                gEn[:, j, i, :] += g[:, None] * En[:, i, j, :]
+        np.add.at(gV, Xp, gEp)
+        np.add.at(gV, Xn, gEn)
         np.add.at(gW, Xp, -g[:, None])
         np.add.at(gW, Xn, g[:, None])
-        np.add.at(gV, Xp, -g[:, None, None] * (Sp[:, None, :] - Ep))
-        np.add.at(gV, Xn, g[:, None, None] * (Sn[:, None, :] - En))
         gV += self.l2 * self.V; gW += self.l2 * self.W
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
@@ -86,7 +83,7 @@ class FM:
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         return float(np.mean(-np.log(sigmoid(d) + 1e-9)))
 
-    def predict(self, X, bs=200_000):
+    def predict(self, X, bs=20_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
 def read_checkpoint(path):
```

---

## Iteration 4: `node_004`

**Status** `success` · **Parent** `node_002` · **Commit** `66fa639c382c`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss-formulation subsystem, extending the change that already paid off on this branch): replace the 1-negative pairwise BPR objective of the parent with an in-user sampled-softmax (listwise) objective over 1 positive and M=8 uniformly sampled negatives from the same user_id, keeping the plain shared-embedding FM backbone, the 5-field encoding in features.py, and all runner/inference contracts unchanged. Hypothesis: BPR only pushes a positive above one sampled negative per update, which gives a noisy estimate of the within-user ordering; normalizing over 8 same-user negatives per positive concentrates gradient on the negatives currently scored highest (a softer top-of-list objective), which should sharpen the head of each user's ranking and therefore nDCG@5 as well as GAUC, at ~4x the parent's per-epoch cost (parent ran 32 s, so ~150 s, far inside candidate_timeout_s). Distinction from the closest supplied prior attempts: node_002 (this parent's incoming edge) changed pointwise BCE -> pairwise BPR with exactly one negative; the sibling node_003 replaced the backbone with FFM and lost -0.0011; the other-run memory entry only added a temperature on top of an already-existing sampled softmax. No multi-negative softmax loss has been tried from this parent.

Implementation:
1. model.py: keep FM.logits, FM.step, FM.step_pair, predict, read_checkpoint, Predictor and load_predictor exactly as supplied (so vars(model) keys and checkpoint resume logic are unchanged), and add a new method FM.step_group(self, Xp, Xn) where Xp has shape (B, F) and Xn has shape (B, M, F). It must: (a) build Xall = np.concatenate([Xp[:, None, :], Xn], axis=1) of shape (B, M+1, F) and Xflat = Xall.reshape(-1, F); (b) compute z, E, S = self.logits(Xflat) and reshape z to (B, M+1); (c) compute a numerically stable softmax P = exp(z - z.max(axis=1, keepdims=True)) normalized along axis 1; (d) form G = P.copy(); G[:, 0] -= 1.0; G /= B; g = G.reshape(-1).astype(np.float32); (e) accumulate gV = zeros_like(self.V), gW = zeros_like(self.W) with np.add.at(gW, Xflat, g[:, None]) and np.add.at(gV, Xflat, g[:, None, None] * (S[:, None, :] - E)); (f) add gV += self.l2 * self.V; gW += self.l2 * self.W; (g) do self.t += 1 and apply exactly the same Adam update (b1=0.9, b2=0.999, eps=1e-8) over (V, gV, mV, vV) and (W, gW, mW, vW) as FM.step, leaving self.b untouched because the global bias cancels inside the per-user softmax; (h) return float(np.mean(-np.log(P[:, 0] + 1e-9))).
2. train.py: keep the existing group-building code (grouping training row indices by r[1] with the r[6] pos/neg split, pos_idx repeated config['pairs_per_pos'] times, neg_flat with per-entry starts/lengths, and the ValueError when no user has both classes). Change only the sampling and the inner loop: each epoch draw a negative matrix neg_idx = neg_flat[starts[:, None] + (rng.random((len(pos_idx), config['negs'])) * lengths[:, None]).astype(np.int64)] of shape (len(pos_idx), negs) (sampling with replacement so users with fewer than negs negatives still work), permute rows with perm = rng.permutation(len(pos_idx)), and for each minibatch of config['bs'] positives call model.step_group(Xtr[pos_perm[i:i+bs]], Xtr[neg_perm[i:i+bs]]) where Xtr[neg_perm_batch] yields the (b, negs, 5) index tensor; collect the returned losses for the existing per-epoch print. Everything else (validation via evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva)), best/bad/patience tracking on validation['primary'], nonfinite checks, training_state capture with rng state and latest=vars(model), atomic save_checkpoint each epoch) stays exactly as supplied.
3. config.py: add negs=8 to DEFAULTS and validate it in resolve() as an int >= 1 in the same integer-key loop; keep k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0 and pairs_per_pos=2 unchanged.
Leave features.py and requirements.txt exactly as supplied.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669859 | 0.536526 | 0.603193 | -0.000059 | 72 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 26 ++++++++++++++++++++++++++
 train.py  |  4 ++--
 3 files changed, 30 insertions(+), 4 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 5d2be0e..fc08616 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, negs=8)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'pairs_per_pos'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'pairs_per_pos', 'negs'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index f2c39f8..8750baa 100644
--- a/model.py
+++ b/model.py
@@ -86,6 +86,32 @@ class FM:
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         return float(np.mean(-np.log(sigmoid(d) + 1e-9)))
 
+    def step_group(self, Xp, Xn):
+        B, F = Xp.shape
+        M = Xn.shape[1]
+        Xall = np.concatenate([Xp[:, None, :], Xn], axis=1)  # (B, M+1, F)
+        Xflat = Xall.reshape(-1, F)
+        z, E, S = self.logits(Xflat)
+        z = z.reshape(B, M + 1)
+        z = z - z.max(axis=1, keepdims=True)
+        P = np.exp(z)
+        P /= P.sum(axis=1, keepdims=True)
+        G = P.copy()
+        G[:, 0] -= 1.0
+        G /= B
+        g = G.reshape(-1).astype(np.float32)
+        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
+        np.add.at(gW, Xflat, g[:, None])
+        np.add.at(gV, Xflat, g[:, None, None] * (S[:, None, :] - E))
+        gV += self.l2 * self.V; gW += self.l2 * self.W
+        self.t += 1
+        b1, b2, eps = 0.9, 0.999, 1e-8
+        for P_, G_, M_, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
+            M_ *= b1; M_ += (1 - b1) * G_
+            Vv *= b2; Vv += (1 - b2) * (G_ * G_)
+            P_ -= self.lr * (M_ / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        return float(np.mean(-np.log(P[:, 0] + 1e-9)))
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index 8529995..7cbbc65 100644
--- a/train.py
+++ b/train.py
@@ -151,11 +151,11 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
-        neg_idx = neg_flat[starts + (rng.random(len(pos_idx)) * lengths).astype(np.int64)]
+        neg_idx = neg_flat[starts[:, None] + (rng.random((len(pos_idx), config['negs'])) * lengths[:, None]).astype(np.int64)]
         perm = rng.permutation(len(pos_idx))
         pos_perm = pos_idx[perm]
         neg_perm = neg_idx[perm]
-        losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
+        losses = [model.step_group(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
                   for i in range(0, len(perm), config['bs'])]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
```

---

## Iteration 5: `node_005`

**Status** `success` · **Parent** `node_002` · **Commit** `5c1e73148e1a`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem — untouched from this parent; the only supplied siblings from node_002 changed the backbone (FFM, -0.0011) and the loss (sampled softmax, -0.0001), and the single prior feature attempt, node_001, was made from the pointwise-BCE genesis parent with a different, unspecified encoding change): keep the parent's pairwise BPR FM training loop and all hyperparameters exactly as supplied, and instead enrich features.py from the current 5-field encoding to a 9-field, leakage-free encoding that adds exposure-frequency (popularity) buckets, finer duration resolution, and one categorical cross. Hypothesis: GAUC/nDCG@5 depend only on within-user ordering, which is driven by item-side signal; with raw video_id/author_id ids many items appear too rarely for their embeddings to train, so generalizable popularity buckets plus higher-resolution duration (long_view depends strongly on video length) and a tab×duration cross should sharpen within-user ranking without changing the objective.

Edit features.py only (config.py, model.py, train.py and requirements.txt stay exactly as supplied; FM.logits/step_pair/predict already handle an arbitrary number of fields F, and transform is the only place field count is hard-coded).

1. fit(rows) must, using training rows only and no label/target information whatsoever (row index 6 must never be read in features.py): (a) compute edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 21)[1:-1]) so duration is bucketed into 20 quantile bins instead of 10; (b) build plain occurrence-count dictionaries from the training rows: video_counts over r[2], author_counts over r[3], user_counts over r[1] (pure exposure counts, no outcomes); (c) store edges, video_counts, author_counts, user_counts in the returned state dict, then build vocabs by iterating rows through raw(row, state), and return the same state keys as today plus the new ones: dict(edges=..., video_counts=..., author_counts=..., user_counts=..., vocabs=..., offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims)).

2. Change raw(row, state) (signature changes from raw(row, edges) to raw(row, state); update its call sites in fit and transform accordingly) to return a list of 9 string tokens in this order: [0] str(row[1]) user_id; [1] str(row[2]) video_id; [2] str(row[3]) author_id; [3] str(row[4]) tab; [4] duration bucket 'd' + str(int(np.searchsorted(state['edges'], row[5]))); [5] video popularity bucket 'vc' + str(min(int(np.log2(1.0 + state['video_counts'].get(row[2], 0))), 20)); [6] author popularity bucket 'ac' + str(min(int(np.log2(1.0 + state['author_counts'].get(row[3], 0))), 20)); [7] user activity bucket 'uc' + str(min(int(np.log2(1.0 + state['user_counts'].get(row[1], 0))), 20)); [8] cross 'x' + str(row[4]) + '|' + duration-bucket token from [4]. Unseen users/videos/authors at inference get count 0 (bucket 0) and unseen vocabulary values keep the existing OOV handling (vocab.get(value, len(vocab)) + offset).

3. transform(rows, state) must allocate np.empty((len(rows), len(state['vocabs'])), dtype=np.int32) instead of a hard-coded width 5 and otherwise keep its current per-field vocab lookup and offset logic, preserving input row order.

Everything else is unchanged: config DEFAULTS stay k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2; the in-user pairwise BPR sampling/step_pair loop, evaluation via agent.sandbox.protocol.evaluate, best/patience selection, checkpoint layout (version/config/features_state/model_state/training_state/context) and atomic saving are untouched, and load_predictor keeps working because Predictor rebuilds FM from features_state['dim'] and calls the updated transform. Expected cost is roughly 1.8-2.5x the parent's 32 s run (F goes 5 -> 9), i.e. well inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668677 | 0.536468 | 0.602572 | -0.000679 | 41 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 35 +++++++++++++++++++++++++++--------
 1 file changed, 27 insertions(+), 8 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..aa3ce10 100644
--- a/features.py
+++ b/features.py
@@ -26,26 +26,45 @@ while preserving the input-row contract and leakage constraints.
 import numpy as np
 
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+def raw(row, state):
+    duration_bucket = 'd' + str(int(np.searchsorted(state['edges'], row[5])))
+    return [
+        str(row[1]),
+        str(row[2]),
+        str(row[3]),
+        str(row[4]),
+        duration_bucket,
+        'vc' + str(min(int(np.log2(1.0 + state['video_counts'].get(row[2], 0))), 20)),
+        'ac' + str(min(int(np.log2(1.0 + state['author_counts'].get(row[3], 0))), 20)),
+        'uc' + str(min(int(np.log2(1.0 + state['user_counts'].get(row[1], 0))), 20)),
+        'x' + str(row[4]) + '|' + duration_bucket,
+    ]
 
 
 def fit(rows):
-    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 21)[1:-1])
+    video_counts, author_counts, user_counts = {}, {}, {}
+    for r in rows:
+        video_counts[r[2]] = video_counts.get(r[2], 0) + 1
+        author_counts[r[3]] = author_counts.get(r[3], 0) + 1
+        user_counts[r[1]] = user_counts.get(r[1], 0) + 1
+    state = dict(edges=edges, video_counts=video_counts,
+                 author_counts=author_counts, user_counts=user_counts)
+    vocabs = [{} for _ in range(9)]
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
+        for i, value in enumerate(raw(row, state)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
-    return dict(edges=edges, vocabs=vocabs,
+    return dict(edges=edges, video_counts=video_counts, author_counts=author_counts,
+                user_counts=user_counts, vocabs=vocabs,
                 offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
 
 
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

## Iteration 6: `node_006`

**Status** `success` · **Parent** `node_002` · **Commit** `cd7c4b7a30fb`

### Hypothesis

```text
SELECTED CHANGE
Experiment (training-procedure / optimization subsystem — the only lever untouched from this parent: from node_002 the siblings already tried a backbone swap (FFM, -0.0011), a multi-negative sampled-softmax loss (-0.0001), and a richer 9-field feature encoding (-0.0007), all of which lost; global memory reports weight EMA as part of a successful path in a different, more advanced run, so this is a transfer of that idea onto this simpler pairwise-BPR FM baseline where no averaging of any kind exists yet): add an exponential moving average (EMA) of the FM parameters over optimizer steps, evaluate and select/serialize the EMA weights instead of the raw ones, keeping the in-user pairwise BPR loss, the supplied 5-field encoding in features.py, and all runner/inference contracts unchanged. Hypothesis: one-negative BPR updates on sparse id embeddings are very noisy, so the raw end-of-epoch weights fluctuate around a better average; smoothing the trajectory should reduce variance in the within-user score ordering and lift GAUC/nDCG@5 at near-zero extra compute.

Implementation (edit model.py, train.py and config.py only; features.py and requirements.txt stay exactly as supplied):

1. config.py: add ema_decay=0.999 to DEFAULTS and validate it in resolve() as a finite float with 0 < ema_decay < 1 (extend the existing float validation loop or add an explicit check). Leave k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2 unchanged.

2. model.py: give FM.__init__ a new keyword ema_decay=0.999, store self.ema_decay = float(ema_decay), and allocate zero-initialized EMA buffers self.eV = np.zeros_like(self.V), self.eW = np.zeros_like(self.W), self.eb = np.float32(0.0). At the end of FM.step_pair (after the existing Adam updates of V and W and after self.t has been incremented), update the buffers in place: self.eV *= d; self.eV += (1 - d) * self.V; self.eW *= d; self.eW += (1 - d) * self.W; self.eb = np.float32(d * self.eb + (1 - d) * self.b), with d = self.ema_decay; keep the returned BPR loss unchanged. Add FM.ema_params(self) returning bias-corrected copies (self.eV / c, self.eW / c, np.float32(self.eb / c)) with c = 1 - self.ema_decay ** self.t (fall back to the raw V, W, b when self.t == 0). Add FM.predict_ema(self, X, bs=200_000) that computes exactly the same FM score as logits() but using those bias-corrected EMA arrays (b + W[X].sum(1) + 0.5*((E.sum(1)**2).sum(1) - (E**2).sum((1,2))) with E = Vema[X]), batched like predict. Leave FM.logits, FM.step, FM.predict, read_checkpoint, Predictor and load_predictor unchanged (Predictor still rebuilds FM from features_state['dim'] and restores V/W/b, whose shapes are unchanged).

3. train.py: construct the model with ema_decay=config['ema_decay'] at both construction sites (fresh and resume paths), so the resume check set(state['latest']) == set(vars(model)) still matches now that vars(model) additionally contains eV, eW, eb and ema_decay. In the epoch loop, compute validation with the EMA scores: validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict_ema(Xva)); keep the identical best/bad/patience logic on validation['primary'], but when a new best is found set payload['model_state'] from the EMA parameters, i.e. Vema, Wema, bema = model.ema_params() saved as dict(V=copy.deepcopy(Vema), W=copy.deepcopy(Wema), b=bema), so inference through load_predictor uses exactly the weights that were validated. Extend the per-epoch nonfinite guard to also check eV, eW, eb, keep training_state = dict(epoch, best, bad, rng, latest=copy.deepcopy(vars(model))) and the atomic save_checkpoint each epoch as supplied, and additionally print the raw-weight validation primary (evaluate on model.predict(Xva)) alongside the EMA primary purely as a diagnostic that is never used for selection.

Expected cost is roughly 1.3-1.6x the parent's 32 s run (two extra array multiply-adds per step plus one extra validation pass per epoch), far inside candidate_timeout_s. Distinguishing note: no prior experiment from this parent or its ancestors changed the optimization trajectory or the weights used for validation/serialization — all supplied siblings changed features, backbone, or the loss function itself.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670520 | 0.537355 | 0.603938 | +0.000686 | 58 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 model.py  | 27 ++++++++++++++++++++++++++-
 train.py  | 13 ++++++++-----
 3 files changed, 37 insertions(+), 7 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 5d2be0e..cd7fb6f 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999)
 
 
 def resolve(overrides):
@@ -36,4 +36,6 @@ def resolve(overrides):
     for key in ('lr', 'l2'):
         if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
             raise ValueError(f'invalid {key}')
+    if not math.isfinite(config['ema_decay']) or not 0 < config['ema_decay'] < 1:
+        raise ValueError('invalid ema_decay')
     return config
diff --git a/model.py b/model.py
index f2c39f8..e88f150 100644
--- a/model.py
+++ b/model.py
@@ -32,7 +32,7 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, ema_decay=0.999):
         rng = np.random.default_rng(seed)
         self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
@@ -41,6 +41,10 @@ class FM:
         self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
         self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
         self.t = 0
+        self.ema_decay = float(ema_decay)
+        self.eV = np.zeros_like(self.V)
+        self.eW = np.zeros_like(self.W)
+        self.eb = np.float32(0.0)
 
     def logits(self, X):
         E = self.V[X]                                   # (B,F,k)
@@ -84,11 +88,32 @@ class FM:
             M *= b1; M += (1 - b1) * G
             Vv *= b2; Vv += (1 - b2) * (G * G)
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        decay = self.ema_decay
+        self.eV *= decay; self.eV += (1 - decay) * self.V
+        self.eW *= decay; self.eW += (1 - decay) * self.W
+        self.eb = np.float32(decay * self.eb + (1 - decay) * self.b)
         return float(np.mean(-np.log(sigmoid(d) + 1e-9)))
 
+    def ema_params(self):
+        if self.t == 0:
+            return self.V, self.W, self.b
+        c = 1 - self.ema_decay ** self.t
+        return self.eV / c, self.eW / c, np.float32(self.eb / c)
+
     def predict(self, X, bs=200_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
+    def predict_ema(self, X, bs=200_000):
+        Vema, Wema, bema = self.ema_params()
+        out = []
+        for i in range(0, len(X), bs):
+            Xb = X[i:i + bs]
+            E = Vema[Xb]
+            S = E.sum(1)
+            inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
+            out.append(bema + Wema[Xb].sum(1) + inter)
+        return np.concatenate(out)
+
 def read_checkpoint(path):
     with open(path, 'rb') as stream:
         state = pickle.load(stream)
diff --git a/train.py b/train.py
index 8529995..8d1505b 100644
--- a/train.py
+++ b/train.py
@@ -98,7 +98,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], ema_decay=config['ema_decay'])
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +115,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], ema_decay=config['ema_decay'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -157,14 +157,17 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         neg_perm = neg_idx[perm]
         losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
                   for i in range(0, len(perm), config['bs'])]
-        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
+        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict_ema(Xva))
+        raw_validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
+        print(f'epoch={epoch} raw_primary={raw_validation["primary"]:.6f} (diagnostic only)', flush=True)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            payload['model_state'] = {key: copy.deepcopy(getattr(model, key)) for key in ('V', 'W', 'b')}
+            Vema, Wema, bema = model.ema_params()
+            payload['model_state'] = dict(V=copy.deepcopy(Vema), W=copy.deepcopy(Wema), b=bema)
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW')):
+        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'eV', 'eW', 'eb')):
             raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
             rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
```

---

## Iteration 7: `node_007`

**Status** `success` · **Parent** `node_006` · **Commit** `7807fa6f514a`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model-averaging / inference subsystem, untouched in this lineage): turn the single pairwise-BPR + EMA FM into a seed-bagged score-space ensemble of N=3 FMs whose standardized scores are averaged for validation, checkpoint selection, and inference. Hypothesis: one-negative BPR updates on sparse id embeddings leave a lot of seed/sampling variance in the within-user score ordering; the parent's EMA already showed that reducing this variance lifts the metric (+0.0007), and averaging several independently initialized and independently negative-sampled models attacks the same variance along a different axis (independent errors cancel), so GAUC and nDCG@5 should both rise at ~3x the parent's 58 s runtime. Distinguishing note: no ensembling of any kind exists in the supplied parent or its lineage — siblings from node_002 changed the backbone (FFM), the loss (sampled softmax) and the feature encoding, and node_006 added EMA over a single model; global memory reports score-space ensembling only in a different, more advanced other-run lineage, so this is a transfer onto a materially simpler single-model baseline.

Edit config.py, model.py and train.py only (features.py and requirements.txt stay exactly as supplied; train.train and model.load_predictor signatures, the version/config/features_state/model_state/training_state/context checkpoint layout, atomic saving, splits, target, ranking groups and evaluation via agent.sandbox.protocol.evaluate are unchanged).

1. config.py: add n_models=3 to DEFAULTS and validate it by adding 'n_models' to the existing integer key tuple in resolve() (int >= 1). All other defaults unchanged (k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999).

2. model.py: leave sigmoid, FM (logits/step/step_pair/ema_params/predict/predict_ema), read_checkpoint and load_predictor exactly as they are. Change only Predictor to consume an ensemble model_state of the form dict(members=[dict(V=..., W=..., b=..., mu=float, sd=float), ...]): build one FM per member with features_state['dim'] and config k/lr/l2/seed, keep the existing per-array shape and np.isfinite validation for V/W/b (raise ValueError on mismatch, and raise if 'members' is missing or empty), store each member's mu/sd as floats, and in predict(rows) transform the rows once and return the mean over members of (member.predict(X) - mu) / max(sd, 1e-6) as a finite float array in input order; keep the empty-rows early return.

3. train.py: replace the single model with models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i, ema_decay=config['ema_decay']) for i in range(config['n_models'])] at both the fresh and the resume construction sites. On resume, training_state['latest'] is a list: require it to be a list of length config['n_models'] whose i-th element has set(...) == set(vars(models[i])) and restore every entry with the existing shape/finiteness checks; keep the existing epoch/bad/best/lr/l2 progress validation but apply the model.t check to models[0]. Keep the single shared rng and the existing pos_idx/neg_flat/starts/lengths pair structures built once from train_rows (user grouping on r[1], pos/neg split on r[6], pairs_per_pos repeats). Before the epoch loop, draw once with a dedicated Generator np.random.default_rng(config['seed']) a fixed calibration subsample Xsub of up to 200_000 training rows from Xtr (inputs only, no labels). In each epoch, for every model i in order: draw its own neg_idx = neg_flat[starts + (rng.random(len(pos_idx)) * lengths).astype(np.int64)] and its own perm = rng.permutation(len(pos_idx)) from the shared rng (so members see different negatives and different orders), then run the same minibatch loop of models[i].step_pair(Xtr[pos_perm[j:j+bs]], Xtr[neg_perm[j:j+bs]]) collecting losses. After all members have stepped, compute for each member s_sub = models[i].predict_ema(Xsub), mu_i = float(s_sub.mean()), sd_i = float(s_sub.std()) or 1.0 if not finite/zero, and s_va = (models[i].predict_ema(Xva) - mu_i) / max(sd_i, 1e-6); average the member s_va arrays and call evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], ensemble_scores) exactly once per epoch. Keep the best/bad/patience logic on validation['primary'] with the same 1e-5 margin; on a new best set payload['model_state'] = dict(members=[dict(V=copy.deepcopy(Vema_i), W=copy.deepcopy(Wema_i), b=bema_i, mu=mu_i, sd=sd_i) for each member]) using models[i].ema_params(), and payload['best_epoch'] = epoch. Extend the nonfinite guard to every member's ('V','W','b','mV','vV','mW','vW','eV','eW','eb'); set training_state = dict(epoch=epoch, best=best, bad=bad, rng=rng.bit_generator.state, latest=[copy.deepcopy(vars(m)) for m in models]) and keep the atomic save_checkpoint every epoch. Drop the raw-weight diagnostic evaluate() call (diagnostic only) to control runtime, printing per epoch the mean BPR loss over all members and the ensemble primary.

Expected cost roughly 3x the parent's 57.7 s (about 150-200 s), far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670249 | 0.537152 | 0.603700 | -0.000237 | 118 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 29 +++++++++++++++++++-------
 train.py  | 71 +++++++++++++++++++++++++++++++++++++++++++--------------------
 3 files changed, 73 insertions(+), 31 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index cd7fb6f..3f92d6e 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999, n_models=3)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'pairs_per_pos'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'pairs_per_pos', 'n_models'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index e88f150..db2c0b5 100644
--- a/model.py
+++ b/model.py
@@ -131,13 +131,23 @@ class Predictor:
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
+        members = weights.get('members')
+        if not members:
+            raise ValueError('missing or empty model_state members')
+        self.models = []
+        self.mus = []
+        self.sds = []
+        for i, member in enumerate(members):
+            model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i)
+            for name in ('V', 'W', 'b'):
+                value = member[name]
+                if np.shape(value) != np.shape(getattr(model, name)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite model weights: ' + name)
+                setattr(model, name, value)
+            self.models.append(model)
+            self.mus.append(float(member['mu']))
+            self.sds.append(float(member['sd']))
 
     def predict(self, rows):
         """Return one finite real-valued score per row, preserving input order.
@@ -148,7 +158,12 @@ class Predictor:
         """
         if not len(rows):
             return np.empty(0, dtype=np.float32)
-        return self.model.predict(transform(rows, self.features))
+        X = transform(rows, self.features)
+        scores = np.zeros(len(rows), dtype=np.float64)
+        for model, mu, sd in zip(self.models, self.mus, self.sds):
+            scores += (model.predict(X) - mu) / max(sd, 1e-6)
+        scores /= len(self.models)
+        return scores.astype(np.float32)
 
 
 def load_predictor(checkpoint_path):
diff --git a/train.py b/train.py
index 8d1505b..c71859a 100644
--- a/train.py
+++ b/train.py
@@ -98,13 +98,18 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], ema_decay=config['ema_decay'])
-        if set(state['latest']) != set(vars(model)):
+        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i, ema_decay=config['ema_decay']) for i in range(config['n_models'])]
+        latest = state['latest']
+        if not isinstance(latest, list) or len(latest) != config['n_models']:
             raise ValueError('incomplete optimizer/model state')
-        for key, value in state['latest'].items():
-            if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
-                raise ValueError('incompatible or nonfinite latest state: ' + key)
-            setattr(model, key, value)
+        for model, entry in zip(models, latest):
+            if set(entry) != set(vars(model)):
+                raise ValueError('incomplete optimizer/model state')
+            for key, value in entry.items():
+                if np.shape(value) != np.shape(getattr(model, key)) or not np.isfinite(value).all():
+                    raise ValueError('incompatible or nonfinite latest state: ' + key)
+                setattr(model, key, value)
+        model = models[0]
         best, bad, epoch = state['best'], state['bad'], state['epoch']
         if (type(epoch) is not int or not 1 <= epoch <= config['epochs']
                 or type(bad) is not int or not 0 <= bad <= config['patience']
@@ -115,7 +120,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], ema_decay=config['ema_decay'])
+        models = [FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'] + i, ema_decay=config['ema_decay']) for i in range(config['n_models'])]
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
@@ -148,29 +153,51 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     starts = np.asarray(starts, dtype=np.int64)
     lengths = np.asarray(lengths, dtype=np.int64)
 
+    calib_rng = np.random.default_rng(config['seed'])
+    n_sub = min(200_000, len(Xtr))
+    sub_idx = calib_rng.choice(len(Xtr), size=n_sub, replace=False)
+    Xsub = Xtr[sub_idx]
+
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
             break
-        neg_idx = neg_flat[starts + (rng.random(len(pos_idx)) * lengths).astype(np.int64)]
-        perm = rng.permutation(len(pos_idx))
-        pos_perm = pos_idx[perm]
-        neg_perm = neg_idx[perm]
-        losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
-                  for i in range(0, len(perm), config['bs'])]
-        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict_ema(Xva))
-        raw_validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
-        print(f'epoch={epoch} raw_primary={raw_validation["primary"]:.6f} (diagnostic only)', flush=True)
+        all_losses = []
+        for model in models:
+            neg_idx = neg_flat[starts + (rng.random(len(pos_idx)) * lengths).astype(np.int64)]
+            perm = rng.permutation(len(pos_idx))
+            pos_perm = pos_idx[perm]
+            neg_perm = neg_idx[perm]
+            losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
+                      for i in range(0, len(perm), config['bs'])]
+            all_losses.extend(losses)
+
+        mus, sds, s_vas = [], [], []
+        for model in models:
+            s_sub = model.predict_ema(Xsub)
+            mu = float(s_sub.mean())
+            sd = float(s_sub.std())
+            if not np.isfinite(sd) or sd == 0:
+                sd = 1.0
+            mus.append(mu)
+            sds.append(sd)
+            s_vas.append((model.predict_ema(Xva) - mu) / max(sd, 1e-6))
+        ensemble_scores = np.mean(s_vas, axis=0)
+        validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], ensemble_scores)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
-            Vema, Wema, bema = model.ema_params()
-            payload['model_state'] = dict(V=copy.deepcopy(Vema), W=copy.deepcopy(Wema), b=bema)
+            members = []
+            for model, mu, sd in zip(models, mus, sds):
+                Vema, Wema, bema = model.ema_params()
+                members.append(dict(V=copy.deepcopy(Vema), W=copy.deepcopy(Wema), b=bema, mu=mu, sd=sd))
+            payload['model_state'] = dict(members=members)
             payload['best_epoch'] = epoch
         else:
             bad += 1
-        if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'eV', 'eW', 'eb')):
-            raise ValueError('nonfinite training state; keeping last valid checkpoint')
+        for model in models:
+            if not all(np.isfinite(getattr(model, key)).all() for key in ('V', 'W', 'b', 'mV', 'vV', 'mW', 'vW', 'eV', 'eW', 'eb')):
+                raise ValueError('nonfinite training state; keeping last valid checkpoint')
         payload['training_state'] = dict(epoch=epoch, best=best, bad=bad,
-            rng=rng.bit_generator.state, latest=copy.deepcopy(vars(model)))
+            rng=rng.bit_generator.state, latest=[copy.deepcopy(vars(m)) for m in models])
         payload['validation'] = validation
         save_checkpoint(checkpoint_path, payload)
-        print(f'epoch={epoch} loss={np.mean(losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
+        print(f'epoch={epoch} loss={np.mean(all_losses):.6f} primary={validation["primary"]:.6f} checkpoint saved', flush=True)
```

---

## Iteration 8: `node_008`

**Status** `success` · **Parent** `node_006` · **Commit** `e015ebf6185e`

### Hypothesis

```text
SELECTED CHANGE
Experiment (FM backbone hyperparameters — the one lever never touched anywhere in this lineage): double the factorization capacity of the pairwise-BPR + EMA FM by raising the embedding dimension from k=16 to k=32, keeping the loss, sampling, EMA, feature encoding and all other settings exactly as in the parent. Hypothesis: k=16, lr=0.001 and l2=1e-6 were inherited unchanged from the original pointwise-BCE reference and have never been re-tuned for the current in-user pairwise BPR objective with EMA weight averaging; the dominant signal for within-user ranking is the user_id x video_id / user_id x author_id embedding interaction, which is effectively a rank-16 matrix factorization and is likely capacity-limited. Doubling k should let the model resolve finer within-user item ordering, and the existing early stopping on validation primary plus the EMA smoothing (which already proved to reduce trajectory noise, +0.0007) should protect against the extra overfitting risk.

Implementation:
1. config.py: change DEFAULTS to k=32 (leave lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999 and the entire resolve() validation logic unchanged).
2. train.py (supporting cost-control edit for this same experiment, no behavioral change to selection): delete the per-epoch diagnostic raw-weight evaluation, i.e. remove the `raw_validation = evaluate(...)` call and its accompanying `print(... raw_primary ...)` line, so only one evaluate() call per epoch remains. Everything else stays byte-for-byte: EMA-based validation via `model.predict_ema(Xva)`, the best/bad/patience logic with the 1e-5 margin, saving `payload['model_state']` from `model.ema_params()`, the nonfinite guard over ('V','W','b','mV','vV','mW','vW','eV','eW','eb'), the training_state/rng capture and the atomic save_checkpoint each epoch, plus the unchanged pairwise structures (grouping on r[1], pos/neg split on r[6], pairs_per_pos repeats, vectorized negative sampling).
3. model.py, features.py, requirements.txt: unchanged (FM already takes k from config; Predictor rebuilds FM with config['k'], so checkpoints stay self-consistent).

Expected cost: the dense Adam/EMA update over the full embedding table scales linearly in k, so roughly 2x the parent's per-step cost, partly offset by dropping the second per-epoch evaluation; expect ~90-130 s, far inside candidate_timeout_s and cheap relative to remaining budget.

Distinguishing note vs supplied prior attempts: every node from genesis through node_006 and every sibling (node_001 feature re-encoding, FFM backbone swap, sampled-softmax loss, 9-field encoding, node_007 3-seed score-space ensemble) kept k=16/lr=0.001/l2=1e-6 fixed; no supplied experiment has varied FM capacity or any other core hyperparameter, and this is not an ensemble, feature, loss or architecture change.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670741 | 0.537103 | 0.603922 | -0.000016 | 60 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py | 2 +-
 train.py  | 2 --
 2 files changed, 1 insertion(+), 3 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index cd7fb6f..a1c0725 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999)
+DEFAULTS = dict(k=32, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999)
 
 
 def resolve(overrides):
diff --git a/train.py b/train.py
index 8d1505b..6142f9a 100644
--- a/train.py
+++ b/train.py
@@ -158,8 +158,6 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
                   for i in range(0, len(perm), config['bs'])]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict_ema(Xva))
-        raw_validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
-        print(f'epoch={epoch} raw_primary={raw_validation["primary"]:.6f} (diagnostic only)', flush=True)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
             Vema, Wema, bema = model.ema_params()
```

---

## Iteration 9: `node_009`

**Status** `success` · **Parent** `node_006` · **Commit** `7548c9d07ae1`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem, specifically label-derived out-of-fold target statistics — never tried anywhere in this lineage): keep the pairwise-BPR + EMA FM, the loss, sampling, optimizer, EMA and all config hyperparameters exactly as in the parent, and extend the input encoding from 5 to 7 categorical fields by adding two leakage-free, out-of-fold smoothed long_view-rate buckets: one for video_id and one for author_id. Hypothesis: within-user ranking is dominated by each candidate item's intrinsic long-view propensity, but raw video_id/author_id embeddings are trained from few pairwise updates for the long tail; a bucketized smoothed long_view rate is a low-variance shared prior that generalizes to rare items and should raise both GAUC and nDCG@5. Distinguishing note vs supplied prior attempts: the only earlier feature experiments (node_001's re-encoding from the pointwise genesis, and node_002's 9-field "richer encoding") changed ID encodings/crosses and used no label statistics; node_007 (seed ensemble) and node_008 (k=32) from this same parent changed averaging and capacity, not features.

Edit features.py and train.py only (config.py, model.py, requirements.txt unchanged; train.train and model.load_predictor contracts, checkpoint layout, splits, target, ranking groups and evaluation unchanged).

1. features.py, fit(rows): keep the existing duration quantile edges, the 5 base vocabs and their per-field dims exactly as they are, then additionally compute, using training rows only, with module-level constants TE_FOLDS = 5, TE_SMOOTH = 20.0, TE_BINS = 16:
   - p = float(mean of r[6]) over rows;
   - for the video field (row[2], vocab index 1) and the author field (row[3], vocab index 2), arrays cnt and sm of shape (len(vocab) + 1, TE_FOLDS) float64, filled by iterating rows with fold = i % TE_FOLDS and e = vocab.get(value, len(vocab)): cnt[e, fold] += 1, sm[e, fold] += float(r[6]);
   - the per-row out-of-fold rate for training row i: rate = (sm[e].sum() - sm[e, fold] + TE_SMOOTH * p) / (cnt[e].sum() - cnt[e, fold] + TE_SMOOTH);
   - bucket edges per entity: edges = np.quantile(oof_rates_over_training_rows, np.linspace(0, 1, TE_BINS + 1)[1:-1]) (15 edges);
   store in the returned state: p, TE_FOLDS/TE_SMOOTH values, n_train = len(rows), and per entity the cnt/sm arrays and rate edges. Append the two new fields' dims (TE_BINS each) after the 5 base dims, and recompute offsets = np.cumsum([0] + dims[:-1]).astype(np.int32) and dim = sum(dims) over all 7 fields so the FM input dimension stays consistent.

2. features.py, transform(rows, state, oof=False): return an int32 array of shape (len(rows), 7). Columns 0-4 are produced exactly as today via raw()/vocabs/offsets. Columns 5 and 6 are the video and author rate buckets: for each row compute e = vocab.get(id, len(vocab)); if oof is True use rate = (sm[e].sum() - sm[e, i % TE_FOLDS] + TE_SMOOTH * p) / (cnt[e].sum() - cnt[e, i % TE_FOLDS] + TE_SMOOTH) with i the row position, otherwise use the full-data rate = (sm[e].sum() + TE_SMOOTH * p) / (cnt[e].sum() + TE_SMOOTH) (unseen ids land on the all-zero last row and therefore get exactly p); then bucket = int(np.clip(np.searchsorted(edges, rate), 0, TE_BINS - 1)) and add the corresponding offset. When oof is True, require len(rows) == state['n_train'] and raise a clear ValueError otherwise, since out-of-fold indexing assumes the training rows in fit order. Vectorize the bucket computation (precompute per-entity totals once, gather with np.asarray of entity indices, and use np.searchsorted on the whole column) so the extra cost stays negligible. Never read r[6] in the non-oof path.

3. train.py: change only the training-matrix construction to Xtr = transform(train_rows, features, oof=True); Xva = transform(valid_rows, features) stays as is (validation rows use statistics fitted on training rows only, so no validation-label leakage). Everything else — the pairwise group/pos/neg structures, vectorized negative sampling, step_pair minibatch loop, EMA-based validation and selection, nonfinite guard, training_state capture and atomic per-epoch save_checkpoint — remains byte-for-byte unchanged. model.py needs no edit because Predictor calls transform(rows, self.features) with the default oof=False and rebuilds FM from features_state['dim'].

Expected cost: field count rises 5 -> 7, so per-step FM and scatter-add work grows about 1.4x, i.e. roughly 80-95 s versus the parent's 58 s, far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670110 | 0.537152 | 0.603631 | -0.000307 | 52 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 72 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---
 train.py    |  2 +-
 2 files changed, 70 insertions(+), 4 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 189b9e0..2af2d8c 100644
--- a/features.py
+++ b/features.py
@@ -25,6 +25,10 @@ while preserving the input-row contract and leakage constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import numpy as np
 
+TE_FOLDS = 5
+TE_SMOOTH = 20.0
+TE_BINS = 16
+
 
 def raw(row, edges):
     return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
@@ -38,14 +42,76 @@ def fit(rows):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
+
+    p = float(np.mean([float(r[6]) for r in rows]))
+    n_train = len(rows)
+
+    entity_stats = {}
+    for field_name, row_idx, vocab_idx in (('video', 2, 1), ('author', 3, 2)):
+        vocab = vocabs[vocab_idx]
+        n_e = len(vocab) + 1
+        cnt = np.zeros((n_e, TE_FOLDS), dtype=np.float64)
+        sm = np.zeros((n_e, TE_FOLDS), dtype=np.float64)
+        for i, r in enumerate(rows):
+            fold = i % TE_FOLDS
+            e = vocab.get(r[row_idx], len(vocab))
+            cnt[e, fold] += 1
+            sm[e, fold] += float(r[6])
+        cnt_tot = cnt.sum(1)
+        sm_tot = sm.sum(1)
+        oof_rates = np.empty(n_train, dtype=np.float64)
+        for i, r in enumerate(rows):
+            fold = i % TE_FOLDS
+            e = vocab.get(r[row_idx], len(vocab))
+            rate = (sm_tot[e] - sm[e, fold] + TE_SMOOTH * p) / (cnt_tot[e] - cnt[e, fold] + TE_SMOOTH)
+            oof_rates[i] = rate
+        te_edges = np.quantile(oof_rates, np.linspace(0, 1, TE_BINS + 1)[1:-1])
+        entity_stats[field_name] = dict(cnt=cnt, sm=sm, edges=te_edges)
+
+    dims = dims + [TE_BINS, TE_BINS]
+
     return dict(edges=edges, vocabs=vocabs,
-                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
+                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims),
+                p=p, te_folds=TE_FOLDS, te_smooth=TE_SMOOTH, n_train=n_train,
+                video=entity_stats['video'], author=entity_stats['author'])
+
 
+def _te_bucket_column(rows, row_idx, vocab, stats, p, folds, smooth, oof):
+    cnt = stats['cnt']
+    sm = stats['sm']
+    edges = stats['edges']
+    cnt_tot = cnt.sum(1)
+    sm_tot = sm.sum(1)
+    entities = np.asarray([vocab.get(r[row_idx], len(vocab)) for r in rows], dtype=np.int64)
+    if oof:
+        fold_idx = np.arange(len(rows)) % folds
+        rate = (sm_tot[entities] - sm[entities, fold_idx] + smooth * p) / \
+               (cnt_tot[entities] - cnt[entities, fold_idx] + smooth)
+    else:
+        rate = (sm_tot[entities] + smooth * p) / (cnt_tot[entities] + smooth)
+    buckets = np.clip(np.searchsorted(edges, rate), 0, len(edges))
+    return buckets.astype(np.int32)
 
-def transform(rows, state):
-    result = np.empty((len(rows), 5), dtype=np.int32)
+
+def transform(rows, state, oof=False):
+    if oof and len(rows) != state['n_train']:
+        raise ValueError('oof transform requires rows to match training rows in fit order')
+    result = np.empty((len(rows), 7), dtype=np.int32)
     for n, row in enumerate(rows):
         for i, value in enumerate(raw(row, state['edges'])):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
+
+    p = state['p']
+    folds = state['te_folds']
+    smooth = state['te_smooth']
+
+    video_vocab = state['vocabs'][1]
+    author_vocab = state['vocabs'][2]
+
+    video_buckets = _te_bucket_column(rows, 2, video_vocab, state['video'], p, folds, smooth, oof)
+    author_buckets = _te_bucket_column(rows, 3, author_vocab, state['author'], p, folds, smooth, oof)
+
+    result[:, 5] = video_buckets + state['offsets'][5]
+    result[:, 6] = author_buckets + state['offsets'][6]
     return result
diff --git a/train.py b/train.py
index 8d1505b..dea704b 100644
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

## Iteration 10: `node_010`

**Status** `success` · **Parent** `node_006` · **Commit** `9c09aa9961bb`

### Hypothesis

```text
SELECTED CHANGE
SELECTED CHANGE
Experiment (training-objective weighting / pair-sampling subsystem — untouched in this lineage): make the in-user pairwise BPR objective user-balanced, so that every qualifying user contributes the same total gradient weight per epoch instead of a weight proportional to that user's number of positives. Hypothesis: the evaluation metric averages per user (GAUC over user groups, nDCG@5 per group), but the current training distribution builds pairs_per_pos pairs per positive row, so a user with 50 positives dominates a user with 1 positive by 50x. Re-weighting each pair by 1/n_pos(user) aligns the optimization distribution with the per-user averaged metric, should improve ranking quality for the many light users that the metric weights equally, and costs essentially nothing in runtime. Distinguishing note vs supplied prior attempts: the three siblings from this same parent changed model averaging (node_007, 3-seed score ensemble), capacity (node_008, k=32) and features (node_009, out-of-fold target encoding); node_002's sibling replaced BPR with a multi-negative sampled softmax. No supplied experiment has changed how pairs are weighted or how users are balanced in the training signal; the loss stays one-negative BPR and the 5-field encoding, EMA, optimizer and all other hyperparameters stay exactly as in the parent.

Edit config.py, model.py and train.py only (features.py and requirements.txt stay exactly as supplied; train.train and model.load_predictor signatures, the version/config/features_state/model_state/training_state/context checkpoint layout, atomic saving, splits, target, ranking groups and evaluation via agent.sandbox.protocol.evaluate are unchanged).

1. config.py: add user_balance_power=1.0 to DEFAULTS and validate it in resolve() as a finite float with 0.0 <= user_balance_power <= 1.0 (raise ValueError('invalid user_balance_power') otherwise). Leave k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999 unchanged.

2. model.py: change FM.step_pair(self, Xp, Xn) to FM.step_pair(self, Xp, Xn, w=None). Inside, set B = len(Xp); if w is None treat it as all ones, else use wb = np.asarray(w, dtype=np.float32). Compute zp/Ep/Sp and zn/En/Sn exactly as today, d = zp - zn, s = sigmoid(-d), and change only the per-example gradient scale to g = (s * wb / B).astype(np.float32); leave the np.add.at scatter-adds into gW/gV, the L2 terms, self.t increment, the Adam update over (V, gV, mV, vV) and (W, gW, mW, vW), and the EMA buffer update (eV/eW/eb with self.ema_decay) byte-for-byte as they are. Return the weighted mean loss float(np.sum(wb * -np.log(sigmoid(d) + 1e-9)) / B). Do not touch FM.logits, FM.step, FM.ema_params, FM.predict, FM.predict_ema, read_checkpoint, Predictor or load_predictor (vars(model) key set is unchanged, so the resume check in train.py still matches).

3. train.py: while building the pairwise structures, also build a float32 per-pair weight array aligned element-by-element with pos_idx: for each qualifying user (those with at least one positive and at least one negative), each of that user's pair entries gets weight (1.0 / len(poss)) ** config['user_balance_power']; after the loop convert to np.asarray(..., dtype=np.float32) and rescale it so its mean is exactly 1.0 (w *= len(w) / w.sum(), guarding against a zero/nonfinite sum), keeping the overall gradient magnitude comparable to the parent. In the epoch loop, permute the weights with the same perm as the positives/negatives (w_perm = pair_w[perm]) and pass the matching slice to the step: model.step_pair(Xtr[pos_perm[i:i+bs]], Xtr[neg_perm[i:i+bs]], w_perm[i:i+bs]). Everything else in train() stays as supplied: grouping on r[1], pos/neg split on r[6], pairs_per_pos repeats, vectorized negative sampling via neg_flat[starts + (rng.random(len(pos_idx)) * lengths).astype(np.int64)], EMA-based validation (model.predict_ema(Xva)) with the same best/bad/patience logic and 1e-5 margin, saving payload['model_state'] from model.ema_params(), the nonfinite guard over ('V','W','b','mV','vV','mW','vW','eV','eW','eb'), training_state/rng capture and per-epoch atomic save_checkpoint. As a supporting cost-control edit for this same experiment, delete the per-epoch diagnostic raw-weight evaluation (the raw_validation = evaluate(...) call and its raw_primary print), which never affects selection, so only one evaluate() call per epoch remains.

Expected cost is at or slightly below the parent's 57.7 s (one fewer validation pass per epoch, one extra elementwise multiply per step), far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.666101 | 0.535328 | 0.600714 | -0.003223 | 46 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 model.py  | 10 +++++++---
 train.py  | 14 ++++++++++----
 3 files changed, 20 insertions(+), 8 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index cd7fb6f..6dbd0b9 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999, user_balance_power=1.0)
 
 
 def resolve(overrides):
@@ -38,4 +38,6 @@ def resolve(overrides):
             raise ValueError(f'invalid {key}')
     if not math.isfinite(config['ema_decay']) or not 0 < config['ema_decay'] < 1:
         raise ValueError('invalid ema_decay')
+    if not math.isfinite(config['user_balance_power']) or not 0.0 <= config['user_balance_power'] <= 1.0:
+        raise ValueError('invalid user_balance_power')
     return config
diff --git a/model.py b/model.py
index e88f150..4da7847 100644
--- a/model.py
+++ b/model.py
@@ -69,13 +69,17 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
-    def step_pair(self, Xp, Xn):
+    def step_pair(self, Xp, Xn, w=None):
         B = len(Xp)
+        if w is None:
+            wb = np.ones(B, dtype=np.float32)
+        else:
+            wb = np.asarray(w, dtype=np.float32)
         zp, Ep, Sp = self.logits(Xp)
         zn, En, Sn = self.logits(Xn)
         d = zp - zn
         s = sigmoid(-d)
-        g = (s / B).astype(np.float32)
+        g = (s * wb / B).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, Xp, -g[:, None])
         np.add.at(gW, Xn, g[:, None])
@@ -92,7 +96,7 @@ class FM:
         self.eV *= decay; self.eV += (1 - decay) * self.V
         self.eW *= decay; self.eW += (1 - decay) * self.W
         self.eb = np.float32(decay * self.eb + (1 - decay) * self.b)
-        return float(np.mean(-np.log(sigmoid(d) + 1e-9)))
+        return float(np.sum(wb * -np.log(sigmoid(d) + 1e-9)) / B)
 
     def ema_params(self):
         if self.t == 0:
diff --git a/train.py b/train.py
index 8d1505b..095babc 100644
--- a/train.py
+++ b/train.py
@@ -127,17 +127,19 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     for idx, r in enumerate(train_rows):
         groups.setdefault(r[1], [[], []])[int(r[6])].append(idx)
 
-    pos_list, neg_flat_list, starts, lengths = [], [], [], []
+    pos_list, neg_flat_list, starts, lengths, weight_list = [], [], [], [], []
     offset = 0
     for _uid, (negs, poss) in groups.items():
         if not poss or not negs:
             continue
         neg_flat_list.extend(negs)
+        pair_weight = (1.0 / len(poss)) ** config['user_balance_power']
         for p in poss:
             for _ in range(config['pairs_per_pos']):
                 pos_list.append(p)
                 starts.append(offset)
                 lengths.append(len(negs))
+                weight_list.append(pair_weight)
         offset += len(negs)
 
     if not pos_list:
@@ -147,6 +149,11 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     neg_flat = np.asarray(neg_flat_list, dtype=np.int32)
     starts = np.asarray(starts, dtype=np.int64)
     lengths = np.asarray(lengths, dtype=np.int64)
+    pair_w = np.asarray(weight_list, dtype=np.float32)
+    wsum = pair_w.sum()
+    if not np.isfinite(wsum) or wsum == 0:
+        raise ValueError('invalid pair weight sum')
+    pair_w *= len(pair_w) / wsum
 
     for epoch in range(epoch + 1, config['epochs'] + 1):
         if bad >= config['patience']:
@@ -155,11 +162,10 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         perm = rng.permutation(len(pos_idx))
         pos_perm = pos_idx[perm]
         neg_perm = neg_idx[perm]
-        losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
+        w_perm = pair_w[perm]
+        losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]], w_perm[i:i + config['bs']])
                   for i in range(0, len(perm), config['bs'])]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict_ema(Xva))
-        raw_validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
-        print(f'epoch={epoch} raw_primary={raw_validation["primary"]:.6f} (diagnostic only)', flush=True)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
             Vema, Wema, bema = model.ema_params()
```

---

## Iteration 11: `node_011`

**Status** `success` · **Parent** `node_006` · **Commit** `e8217c8c21ae`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss-formulation subsystem, hybrid objective): from node_006 (pairwise in-user BPR + EMA FM, 5-field encoding, k=16), add an auxiliary pointwise binary-cross-entropy term to the pairwise update so the objective becomes L = BPR(z_pos - z_neg) + point_weight * [BCE(z_pos, 1) + BCE(z_neg, 0)], computed on exactly the same rows that are already in each pair minibatch (no extra forward pass). Hypothesis: pure BPR only constrains score *differences*, leaving each row's absolute score unanchored, so embeddings of frequently sampled ids drift and rarely-updated ids stay near initialization; adding an absolute per-row target term re-injects the global item/duration/tab quality signal (pointwise-only training reached 0.6015 primary at genesis, close to BPR's 0.6033), acting as a regularizer that should sharpen within-user ordering and lift GAUC/nDCG@5. Distinguishing note vs supplied prior attempts: the only other loss experiment in this lineage replaced BPR with a multi-negative sampled softmax (from node_002, -0.0001), node_010 reweighted pairs across users (-0.0032), and the siblings from this same parent changed ensembling (node_007), capacity (node_008) and features (node_009); none combined the pairwise and pointwise objectives in a single update.

Edit config.py, model.py and train.py only (features.py and requirements.txt stay exactly as supplied; train.train and model.load_predictor signatures, the version/config/features_state/model_state/training_state/context checkpoint layout, atomic saving, splits, target, ranking groups and evaluation via agent.sandbox.protocol.evaluate stay unchanged).

1. config.py: add point_weight=0.3 to DEFAULTS and validate it in resolve() as a finite float with point_weight >= 0 (raise ValueError('invalid point_weight')). Leave k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999 unchanged.

2. model.py: change the signature to FM.step_pair(self, Xp, Xn, point_weight=0.0). Keep B = len(Xp), zp, Ep, Sp = self.logits(Xp), zn, En, Sn = self.logits(Xn), d = zp - zn, s = sigmoid(-d). Replace the single scale g by two per-example scales that fold in the pointwise gradients: gp = (-s / B + point_weight * (sigmoid(zp) - 1.0) / B).astype(np.float32) and gn = (s / B + point_weight * sigmoid(zn) / B).astype(np.float32). Scatter with np.add.at(gW, Xp, gp[:, None]); np.add.at(gW, Xn, gn[:, None]); np.add.at(gV, Xp, gp[:, None, None] * (Sp[:, None, :] - Ep)); np.add.at(gV, Xn, gn[:, None, None] * (Sn[:, None, :] - En)). Keep the existing L2 terms (gV += self.l2 * self.V; gW += self.l2 * self.W), the self.t increment, the identical Adam update (b1=0.9, b2=0.999, eps=1e-8) over (V, gV, mV, vV) and (W, gW, mW, vW), and the existing EMA buffer update of eV/eW/eb with self.ema_decay. Additionally, when point_weight > 0, update the global bias with plain SGD on the pointwise part only: self.b = np.float32(self.b - self.lr * float(gp.sum() + gn.sum())) (the BPR contribution cancels in gp + gn), placed before the EMA buffer update so eb tracks the updated bias. Return float(np.mean(-np.log(sigmoid(d) + 1e-9)) + point_weight * np.mean(-np.log(sigmoid(zp) + 1e-9) - np.log(1 - sigmoid(zn) + 1e-9))) for logging. Do not add or remove any instance attributes, so vars(model) and the resume check in train.py remain valid; leave FM.logits, FM.step, FM.ema_params, FM.predict, FM.predict_ema, read_checkpoint, Predictor and load_predictor untouched.

3. train.py: pass the new argument in the minibatch loop, i.e. model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]], config['point_weight']). As a supporting cost-control edit for this same experiment, delete the per-epoch diagnostic raw-weight evaluation (the raw_validation = evaluate(...) call and its raw_primary print), which never affects selection, so only one evaluate() call per epoch remains. Everything else stays byte-for-byte: pair construction (grouping on r[1], pos/neg split on r[6], pairs_per_pos repeats), vectorized negative sampling, EMA-based validation via model.predict_ema(Xva) with the same best/bad/patience logic and 1e-5 margin, saving payload['model_state'] from model.ema_params(), the nonfinite guard over ('V','W','b','mV','vV','mW','vW','eV','eW','eb'), training_state/rng capture and per-epoch atomic save_checkpoint.

Expected cost is at or slightly below the parent's 57.7 s (no extra forward passes, one fewer validation pass per epoch), far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.670418 | 0.537019 | 0.603719 | -0.000219 | 35 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 +++-
 model.py  | 17 ++++++++++-------
 train.py  |  4 +---
 3 files changed, 14 insertions(+), 11 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index cd7fb6f..cb31605 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999)
+DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=60, bs=4096, patience=5, seed=0, pairs_per_pos=2, ema_decay=0.999, point_weight=0.3)
 
 
 def resolve(overrides):
@@ -38,4 +38,6 @@ def resolve(overrides):
             raise ValueError(f'invalid {key}')
     if not math.isfinite(config['ema_decay']) or not 0 < config['ema_decay'] < 1:
         raise ValueError('invalid ema_decay')
+    if not math.isfinite(config['point_weight']) or config['point_weight'] < 0:
+        raise ValueError('invalid point_weight')
     return config
diff --git a/model.py b/model.py
index e88f150..035fee5 100644
--- a/model.py
+++ b/model.py
@@ -69,18 +69,19 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
-    def step_pair(self, Xp, Xn):
+    def step_pair(self, Xp, Xn, point_weight=0.0):
         B = len(Xp)
         zp, Ep, Sp = self.logits(Xp)
         zn, En, Sn = self.logits(Xn)
         d = zp - zn
         s = sigmoid(-d)
-        g = (s / B).astype(np.float32)
+        gp = (-s / B + point_weight * (sigmoid(zp) - 1.0) / B).astype(np.float32)
+        gn = (s / B + point_weight * sigmoid(zn) / B).astype(np.float32)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
-        np.add.at(gW, Xp, -g[:, None])
-        np.add.at(gW, Xn, g[:, None])
-        np.add.at(gV, Xp, -g[:, None, None] * (Sp[:, None, :] - Ep))
-        np.add.at(gV, Xn, g[:, None, None] * (Sn[:, None, :] - En))
+        np.add.at(gW, Xp, gp[:, None])
+        np.add.at(gW, Xn, gn[:, None])
+        np.add.at(gV, Xp, gp[:, None, None] * (Sp[:, None, :] - Ep))
+        np.add.at(gV, Xn, gn[:, None, None] * (Sn[:, None, :] - En))
         gV += self.l2 * self.V; gW += self.l2 * self.W
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
@@ -88,11 +89,13 @@ class FM:
             M *= b1; M += (1 - b1) * G
             Vv *= b2; Vv += (1 - b2) * (G * G)
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
+        if point_weight > 0:
+            self.b = np.float32(self.b - self.lr * float(gp.sum() + gn.sum()))
         decay = self.ema_decay
         self.eV *= decay; self.eV += (1 - decay) * self.V
         self.eW *= decay; self.eW += (1 - decay) * self.W
         self.eb = np.float32(decay * self.eb + (1 - decay) * self.b)
-        return float(np.mean(-np.log(sigmoid(d) + 1e-9)))
+        return float(np.mean(-np.log(sigmoid(d) + 1e-9)) + point_weight * np.mean(-np.log(sigmoid(zp) + 1e-9) - np.log(1 - sigmoid(zn) + 1e-9)))
 
     def ema_params(self):
         if self.t == 0:
diff --git a/train.py b/train.py
index 8d1505b..db347c1 100644
--- a/train.py
+++ b/train.py
@@ -155,11 +155,9 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         perm = rng.permutation(len(pos_idx))
         pos_perm = pos_idx[perm]
         neg_perm = neg_idx[perm]
-        losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]])
+        losses = [model.step_pair(Xtr[pos_perm[i:i + config['bs']]], Xtr[neg_perm[i:i + config['bs']]], config['point_weight'])
                   for i in range(0, len(perm), config['bs'])]
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict_ema(Xva))
-        raw_validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
-        print(f'epoch={epoch} raw_primary={raw_validation["primary"]:.6f} (diagnostic only)', flush=True)
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
             Vema, Wema, bema = model.ema_params()
```

---

## Iteration 12: `node_012`

**Status** `success` · **Parent** `genesis` · **Commit** `13fb24475dca`

### Hypothesis

```text
SELECTED CHANGE
Experiment (model-backbone subsystem — never touched from this parent; the two supplied siblings from genesis changed features.py encoding (node_001, -0.0039) and the loss to pairwise BPR (node_002, +0.0018), both keeping the plain shared-embedding FM): replace the shared-embedding factorization machine with a Field-aware Factorization Machine (FFM) while keeping the pointwise BCE loss, the supplied 5-field encoding, and all training/eval contracts unchanged. Hypothesis: with only 5 fields (user_id, video_id, author_id, tab, duration bucket), a single k=16 embedding per feature must serve every interaction at once; giving each feature a separate embedding per interacting field lets, e.g., the user embedding used against video_id differ from the one used against tab/duration, which should sharpen the within-user discrimination that GAUC and nDCG@5 measure. This is distinct from both supplied siblings (encoding change / loss change) and from anything in memory.

Implementation:
1. model.py: keep the class name FM (train.py imports it) and keep logits/step/predict/Predictor/read_checkpoint/load_predictor signatures and the checkpoint weight names ('V','W','b'). Change __init__ to FM(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, fields=5): V = rng.normal(0, 0.01, (dim, fields, k)).astype(np.float32) (field-aware embeddings), W = zeros(dim), b = float32(0), Adam buffers mV/vV shaped like V and mW/vW like W, t=0; store self.fields and a precomputed pair list PAIRS = [(i, j) for i in range(fields) for j in range(i+1, fields)] (10 pairs for 5 fields). logits(X) with X of shape (B,F): E = self.V[X] with shape (B,F,F,k) where E[b,i,f] = V[X[b,i], f]; inter = sum over (i,j) in PAIRS of (E[:,i,j,:] * E[:,j,i,:]).sum(1); return (self.b + self.W[X].sum(1) + inter, E, None) keeping a 3-tuple return so existing call sites still unpack. step(X, y) keeps the pointwise BCE gradient: g = ((sigmoid(z) - y) / B).astype(np.float32); gW zeros_like(W) with np.add.at(gW, X, g[:, None]); gV zeros_like(V) accumulated per pair with np.add.at(gV, (X[:, i], j), g[:, None] * E[:, j, i, :]) and np.add.at(gV, (X[:, j], i), g[:, None] * E[:, i, j, :]) for every (i, j) in PAIRS; then gV += self.l2 * self.V; gW += self.l2 * self.W; identical Adam update (b1=0.9, b2=0.999, eps=1e-8, self.t += 1) over (V,gV,mV,vV) and (W,gW,mW,vW); self.b -= self.lr * g.sum(); return the same mean binary log-loss float. Reduce the predict default batch size to bs=50_000 to bound the (B,F,F,k) temporary. In Predictor.__init__, construct FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], fields=self.features['fields']) and keep the existing shape/finiteness validation of restored V/W/b.
2. features.py: only change is that fit() additionally stores fields=len(vocabs) in the returned state dict (raw/transform/vocab logic, duration edges, offsets, dim and the OOV convention stay exactly as supplied).
3. train.py: pass fields=features['fields'] to both FM(...) constructions (fresh and resume paths); everything else (epoch loop, evaluate call, best/bad/patience tracking, nonfinite checks, training_state capture with vars(model), atomic save_checkpoint, payload layout) stays unchanged.
4. config.py: change DEFAULTS k from 16 to 8 (field-aware embeddings multiply parameters by the field count, so k=8 keeps per-feature capacity comparable at 5*8=40 vs 16 and keeps runtime near baseline); leave lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0 and the existing resolve() validation unchanged.

Expected cost is roughly 2-3x the 36 s genesis baseline (larger fancy-indexed embedding gather, 20 np.add.at calls of the same total element count), i.e. ~100 s, far inside candidate_timeout_s.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668809 | 0.536468 | 0.602638 | +0.001170 | 51 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py   |  2 +-
 features.py |  3 ++-
 model.py    | 26 ++++++++++++++++----------
 train.py    |  4 ++--
 4 files changed, 21 insertions(+), 14 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index 147c6ac..d7123ea 100644
--- a/config.py
+++ b/config.py
@@ -22,7 +22,7 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=8, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)
 
 
 def resolve(overrides):
diff --git a/features.py b/features.py
index 189b9e0..cedab35 100644
--- a/features.py
+++ b/features.py
@@ -39,7 +39,8 @@ def fit(rows):
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
     return dict(edges=edges, vocabs=vocabs,
-                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims))
+                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims),
+                fields=len(vocabs))
 
 
 def transform(rows, state):
diff --git a/model.py b/model.py
index 495d48e..3fd7205 100644
--- a/model.py
+++ b/model.py
@@ -32,9 +32,11 @@ from features import transform
 def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
 
 class FM:
-    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
+    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0, fields=5):
         rng = np.random.default_rng(seed)
-        self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
+        self.fields = fields
+        self.PAIRS = [(i, j) for i in range(fields) for j in range(i + 1, fields)]
+        self.V = rng.normal(0, 0.01, (dim, fields, k)).astype(np.float32)
         self.W = np.zeros(dim, dtype=np.float32)
         self.b = np.float32(0.0)
         self.lr, self.l2 = lr, l2
@@ -43,18 +45,22 @@ class FM:
         self.t = 0
 
     def logits(self, X):
-        E = self.V[X]                                   # (B,F,k)
-        S = E.sum(1)                                    # (B,k)
-        inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
-        return self.b + self.W[X].sum(1) + inter, E, S
+        E = self.V[X]                                   # (B,F,F,k)
+        inter = None
+        for i, j in self.PAIRS:
+            term = (E[:, i, j, :] * E[:, j, i, :]).sum(1)
+            inter = term if inter is None else inter + term
+        return self.b + self.W[X].sum(1) + inter, E, None
 
     def step(self, X, y):
         B = len(y)
-        z, E, S = self.logits(X)
+        z, E, _ = self.logits(X)
         g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
-        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
+        for i, j in self.PAIRS:
+            np.add.at(gV, (X[:, i], j), g[:, None] * E[:, j, i, :])
+            np.add.at(gV, (X[:, j], i), g[:, None] * E[:, i, j, :])
         gV += self.l2 * self.V; gW += self.l2 * self.W
         self.t += 1
         b1, b2, eps = 0.9, 0.999, 1e-8
@@ -65,7 +71,7 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
-    def predict(self, X, bs=200_000):
+    def predict(self, X, bs=50_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
 def read_checkpoint(path):
@@ -85,7 +91,7 @@ class Predictor:
     def __init__(self, state):
         config = state['config']
         self.features = state['features_state']
-        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], fields=self.features['fields'])
         weights = state['model_state']
         for name in ('V', 'W', 'b'):
             value = weights[name]
diff --git a/train.py b/train.py
index 0451b1a..15b3ad4 100644
--- a/train.py
+++ b/train.py
@@ -98,7 +98,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         features = payload['features_state']
         state = payload['training_state']
         rng.bit_generator.state = state['rng']
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], fields=features['fields'])
         if set(state['latest']) != set(vars(model)):
             raise ValueError('incomplete optimizer/model state')
         for key, value in state['latest'].items():
@@ -115,7 +115,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         print(f'resume: completed epoch={epoch}, optimizer step={model.t}', flush=True)
     else:
         features = fit(train_rows)
-        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
+        model = FM(features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'], fields=features['fields'])
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
```

---

## Iteration 13: `node_013`

**Status** `success` · **Parent** `node_012` · **Commit** `99a69631a40e`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem, exploiting the FFM backbone already present in this parent): add two derived frequency/popularity bucket fields to the 5-field encoding so the field-aware model can learn popularity- and activity-conditioned interactions. Hypothesis: with only raw ID fields, rare videos/users get poorly estimated embeddings; a video-popularity field interacting (field-aware) with user_id/author_id/tab and a user-activity field interacting with video_id/author_id give the model shared, well-estimated parameters that modulate item scores for cold items and cold users, which should sharpen within-user ordering measured by GAUC and nDCG@5. This differs from the only supplied feature-side attempt (node_001 from the genesis plain-FM parent, which re-encoded existing fields and lost 0.0039): here new count-derived fields are added on top of the FFM parent, where each new field gets its own per-interaction embeddings; no supplied sibling or ancestor of this parent added derived popularity features.

Implementation:
1. features.py: in fit(rows), first compute duration `edges` exactly as now, plus two count dictionaries over training rows only (no labels touched): user_counts[row[1]] += 1 and video_counts[row[2]] += 1. Add a helper `count_bucket(n)` returning `'c' + str(min(15, int(np.log2(n + 1))))`. Change `raw(row, state)` to take the fitted state dict (containing 'edges', 'user_counts', 'video_counts') and return 7 string/ID values in this order: [row[1], row[2], row[3], row[4], str(int(np.searchsorted(state['edges'], row[5]))), count_bucket(state['user_counts'].get(row[1], 0)), count_bucket(state['video_counts'].get(row[2], 0))]. In fit, build a temporary base state dict (edges, user_counts, video_counts), then build `vocabs = [{} for _ in range(7)]` with the same loop over raw(row, base_state); dims/offsets/dim computed exactly as now; return dict(edges=..., user_counts=..., video_counts=..., vocabs=..., offsets=..., dim=..., fields=len(vocabs)) so fields becomes 7 automatically. In transform, allocate `np.empty((len(rows), len(state['vocabs'])), dtype=np.int32)` and call raw(row, state); keep the existing unseen-value OOV convention `vocab.get(value, len(vocab)) + offsets[i]` unchanged (an unseen video therefore maps to an OOV popularity bucket, a useful cold-item marker) and keep input row order.
2. model.py: no architectural change; only reduce the FM.predict default batch size from bs=50_000 to bs=25_000 so the (B,F,F,k) gather with F=7 stays bounded in memory. Keep the FM/Predictor/read_checkpoint/load_predictor signatures, checkpoint weight names ('V','W','b'), the field-aware logits/step math, and the `fields` constructor argument as supplied.
3. train.py and config.py: unchanged (fields is already read from features['fields'] on both fresh and resume paths; keep k=8, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0).

Cost: pairs grow from 10 to 21, so expect roughly 2-2.5x the 50 s parent runtime (~110-130 s), well inside candidate_timeout_s and the remaining budget. No change to splits, long_view target, ranking groups, or evaluation.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668530 | 0.537157 | 0.602844 | +0.000205 | 91 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 26 +++++++++++++++++++-------
 model.py    |  2 +-
 2 files changed, 20 insertions(+), 8 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index cedab35..591638d 100644
--- a/features.py
+++ b/features.py
@@ -26,27 +26,39 @@ while preserving the input-row contract and leakage constraints.
 import numpy as np
 
 
-def raw(row, edges):
-    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(edges, row[5])))]
+def count_bucket(n):
+    return 'c' + str(min(15, int(np.log2(n + 1))))
+
+
+def raw(row, state):
+    return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(state['edges'], row[5]))),
+            count_bucket(state['user_counts'].get(row[1], 0)),
+            count_bucket(state['video_counts'].get(row[2], 0))]
 
 
 def fit(rows):
     edges = np.quantile([r[5] for r in rows], np.linspace(0, 1, 11)[1:-1])
-    vocabs = [{} for _ in range(5)]
+    user_counts = {}
+    video_counts = {}
+    for row in rows:
+        user_counts[row[1]] = user_counts.get(row[1], 0) + 1
+        video_counts[row[2]] = video_counts.get(row[2], 0) + 1
+    base_state = dict(edges=edges, user_counts=user_counts, video_counts=video_counts)
+    vocabs = [{} for _ in range(7)]
     for row in rows:
-        for i, value in enumerate(raw(row, edges)):
+        for i, value in enumerate(raw(row, base_state)):
             if value not in vocabs[i]:
                 vocabs[i][value] = len(vocabs[i])
     dims = [len(v) + 1 for v in vocabs]
-    return dict(edges=edges, vocabs=vocabs,
+    return dict(edges=edges, user_counts=user_counts, video_counts=video_counts, vocabs=vocabs,
                 offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims),
                 fields=len(vocabs))
 
 
 def transform(rows, state):
-    result = np.empty((len(rows), 5), dtype=np.int32)
+    result = np.empty((len(rows), len(state['vocabs'])), dtype=np.int32)
     for n, row in enumerate(rows):
-        for i, value in enumerate(raw(row, state['edges'])):
+        for i, value in enumerate(raw(row, state)):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
     return result
diff --git a/model.py b/model.py
index 3fd7205..2837565 100644
--- a/model.py
+++ b/model.py
@@ -71,7 +71,7 @@ class FM:
         self.b -= self.lr * g.sum()
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
-    def predict(self, X, bs=50_000):
+    def predict(self, X, bs=25_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
 def read_checkpoint(path):
```

---

## Iteration 14: `node_014`

**Status** `success` · **Parent** `node_013` · **Commit** `75816a77b08e`

### Hypothesis

```text
SELECTED CHANGE
Experiment (loss-formulation subsystem, transferred to this branch's FFM + count-feature code state): replace the pointwise BCE objective in the selected parent (node_013: field-aware FM with 7 fields including the user/video popularity buckets, k=8) with a pure in-user pairwise BPR ranking objective, keeping the FFM backbone, the 7-field encoding, and all train/predict contracts unchanged. Hypothesis: GAUC and nDCG@5 only depend on within-user ordering, and a pairwise objective optimizes exactly that; this branch has so far only improved the backbone (FFM) and the feature set, both under pointwise BCE, so the loss is the untouched lever here. The closest supplied prior attempts are node_002 (BPR applied to the genesis plain shared-embedding FM, k=16, 5 raw fields, +0.0018) and node_011 (AVOID: adding an auxiliary pointwise BCE term on top of an existing pairwise+EMA model, -0.0002). This is a transfer of the pure pairwise idea onto a materially different parent (field-aware embeddings with per-field-pair parameters plus derived popularity fields), not a re-run of either: field-aware embeddings have many more per-feature parameters that the pointwise loss trains only through absolute-probability calibration, so a ranking loss should sharpen them more than it did the small shared-embedding FM; no hybrid/auxiliary pointwise term is used.

Implementation:
1. model.py: keep the class name FM and the existing __init__ (V shape (dim, fields, k), W, b, Adam buffers mV/vV/mW/vW, t, fields, PAIRS), logits(X), predict(X, bs=25_000), read_checkpoint, Predictor, and load_predictor exactly as supplied, and keep checkpoint weight names ('V','W','b'). Factor the gradient accumulation + Adam update currently inside step() into a private helper _update(X, E, g) that (a) builds gW/gV zeros_like, (b) np.add.at(gW, X, g[:, None]), (c) for each (i, j) in self.PAIRS does np.add.at(gV, (X[:, i], j), g[:, None] * E[:, j, i, :]) and np.add.at(gV, (X[:, j], i), g[:, None] * E[:, i, j, :]), (d) adds l2*V / l2*W, (e) increments self.t and applies the identical Adam update (b1=0.9, b2=0.999, eps=1e-8) to (V,gV,mV,vV) and (W,gW,mW,vW), and (f) self.b -= self.lr * g.sum(). Leave the existing pointwise step(X, y) in place (unused) and add a new method step_pairwise(Xp, Xn): X = np.concatenate([Xp, Xn], axis=0); z, E, _ = self.logits(X); B = len(Xp); d = z[:B] - z[B:]; s = sigmoid(d); gp = (-(1.0 - s) / B).astype(np.float32); g = np.concatenate([gp, -gp]).astype(np.float32); call self._update(X, E, g); return float(-np.mean(np.log(s + 1e-9))) as the logged loss. Do NOT add any new non-array instance attributes to FM (train.py resume validates set(vars(model)) and np.shape/np.isfinite on every attribute).
2. train.py: keep the train(train_rows, valid_rows, checkpoint_path, overrides, context) signature, the resume/fresh checkpoint logic, atomic save_checkpoint, evaluate(...) call on model.predict(Xva), best/bad/patience tracking, nonfinite checks, and payload layout unchanged. After computing Xtr/ytr, build the pair-sampling index structures once (all derived from training rows only, no leakage): map each training row's user_id (train_rows[i][1]) to a compact integer code; collect per-user positive row indices (ytr == 1) and negative row indices (ytr == 0); keep only users having at least one positive and at least one negative; build (a) pos_idx: int64 array of all eligible positive row indices, (b) pos_user: matching user codes, (c) a flattened negative index array neg_flat with per-user neg_start and neg_count int64 arrays. Replace the per-epoch pointwise loop with: order = rng.permutation(len(pos_idx)); for each slice of size config['bs'] take p = pos_idx[order[i:i+bs]] and u = pos_user[order[i:i+bs]], draw offsets = (rng.random(len(u)) * neg_count[u]).astype(np.int64), n = neg_flat[neg_start[u] + offsets], and call model.step_pairwise(Xtr[p], Xtr[n]); collect the returned losses for the existing mean-loss print. Keep using the same rng object so the resume path's rng state capture stays exact.
3. config.py: keep DEFAULTS unchanged (k=8, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0) and resolve() unchanged; bs now means pairs per step (8192 positives + 8192 negatives = 16384 rows forwarded, whose (B,F,F,k) temporary is ~25 MB with F=7, k=8).
4. features.py: unchanged.

Expected cost is roughly comparable to the 90 s parent (about 2x work per step but fewer steps per epoch since only positives seed pairs), i.e. well under 300 s, safely inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668984 | 0.536283 | 0.602634 | -0.000210 | 58 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
model.py | 22 ++++++++++++++++++----
 train.py | 49 ++++++++++++++++++++++++++++++++++++++++++++++---
 2 files changed, 64 insertions(+), 7 deletions(-)
```

```diff
diff --git a/model.py b/model.py
index 2837565..4ba09a5 100644
--- a/model.py
+++ b/model.py
@@ -52,10 +52,7 @@ class FM:
             inter = term if inter is None else inter + term
         return self.b + self.W[X].sum(1) + inter, E, None
 
-    def step(self, X, y):
-        B = len(y)
-        z, E, _ = self.logits(X)
-        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
+    def _update(self, X, E, g):
         gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
         np.add.at(gW, X, g[:, None])
         for i, j in self.PAIRS:
@@ -69,8 +66,25 @@ class FM:
             Vv *= b2; Vv += (1 - b2) * (G * G)
             P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
         self.b -= self.lr * g.sum()
+
+    def step(self, X, y):
+        B = len(y)
+        z, E, _ = self.logits(X)
+        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
+        self._update(X, E, g)
         return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))
 
+    def step_pairwise(self, Xp, Xn):
+        X = np.concatenate([Xp, Xn], axis=0)
+        z, E, _ = self.logits(X)
+        B = len(Xp)
+        d = z[:B] - z[B:]
+        s = sigmoid(d)
+        gp = (-(1.0 - s) / B).astype(np.float32)
+        g = np.concatenate([gp, -gp]).astype(np.float32)
+        self._update(X, E, g)
+        return float(-np.mean(np.log(s + 1e-9)))
+
     def predict(self, X, bs=25_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index 15b3ad4..5a489b4 100644
--- a/train.py
+++ b/train.py
@@ -122,12 +122,55 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
     Xtr = transform(train_rows, features)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
+
+    user_codes = {}
+    users = np.empty(len(train_rows), dtype=np.int64)
+    for i, row in enumerate(train_rows):
+        uid = row[1]
+        code = user_codes.get(uid)
+        if code is None:
+            code = len(user_codes)
+            user_codes[uid] = code
+        users[i] = code
+    n_users = len(user_codes)
+    pos_lists = [[] for _ in range(n_users)]
+    neg_lists = [[] for _ in range(n_users)]
+    for i in range(len(train_rows)):
+        u = users[i]
+        if ytr[i] == 1:
+            pos_lists[u].append(i)
+        else:
+            neg_lists[u].append(i)
+    pos_idx_list = []
+    pos_user_list = []
+    neg_flat_list = []
+    neg_start = np.zeros(n_users, dtype=np.int64)
+    neg_count = np.zeros(n_users, dtype=np.int64)
+    offset = 0
+    for u in range(n_users):
+        if len(pos_lists[u]) > 0 and len(neg_lists[u]) > 0:
+            pos_idx_list.extend(pos_lists[u])
+            pos_user_list.extend([u] * len(pos_lists[u]))
+        neg_start[u] = offset
+        neg_count[u] = len(neg_lists[u])
+        neg_flat_list.extend(neg_lists[u])
+        offset += len(neg_lists[u])
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
+        order = rng.permutation(len(pos_idx))
+        losses = []
+        for i in range(0, len(order), config['bs']):
+            sel = order[i:i + config['bs']]
+            p = pos_idx[sel]
+            u = pos_user[sel]
+            offsets = (rng.random(len(u)) * neg_count[u]).astype(np.int64)
+            n = neg_flat[neg_start[u] + offsets]
+            losses.append(model.step_pairwise(Xtr[p], Xtr[n]))
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

---

## Iteration 15: `node_015`

**Status** `success` · **Parent** `node_014` · **Commit** `7b7154b5e01f`

### Hypothesis

```text
SELECTED CHANGE
Experiment (feature-engineering subsystem, label-based out-of-fold target encoding on top of this parent's FFM + pairwise-BPR code state): add two new categorical fields encoding smoothed, out-of-fold long_view rates for video_id and author_id, growing the encoding from 7 to 9 fields. Hypothesis: the model currently learns item/author quality only through per-ID embeddings and linear weights, which are noisy for the many low-count videos; a smoothed historical long_view rate for the video and for its author gives shared, well-estimated parameters that directly separate items inside a user's candidate list, which is exactly what GAUC and nDCG@5 measure, and (being field-aware) each rate bin also gets its own embedding against user_id, tab and duration. Distinct from the closest supplied prior attempt (node_013 added label-free frequency/popularity count buckets from the same parent lineage); no supplied sibling or ancestor used label statistics, and no leakage is introduced because statistics come only from training rows and training rows are encoded with fold-held-out statistics.

Implementation:
1. features.py:
   - In fit(rows), keep everything currently computed (duration edges, user_counts, video_counts, vocabs, offsets, dim, fields) and additionally compute label statistics from training rows only, reading y = float(row[6]): prior = mean(y) over rows; alpha = 20.0; K = 5 folds with fold(i) = i % 5 (i = row position in the supplied training list).
   - Build compact index dicts vid_index {video_id -> j} and aut_index {author_id -> j} plus float32 arrays vid_n[V], vid_s[V], aut_n[A], aut_s[A] (total count and label sum) and per-fold arrays vid_nf[5, V], vid_sf[5, V], aut_nf[5, A], aut_sf[5, A]; store all of these plus prior and alpha in the returned state dict (numpy arrays, small and picklable).
   - Define enc(n, s) = (s + alpha * prior) / (n + alpha), returning prior when the id is unknown (n = s = 0). Compute the full-data per-row encodings for all training rows once and derive bin edges vid_edges = np.quantile(full_video_encodings, np.linspace(0, 1, 21)[1:-1]) and aut_edges likewise (20 balanced bins); store both in the state.
   - Change raw(row, state, fold=None) to return 9 values: the current 7 values unchanged, then 'v' + str(int(np.searchsorted(state['vid_edges'], rate_v))) and 'a' + str(int(np.searchsorted(state['aut_edges'], rate_a))), where for fold is None the rate uses the full stats (vid_n/vid_s, aut_n/aut_s) and for an integer fold f the rate uses held-out stats (vid_n[j] - vid_nf[f, j], vid_s[j] - vid_sf[f, j]; same for author). Build the vocabs loop in fit with fold = i % 5 so training-time bins define the vocab; keep vocabs = [{} for _ in range(9)], dims/offsets/dim computed exactly as now and fields = len(vocabs) (becomes 9 automatically).
   - Change transform(rows, state, folds=None) so that when folds is None (validation and inference) every row uses the full-data encodings, and when folds is an integer array of len(rows) row n uses raw(row, state, fold=int(folds[n])). Keep the input row order and the existing OOV convention vocab.get(value, len(vocab)) + offsets[i].
2. train.py: keep the train(...) signature, resume/fresh logic, pair-sampling structures, pairwise loop, evaluate call, patience/best tracking, atomic save_checkpoint and payload layout unchanged; only change the training-matrix construction to Xtr = transform(train_rows, features, folds=np.arange(len(train_rows), dtype=np.int64) % 5) while Xva = transform(valid_rows, features) stays as is (full training statistics, no validation labels used). This works identically on the fresh and resume paths because the statistics live in features_state inside the checkpoint.
3. model.py: no architectural change; only lower the FM.predict default batch size from bs=25_000 to bs=20_000 to bound the (B,F,F,k) temporary with F=9. Keep FM/Predictor/read_checkpoint/load_predictor signatures, the 'V','W','b' checkpoint names, step_pairwise, and the fields constructor argument as supplied.
4. config.py: unchanged (k=8, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0).

Cost: field pairs grow from 21 to 36 (~1.7x per-step work), so expect roughly 100-130 s versus the parent's 58 s, comfortably inside candidate_timeout_s and the remaining budget.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.669048 | 0.535877 | 0.602463 | -0.000171 | 84 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
features.py | 105 +++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 model.py    |   2 +-
 train.py    |   2 +-
 3 files changed, 95 insertions(+), 14 deletions(-)
```

```diff
diff --git a/features.py b/features.py
index 591638d..e33a42f 100644
--- a/features.py
+++ b/features.py
@@ -30,10 +30,34 @@ def count_bucket(n):
     return 'c' + str(min(15, int(np.log2(n + 1))))
 
 
-def raw(row, state):
+def _enc(n, s, prior, alpha):
+    return (s + alpha * prior) / (n + alpha)
+
+
+def raw(row, state, fold=None):
+    vid_j = state['vid_index'].get(row[2])
+    if vid_j is None:
+        vn, vs = 0.0, 0.0
+    else:
+        vn, vs = state['vid_n'][vid_j], state['vid_s'][vid_j]
+        if fold is not None:
+            vn = vn - state['vid_nf'][fold, vid_j]
+            vs = vs - state['vid_sf'][fold, vid_j]
+    aut_j = state['aut_index'].get(row[3])
+    if aut_j is None:
+        an, as_ = 0.0, 0.0
+    else:
+        an, as_ = state['aut_n'][aut_j], state['aut_s'][aut_j]
+        if fold is not None:
+            an = an - state['aut_nf'][fold, aut_j]
+            as_ = as_ - state['aut_sf'][fold, aut_j]
+    rate_v = _enc(vn, vs, state['prior'], state['alpha'])
+    rate_a = _enc(an, as_, state['prior'], state['alpha'])
     return [row[1], row[2], row[3], row[4], str(int(np.searchsorted(state['edges'], row[5]))),
             count_bucket(state['user_counts'].get(row[1], 0)),
-            count_bucket(state['video_counts'].get(row[2], 0))]
+            count_bucket(state['video_counts'].get(row[2], 0)),
+            'v' + str(int(np.searchsorted(state['vid_edges'], rate_v))),
+            'a' + str(int(np.searchsorted(state['aut_edges'], rate_a)))]
 
 
 def fit(rows):
@@ -43,22 +67,79 @@ def fit(rows):
     for row in rows:
         user_counts[row[1]] = user_counts.get(row[1], 0) + 1
         video_counts[row[2]] = video_counts.get(row[2], 0) + 1
-    base_state = dict(edges=edges, user_counts=user_counts, video_counts=video_counts)
-    vocabs = [{} for _ in range(7)]
+
+    vid_index = {}
+    aut_index = {}
     for row in rows:
-        for i, value in enumerate(raw(row, base_state)):
-            if value not in vocabs[i]:
-                vocabs[i][value] = len(vocabs[i])
+        if row[2] not in vid_index:
+            vid_index[row[2]] = len(vid_index)
+        if row[3] not in aut_index:
+            aut_index[row[3]] = len(aut_index)
+    V, A = len(vid_index), len(aut_index)
+    K = 5
+    vid_n = np.zeros(V, dtype=np.float32)
+    vid_s = np.zeros(V, dtype=np.float32)
+    aut_n = np.zeros(A, dtype=np.float32)
+    aut_s = np.zeros(A, dtype=np.float32)
+    vid_nf = np.zeros((K, V), dtype=np.float32)
+    vid_sf = np.zeros((K, V), dtype=np.float32)
+    aut_nf = np.zeros((K, A), dtype=np.float32)
+    aut_sf = np.zeros((K, A), dtype=np.float32)
+
+    y_all = np.asarray([float(r[6]) for r in rows], dtype=np.float64)
+    prior = float(y_all.mean()) if len(y_all) else 0.0
+    alpha = 20.0
+
+    for i, row in enumerate(rows):
+        y = float(row[6])
+        f = i % K
+        vj = vid_index[row[2]]
+        vid_n[vj] += 1.0
+        vid_s[vj] += y
+        vid_nf[f, vj] += 1.0
+        vid_sf[f, vj] += y
+        aj = aut_index[row[3]]
+        aut_n[aj] += 1.0
+        aut_s[aj] += y
+        aut_nf[f, aj] += 1.0
+        aut_sf[f, aj] += y
+
+    full_v = np.empty(len(rows), dtype=np.float64)
+    full_a = np.empty(len(rows), dtype=np.float64)
+    for i, row in enumerate(rows):
+        vj = vid_index[row[2]]
+        aj = aut_index[row[3]]
+        full_v[i] = _enc(vid_n[vj], vid_s[vj], prior, alpha)
+        full_a[i] = _enc(aut_n[aj], aut_s[aj], prior, alpha)
+    vid_edges = np.quantile(full_v, np.linspace(0, 1, 21)[1:-1])
+    aut_edges = np.quantile(full_a, np.linspace(0, 1, 21)[1:-1])
+
+    base_state = dict(edges=edges, user_counts=user_counts, video_counts=video_counts,
+                       vid_index=vid_index, aut_index=aut_index,
+                       vid_n=vid_n, vid_s=vid_s, aut_n=aut_n, aut_s=aut_s,
+                       vid_nf=vid_nf, vid_sf=vid_sf, aut_nf=aut_nf, aut_sf=aut_sf,
+                       prior=prior, alpha=alpha, vid_edges=vid_edges, aut_edges=aut_edges)
+
+    vocabs = [{} for _ in range(9)]
+    for i, row in enumerate(rows):
+        fold = i % K
+        for j, value in enumerate(raw(row, base_state, fold=fold)):
+            if value not in vocabs[j]:
+                vocabs[j][value] = len(vocabs[j])
     dims = [len(v) + 1 for v in vocabs]
-    return dict(edges=edges, user_counts=user_counts, video_counts=video_counts, vocabs=vocabs,
-                offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims),
-                fields=len(vocabs))
+
+    state = dict(base_state)
+    state.update(vocabs=vocabs,
+                 offsets=np.cumsum([0] + dims[:-1]).astype(np.int32), dim=sum(dims),
+                 fields=len(vocabs))
+    return state
 
 
-def transform(rows, state):
+def transform(rows, state, folds=None):
     result = np.empty((len(rows), len(state['vocabs'])), dtype=np.int32)
     for n, row in enumerate(rows):
-        for i, value in enumerate(raw(row, state)):
+        fold = None if folds is None else int(folds[n])
+        for i, value in enumerate(raw(row, state, fold=fold)):
             vocab = state['vocabs'][i]
             result[n, i] = vocab.get(value, len(vocab)) + state['offsets'][i]
     return result
diff --git a/model.py b/model.py
index 4ba09a5..9dd3551 100644
--- a/model.py
+++ b/model.py
@@ -85,7 +85,7 @@ class FM:
         self._update(X, E, g)
         return float(-np.mean(np.log(s + 1e-9)))
 
-    def predict(self, X, bs=25_000):
+    def predict(self, X, bs=20_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
 def read_checkpoint(path):
diff --git a/train.py b/train.py
index 5a489b4..91a14e3 100644
--- a/train.py
+++ b/train.py
@@ -119,7 +119,7 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
         best, bad, epoch = -1.0, 0, 0
         payload = dict(version=1, config=config, features_state=features, context=context)
         print('fresh training', flush=True)
-    Xtr = transform(train_rows, features)
+    Xtr = transform(train_rows, features, folds=np.arange(len(train_rows), dtype=np.int64) % 5)
     ytr = np.asarray([r[6] for r in train_rows], dtype=np.float32)
     Xva = transform(valid_rows, features)
```

---

## Iteration 16: `node_016`

**Status** `success` · **Parent** `node_015` · **Commit** `bf82125cb18f`

### Hypothesis

```text
SELECTED CHANGE
Change the training objective in this branch from single-negative pairwise BPR to a multi-negative, in-user sampled-softmax (listwise cross-entropy) loss, keeping the FFM backbone, the 9-field encoding (raw IDs + duration bucket + count buckets + out-of-fold target-encoded video/author rate bins), the uniform within-user negative sampler, and all train/predict/checkpoint contracts unchanged.

Hypothesis: GAUC and especially nDCG@5 are top-heavy within-user ranking metrics; a softmax over one positive against several sampled negatives from the same user supplies a much stronger, better-normalized ranking gradient per positive than a single BPR pair, sharpening the top of each user's list. This is distinct from the closest supplied prior attempts: node_014 introduced pure pairwise BPR with exactly one negative per positive (the current parent code), and node_011 on another branch added an auxiliary pointwise BCE term to a pairwise model; no supplied experiment used a multi-negative listwise/softmax objective.

Implementation:
1. model.py: keep class name FM and every existing signature/attribute exactly as supplied (__init__ with V shape (dim, fields, k), W, b, mV/vV/mW/vW, t, fields, PAIRS; logits; _update; step; step_pairwise; predict(bs=20_000); read_checkpoint; Predictor; load_predictor; checkpoint weight names 'V','W','b'). Do NOT add any new instance attributes to FM (train.py's resume path validates set(vars(model)) and np.shape/np.isfinite on every attribute). Add one new method step_listwise(self, Xp, Xn, M) where Xp has shape (B,F) and Xn has shape (M*B, F) formed as M vertically stacked blocks of B rows: X = np.concatenate([Xp, Xn], axis=0); z, E, _ = self.logits(X); build Z = np.empty((1+M, B), dtype=np.float32) with Z[0] = z[:B] and Z[1:] = z[B:].reshape(M, B); subtract Z.max(axis=0, keepdims=True) for stability; P = exp(...) normalized over axis 0; G = P.copy(); G[0] -= 1.0; G /= B; g = np.concatenate([G[0], G[1:].reshape(-1)]).astype(np.float32) (this row order matches X); call self._update(X, E, g); return float(-np.mean(np.log(P[0] + 1e-9))) as the logged loss. Leave step() and step_pairwise() in place, unused.
2. train.py: keep the train(train_rows, valid_rows, checkpoint_path, overrides, context) signature, resume/fresh logic, feature fitting, fold-based Xtr transform, pair index structures (pos_idx, pos_user, neg_flat, neg_start, neg_count), evaluate call, best/bad/patience tracking, nonfinite checks, atomic save_checkpoint and payload layout unchanged. Replace only the inner batch call: with M = config['negatives'], for each batch slice sel of the permuted positives take p = pos_idx[sel] and u = pos_user[sel], then draw M independent negative index vectors using the same sampler already present (offsets = (rng.random(len(u)) * neg_count[u]).astype(np.int64); n = neg_flat[neg_start[u] + offsets]), build Xn = np.concatenate([Xtr[n_1], ..., Xtr[n_M]], axis=0) in that block order, and append model.step_listwise(Xtr[p], Xn, M) to losses. Keep using the same rng object so resume rng capture stays exact.
3. config.py: add negatives=4 to DEFAULTS (keep k=8, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0) and include 'negatives' in the tuple of integer-validated keys in resolve() so it must be an int >= 1.
4. features.py: unchanged.

Cost: rows forwarded per step rise from 2*bs to 5*bs (40960 rows with F=9, k=8 gives a ~106 MB (B,F,F,k) temporary, acceptable), roughly 2.5x the parent's per-epoch training work; expected total ~150-250 s versus the parent's 84 s, well inside candidate_timeout_s and the remaining budget. No change to splits, the long_view target, ranking groups, or evaluation.

OBJECTIVE
Improve validation Primary = (GAUC + nDCG@5) / 2 within the remaining budget.

CONSTRAINTS
Preserve the frozen data splits, long_view target, ranking groups, GAUC and nDCG@5 evaluation, and test isolation. Do not read test data during search. Keep the train.train and model.load_predictor contracts in the supplied files. Do not modify the agent, evaluator, dataset, shared environments, or external files. Only edit the supplied files. Keep artifacts outside source. One candidate's training and validation must finish inside candidate_timeout_s; exceeding it kills the candidate and records a failure.
```

### Metrics

| GAUC | nDCG@5 | Primary | vs parent | Wall clock |
|---|---|---|---|---|
| 0.668604 | 0.535723 | 0.602164 | -0.000299 | 153 s |

### Errors and recovery

None. The candidate applied cleanly and evaluated on the first attempt.

### Code diff

```text
config.py |  4 ++--
 model.py  | 17 +++++++++++++++++
 train.py  | 11 ++++++++---
 3 files changed, 27 insertions(+), 5 deletions(-)
```

```diff
diff --git a/config.py b/config.py
index d7123ea..2e78e98 100644
--- a/config.py
+++ b/config.py
@@ -22,14 +22,14 @@ space. Settings may evolve with the model while preserving these constraints.
 # Reference implementation: replaceable while preserving the contracts above.
 import math
 
-DEFAULTS = dict(k=8, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)
+DEFAULTS = dict(k=8, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0, negatives=4)
 
 
 def resolve(overrides):
     if set(overrides) - DEFAULTS.keys():
         raise ValueError('unknown configuration keys')
     config = {**DEFAULTS, **overrides}
-    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
+    for key in ('k', 'epochs', 'bs', 'patience', 'seed', 'negatives'):
         value = config[key]
         if type(value) is not int or value < (0 if key == 'seed' else 1):
             raise ValueError(f'invalid {key}')
diff --git a/model.py b/model.py
index 9dd3551..f119daa 100644
--- a/model.py
+++ b/model.py
@@ -85,6 +85,23 @@ class FM:
         self._update(X, E, g)
         return float(-np.mean(np.log(s + 1e-9)))
 
+    def step_listwise(self, Xp, Xn, M):
+        B = len(Xp)
+        X = np.concatenate([Xp, Xn], axis=0)
+        z, E, _ = self.logits(X)
+        Z = np.empty((1 + M, B), dtype=np.float32)
+        Z[0] = z[:B]
+        Z[1:] = z[B:].reshape(M, B)
+        Z -= Z.max(axis=0, keepdims=True)
+        P = np.exp(Z)
+        P /= P.sum(axis=0, keepdims=True)
+        G = P.copy()
+        G[0] -= 1.0
+        G /= B
+        g = np.concatenate([G[0], G[1:].reshape(-1)]).astype(np.float32)
+        self._update(X, E, g)
+        return float(-np.mean(np.log(P[0] + 1e-9)))
+
     def predict(self, X, bs=20_000):
         return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])
 
diff --git a/train.py b/train.py
index 91a14e3..cac094d 100644
--- a/train.py
+++ b/train.py
@@ -164,13 +164,18 @@ def train(train_rows, valid_rows, checkpoint_path, overrides, context):
             break
         order = rng.permutation(len(pos_idx))
         losses = []
+        M = config['negatives']
         for i in range(0, len(order), config['bs']):
             sel = order[i:i + config['bs']]
             p = pos_idx[sel]
             u = pos_user[sel]
-            offsets = (rng.random(len(u)) * neg_count[u]).astype(np.int64)
-            n = neg_flat[neg_start[u] + offsets]
-            losses.append(model.step_pairwise(Xtr[p], Xtr[n]))
+            blocks = []
+            for _ in range(M):
+                offsets = (rng.random(len(u)) * neg_count[u]).astype(np.int64)
+                n = neg_flat[neg_start[u] + offsets]
+                blocks.append(Xtr[n])
+            Xn = np.concatenate(blocks, axis=0)
+            losses.append(model.step_listwise(Xtr[p], Xn, M))
         validation = evaluate([r[1] for r in valid_rows], [r[6] for r in valid_rows], model.predict(Xva))
         if validation['primary'] > best + 1e-5:
             best, bad = validation['primary'], 0
```

