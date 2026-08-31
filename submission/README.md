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
| `checkpoint.pkl` | 71.5 MB | The trained model, byte-identical to the run's own artifact. |
| `pipeline/` | 29 KB | The five editable pipeline files exactly as the selected model left them. |
| `logs/` | 5.3 MB | Per-iteration run logs and raw event logs for all four runs. |
| `SHA256SUMS.txt` | — | Checksums for every file above. |

## Run and iteration logs

`logs/run-N/` holds two views of each of the four runs in the sequence:

| File | What it is |
|---|---|
| `RUN_LOG.md` | The per-iteration log. One section per candidate with the hypothesis the agent formed and why, the diff that implemented it, the resulting GAUC / nDCG@5 / Primary, and any error or recovery event with how it was handled. Opens with the run summary and its manual-intervention count. |
| `events.jsonl` | The raw event stream the orchestrator and runner wrote as the run executed. One JSON object per line. |

`logs/events-merged.jsonl` interleaves all seven event logs — the four runs plus three runs
abandoned to a provider outage — into one chronological timeline. Each record keeps its original
fields and gains a `collation` object naming its source directory and line, so any record traces
back. This is the view that shows the outage cascade as a single sequence rather than as four
unrelated failures.

Run-1 is the run that produced the submitted model. Its log records 2 manual interventions, both
resumes after provider outages; runs 2, 3 and 4 record 0 each.

These logs carry no prompts, provider responses, or credentials. Full request and response bodies
are written to separate per-run `diagnostics/` artifacts that stay local; the event stream only
references them by path. Those paths are absolute and therefore disclose the local working
directory of the machine that ran the search.

## The checkpoint

`checkpoint.pkl` is a copy of
`storage/ensemble-001/run-1/checkpoints/ef1e57fd21914fb5beda2ed5217cf637.pkl`, 75,001,105 bytes,
SHA-256 `88533b2e6ac9603131b1b58e812d3e2403417f95e510ae417c97d928deeb3bc1`. That hash was recorded
by the run when it wrote the file and re-verified on copy, so this is provably the model that
produced the scores above rather than a retrained approximation.

It is committed as an ordinary Git object rather than through Git LFS, so a plain `git clone`
yields the real file. LFS would keep the repository smaller but hands a pointer stub to anyone
cloning without `git lfs` installed, and its free bandwidth tier can stop serving the file
entirely once exhausted.

The model is also reproducible without it: `config.py` fixes `seed=0`, so retraining `pipeline/`
on the frozen splits regenerates the same weights.

**Loading it executes code.** It is a Python pickle, so unpickle it only if you trust this
repository as its origin.

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
