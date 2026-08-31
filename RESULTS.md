# Final submission and results summary

**Benchmark:** KuaiRand-Pure · target `long_view` · within-user ranking over logged impressions
**Primary metric:** `(GAUC + nDCG@5) / 2`

The submitted pipeline is the validation-best model of run-1, selected on validation only. The
test split was scored once, after selection, and never used to choose between candidates or runs.

---

## 1. Submitted model output

| Artifact | Location | Detail |
|---|---|---|
| Test predictions | `submission-run1.csv` | 170,588 rows, kit schema `row_id,user_id,video_id,score` |
| Validation predictions | `submission-run1-valid.csv` | 124,909 rows, same schema |
| Trained checkpoint | `storage/ensemble-001/run-1/checkpoints/ef1e57fd21914fb5beda2ed5217cf637.pkl` | 75,001,105 bytes |
| Checkpoint SHA-256 | `88533b2e6ac9603131b1b58e812d3e2403417f95e510ae417c97d928deeb3bc1` | recorded by the run, re-verified |
| Selected pipeline source | candidate workspace commit `52a281a3146b4b40cc5f2c9f11a8d7c22b164b9f` | `config.py`, `features.py`, `model.py`, `train.py`, `requirements.txt` |
| Node | `node_021` of run `e1d10ad213b54f9d88b0c672f47e168f` | iteration 21 of 22 |

Both CSVs were validated and scored by the starter kit itself, not by our own evaluator:

```
python submit.py --score submission-run1.csv       --data_dir ../KuaiRand-Pure/data
  格式与对齐校验通过：170,588 行，split=test
  GAUC 0.6655 | nDCG@5 0.5314 | primary 0.5985

python submit.py --score submission-run1-valid.csv --data_dir ../KuaiRand-Pure/data --split valid
  格式与对齐校验通过：124,909 行，split=valid
  GAUC 0.6726 | nDCG@5 0.5379 | primary 0.6053
```

Both reproduce the run's own reported metrics, which confirms the predictions are aligned to the
kit's row order rather than to any ordering of ours.

---

## 2. Results table

Official baseline is `fm_official` from the kit's `baseline_scores.json`. Deltas are absolute.

### Validation (the split selection used)

| Metric | `fm_official` | This submission | Absolute delta |
|---|---|---|---|
| GAUC | 0.6674 | **0.672574** | **+0.005174** |
| nDCG@5 | 0.5357 | **0.537937** | **+0.002237** |
| Primary | 0.6016 | **0.605256** | **+0.003656** |

### Held-out test

| Metric | `fm_official` | This submission | Absolute delta |
|---|---|---|---|
| GAUC | 0.6610 | **0.665500** | **+0.004500** |
| nDCG@5 | 0.5282 | **0.531409** | **+0.003209** |
| Primary | 0.5946 | **0.598454** | **+0.003854** |

The kit reports a standard deviation of 0.0008 over five seeds for `fm_official`'s test metrics,
so the test Primary delta is **4.8 standard deviations** above the baseline.

For scale, the kit's other reference points on test Primary: random 0.4753, item popularity 0.5715,
`fm_official` 0.5946, oracle ceiling 0.8645. The improvement closes **1.4%** of the gap between the
official baseline and the oracle ceiling.

### What the model is

A factorization machine, reached from the supplied reference pipeline through 21 accepted changes.
The productive lineage was a within-user pairwise ranking objective, then leakage-safe prior-date
and frequency features, then score-space model averaging, then a temperature-scaled sampled-softmax
loss. Full per-iteration hypotheses and diffs are in `storage/ensemble-001/run-1/RUN_LOG.md`.

---

## 3. Resource usage

Measured for run-1, the run that produced the submitted model.

| Resource | Value |
|---|---|
| Iterations used | **22 of 50** |
| Total LLM calls | 57 |
| **Total tokens (input + output)** | **1,170,743** |
| **Agent wall clock** | **87.1 minutes (1.45 h)** |
| **GPU-hours** | **0** — CPU only, no GPU at any point |
| Manual interventions | 2 (both resumes after provider outages; no model edits) |

Token accounting is complete rather than estimated: every one of the 57 calls returned provider
usage, so `responses_without_usage` is 0 and the figure is the exact sum of reported input and
output tokens.

### Note on "converged"

Two readings of convergence give very different numbers, so both are reported.

**The kit's rule** (`epsilon = 0.002`, `N = 3`: three consecutive iterations whose validation
Primary improvement does not exceed 0.002) fires at **iteration 3** of this run, because no single
candidate ever improved validation Primary by more than 0.002. Resources to that point:

| Resource | At kit convergence (iteration 3) |
|---|---|
| Iterations | 3 |
| LLM calls | 8 |
| Tokens | 93,165 |
| Wall clock | 6.3 minutes |
| Validation Primary | 0.602674 (`node_002`) |

**The run's own stopping** was `time_budget`: it exhausted its wall-clock allowance at iteration 22
while still improving, and produced a model 0.002582 better on validation than the kit's
convergence point would have accepted.

The honest summary is that the full 87 minutes bought the difference between validation Primary
0.602674 and 0.605256. On held-out test that difference did not reliably transfer; see the
limitation below.

---

## 4. Bonus benchmarks

**Not attempted.** KuaiRand-1k and KuaiRand-27k were not downloaded, evaluated, or submitted. No
bonus scoring should be expected.

The agent is dataset-agnostic in principle — the loader, evaluator, and row contract are supplied
per benchmark and the search does not assume KuaiRand-Pure's scale. Attempting them would require
the larger archives, a per-benchmark reference pipeline and evaluator, and a fresh run each; the
evaluation-protocol fingerprint would keep their experiment evidence separate from Pure's
automatically.

---

## 5. Limitation the judges should weigh

Six independent searches on this benchmark (four in the shared-memory ensemble, two earlier
development runs) produced validation Primary between 0.603619 and 0.605256 and test Primary
between 0.597210 and 0.598544. Ranking those runs by validation does **not** reproduce their order
on test: the rank correlation is 0.60 over six observations, and the run with the highest
validation score placed second on test.

The entire test spread across all six is 0.001334, about 1.7 standard deviations of the kit's
reported variation. A single change repeated across three different trees — the within-user
pairwise ranking objective — produced validation Primary of 0.601870, 0.602674 and 0.603598, a
0.0017 range that is wider than most of the differences the search promotes on.

We therefore report a reproducible improvement of roughly +0.004 test Primary over the official
baseline, found autonomously from six different architectural directions, and we do not claim that
the specific submitted run is better than the other five. Selection stayed on validation because
choosing among runs by test score would invalidate the held-out evaluation.

---

## Reproducing this summary

```powershell
# Submission files
.\.venv\Scripts\python.exe scripts\make_submission.py --run-dir storage\ensemble-001\run-1 `
    --data-dir data\kuairand-pure\KuaiRand-Pure\data --split test  --out submission-run1.csv
.\.venv\Scripts\python.exe scripts\make_submission.py --run-dir storage\ensemble-001\run-1 `
    --data-dir data\kuairand-pure\KuaiRand-Pure\data --split valid --out submission-run1-valid.csv

# Per-iteration log
.\.venv\Scripts\python.exe scripts\make_run_log.py --base-dir storage\ensemble-001

# Merged event timeline
.\.venv\Scripts\python.exe scripts\collate_events.py --base-dir storage\ensemble-001
```

Resource figures come from `storage/ensemble-001/run-1/report.json`
(`llm_calls`, `reported_tokens`, `elapsed_s`, `completed_iterations`).
