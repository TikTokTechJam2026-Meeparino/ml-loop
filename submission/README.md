# Submission package — KuaiRand-Pure

Final model output for the required benchmark. Scores and resource figures are in
[`../RESULTS.md`](../RESULTS.md); the per-iteration log is at
`storage/ensemble-001/run-1/RUN_LOG.md`.

**Model identity:** `node_021` of run `e1d10ad213b54f9d88b0c672f47e168f`,
candidate workspace commit `52a281a3146b4b40cc5f2c9f11a8d7c22b164b9f`.

## Contents

| File | Size | What it is |
|---|---|---|
| `submission-test.csv` | 4.3 MB | **The scored output.** 170,588 test-split rows in the kit schema `row_id,user_id,video_id,score`. Test is the split the kit reports baselines on and the one FM must be beaten on. |
| `submission-valid.csv` | 3.1 MB | Same model on the validation split, 124,909 rows. Supporting evidence only. Validation is the split the search was permitted to use while selecting candidates; test was held back for the selected pipeline alone. |
| `pipeline/` | 29 KB | The five editable pipeline files exactly as the selected model left them. |
| `SHA256SUMS.txt` | — | Checksums for every file above. |

## Not included: the trained checkpoint

`storage/ensemble-001/run-1/checkpoints/ef1e57fd21914fb5beda2ed5217cf637.pkl` — 75,001,105 bytes,
SHA-256 `88533b2e6ac9603131b1b58e812d3e2403417f95e510ae417c97d928deeb3bc1`.

It is left out because at 71.5 MB it exceeds GitHub's 50 MB warning threshold and would need Git
LFS, and because it is reproducible: `config.py` fixes `seed=0`, so retraining `pipeline/` on the
frozen splits regenerates the same model. Copy it in if the submission accepts large attachments:

```powershell
Copy-Item storage\ensemble-001\run-1\checkpoints\ef1e57fd21914fb5beda2ed5217cf637.pkl `
          submission\checkpoint.pkl
```

The checkpoint is a Python pickle. Loading one executes code, so it should only be opened by
someone who trusts its origin.

## Verifying this package

Both CSVs were produced from the run's stored predictions and aligned using the starter kit's own
`data.load()`, then checked by the kit itself:

```bash
cd data/kuairand-pure/starter-kit
python submit.py --check ../../../submission/submission-test.csv  --data_dir ../KuaiRand-Pure/data
python submit.py --score ../../../submission/submission-test.csv  --data_dir ../KuaiRand-Pure/data
python submit.py --check ../../../submission/submission-valid.csv --data_dir ../KuaiRand-Pure/data --split valid
python submit.py --score ../../../submission/submission-valid.csv --data_dir ../KuaiRand-Pure/data --split valid
```

Expected:

```
test    GAUC 0.6655 | nDCG@5 0.5314 | primary 0.5985
valid   GAUC 0.6726 | nDCG@5 0.5379 | primary 0.6053
```

Both reproduce the run's own reported metrics, which confirms row alignment came from the kit's
loader rather than from ours.

Checksums:

```bash
cd submission && sha256sum -c SHA256SUMS.txt
```

## Regenerating

```powershell
.\.venv\Scripts\python.exe scripts\make_submission.py --run-dir storage\ensemble-001\run-1 `
    --data-dir data\kuairand-pure\KuaiRand-Pure\data --split test  --out submission\submission-test.csv
.\.venv\Scripts\python.exe scripts\make_submission.py --run-dir storage\ensemble-001\run-1 `
    --data-dir data\kuairand-pure\KuaiRand-Pure\data --split valid --out submission\submission-valid.csv
```
