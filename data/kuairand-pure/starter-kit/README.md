# KuaiRand-Pure Starter Kit

English translation of the supplied starter-kit documentation, with commands adapted to this repository. Results and research guidance below are reported by the kit authors, not reproduced by Recommender Workshop.

## Dependencies

Python 3.9+ and NumPy. No PyTorch, pandas, or scikit-learn is required.

## Dataset

The dataset is **not included**. The original kit provides a download from [KuaiRand](https://kuairand.com) through Zenodo, without registration.

```text
data/kuairand-pure/
├── starter-kit/           # Reference code and this README
└── KuaiRand-Pure/
    └── data/              # Dataset CSVs after extraction
```

Run these commands in PowerShell from the project root to download and extract it:

```powershell
Set-Location data/kuairand-pure
curl.exe -L -o KuaiRand-Pure.tar.gz https://zenodo.org/records/10439422/files/KuaiRand-Pure.tar.gz
tar -xzf KuaiRand-Pure.tar.gz
Set-Location starter-kit
```

All subsequent commands run from `starter-kit/`. The scripts default to `./KuaiRand-Pure/data`; this repository layout instead requires `--data_dir ../KuaiRand-Pure/data`.

## Running a baseline

```powershell
python baseline.py --model fm --data_dir ../KuaiRand-Pure/data
```

Models: `fm` (the kit's official baseline), `pop` (item popularity), and `random` (a lower-bound sanity check). The original kit reports approximately 40 seconds for FM on a single CPU core; actual runtime depends on hardware.

**Project integration:** keep this reference code unchanged and evolve models in `workspace/`. The baseline entry point evaluates both validation and test. Autonomous search must use validation only, reserving test evaluation for the final selected pipeline. The starter scripts do not enforce that separation themselves.

## Task definition — fixed protocol

| Item | Definition |
| --- | --- |
| Task | Within-user ranking over each user's logged evaluation impressions, not full-catalog retrieval |
| Relevance | Native `long_view` column, binary 0/1 |
| Metrics | GAUC and nDCG@5; Primary is their arithmetic mean |
| Splits | Train `20220408–20220421`; valid `20220422–20220428`; test `20220429–20220508` |
| Users with no positives | nDCG is 0.0 and included in the average |
| GAUC | Only users with `0 < positive count < impression count`, weighted by positive count |
| nDCG gain | `2^rel - 1`, equivalent to identity for binary labels |

The implementation and protocol comments are in `evaluate.py`. **Do not change the reference scoring rules.**

## Baseline scores

Reported test scores. **FM is the baseline to beat.**

| Model | GAUC | nDCG@5 | Primary |
| --- | --- | --- | --- |
| Random | 0.4996 | 0.4511 | 0.4753 |
| Item popularity | 0.6308 | 0.5121 | 0.5715 |
| **FM** | **0.6610** | **0.5282** | **0.5946** |

### Metric ceilings

Among the kit's reported 23,875 test users:

| Group | Share | Effect |
| --- | --- | --- |
| All negative | 27.1% | nDCG always 0; excluded from GAUC |
| All positive | 9.2% | nDCG always 1; excluded from GAUC |
| Mixed labels | 63.7% | Contribute to GAUC |

Even oracle predictions using true labels cannot achieve nDCG@5 of 1.0:

| Metric | Random | FM | Oracle ceiling | Random-to-oracle range covered by FM |
| --- | --- | --- | --- | --- |
| GAUC | 0.4996 | 0.6610 | 1.0000 | 32.3% |
| nDCG@5 | 0.4511 | 0.5282 | 0.7289 | 27.8% |
| Primary | 0.4753 | 0.5946 | 0.8645 | 30.7% |

Assess progress relative to the oracle ceiling. FM covers roughly 30% of the available random-to-oracle range; remaining Primary headroom is about 0.27, not 0.41.

The kit reports standard deviations of **0.0008** for FM's test metrics over five seeds. Its convergence rule is **epsilon = 0.002 (approximately 2.5 standard deviations), N = 3**: convergence occurs after three consecutive iterations with validation Primary improvement not exceeding 0.002.

Sanity check: the original kit expects random-model **test** Primary near 0.475 ± 0.001. Investigate the data and evaluation setup if it differs. The reported random validation Primary is 0.4834.

## Submission format

CSV with a header and one row per evaluation row:

```csv
row_id,user_id,video_id,score
0,0,7531,-3.34176
1,0,4214,-1.4955
```

| Field | Meaning |
| --- | --- |
| `row_id` | Consecutive index starting at zero, matching `data.load(data_dir)[split]` order |
| `user_id`, `video_id` | Redundant identifiers for alignment checks |
| `score` | Finite real-valued prediction; only relative ordering matters. NaN and infinity are forbidden |

Deterministic row order: read `log_standard_4_08_to_4_21_pure.csv`, then `log_standard_4_22_to_5_08_pure.csv`, filter by date, and preserve original file order.

**`row_id` is necessary:** `(user_id, video_id)` is not unique. The kit reports 3.06% duplicate pairs in test, with some repeated up to 12 times.

Generate and check a test submission using the reference FM:

```powershell
python submit.py --make --split test --data_dir ../KuaiRand-Pure/data submission.csv
python submit.py --check --split test --data_dir ../KuaiRand-Pure/data submission.csv
```

For validation scoring, create a separate file aligned with validation rows:

```powershell
python submit.py --make --split valid --data_dir ../KuaiRand-Pure/data validation_submission.csv
python submit.py --score --split valid --data_dir ../KuaiRand-Pure/data validation_submission.csv
```

`--check` rejects incorrect headers, row counts, skipped row IDs, misaligned user/video IDs, and nonnumeric or nonfinite scores. **Check submissions before submitting.** Project runs should direct generated files outside this reference directory.

## Where to experiment

The following findings and priorities come from the supplied kit authors.

### Tested changes without gains

| Experiment | Reported result |
| --- | --- |
| Add all 13 CWM static feature fields, including `music_id`, `video_type`, `upload_type`, and six coarse user buckets | Primary 0.5940 versus 0.5950 for five fields; no improvement beyond noise |
| Embedding dimensions k = 8 / 16 / 32 | Primary 0.5895 / 0.5902 / 0.5887; little change |

The authors interpret this as evidence that `user_id × video_id` interactions capture much of the learnable signal. Coarse buckets such as `follow_user_num_range` may be redundant with user ID, and approximately 1.14 million training rows may not support more capacity. In these experiments, static features and capacity were not the bottleneck.

A user-only additive first-order term is constant within a user's group and cannot change its ranking. User features can help through interactions with item features. The kit also reports identical ranking metrics for its tested user-bias-scaled item-popularity variant and plain item popularity.

### Directions not tested by the kit authors

In their suggested priority order:

1. **Ranking losses:** replace pointwise log loss with pairwise BPR or a listwise objective, such as softmax over a user's impressions, to align training with the metrics.
2. **User history sequences:** the baseline does not use behavior sequences. The kit describes hundreds to thousands of training interactions per user and suggests DIN/SIM-style interest modeling.
3. **Multi-task learning:** auxiliary signals include `is_click`, `is_like`, `is_follow`, `is_comment`, `is_forward`, and `play_time_ms`, supporting `long_view`.
4. **Watch-time modeling:** the kit references [CWM](https://github.com/hyz20/CWM) for censored regression. When a video ends, desired watch time may be censored, motivating a one-sided loss rather than squared error.
5. **Alternative models:** DeepFM, DCN, or xDeepFM, after directions 1–4 because capacity changes did not help in the reported experiments.
6. **Temporal features and drift:** explore `hourmin`, `date`, and distribution changes between training and test periods.
7. **Random-exposure validation:** the kit describes `log_random_4_22_to_5_08_pure.csv` as approximately 1.18 million random-exposure rows for diagnosing overfitting to biased traffic. Any use must respect the project's frozen splits and test isolation.

## Using your own model

`evaluate.py` is model-independent and takes three equally sized arrays:

```python
from evaluate import evaluate

print(evaluate(user_ids, labels, scores))
```

- `user_ids`: user ID for each evaluation row.
- `labels`: native binary `long_view` labels.
- `scores`: model predictions in exactly the same row order.

You may replace `baseline.py` with PyTorch, LightGBM, or another implementation and pass its predictions to the same evaluator. **The reference evaluator determines the scoring protocol.**

The original kit cautions that its referenced CWM code depends on `torch==1.6.0`, may be difficult to install on newer GPUs, optimizes counterfactual watch time, and uses a reconstructed `long_view2` label. It recommends CWM as an advanced research reference rather than a starting implementation. These are the kit's compatibility notes, not a fresh audit of CWM.

## Files

| File | Purpose |
| --- | --- |
| `evaluate.py` | Metrics and fixed protocol; preserve unchanged |
| `data.py` | Loading, fixed splits, and feature encoding; reference for editable pipeline features |
| `baseline.py` | Random, popularity, and FM baselines |
| `baseline_scores.json` | Supplied scores, seed variability, and convergence parameters |
| `submit.py` | Submission generation, validation, and scoring |
| `ablation_features.py` | Feature ablations for the reported static-feature experiment |

Only this README is translated and adapted. Python files and the score JSON are preserved byte-for-byte from the supplied local starter kit.
