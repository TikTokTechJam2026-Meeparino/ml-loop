# Recommender Workshop

## Inspiration

Improving recommendation systems involves a repetitive loop of forming hypotheses, editing models, training, evaluating, and fixing failures. We wanted to explore whether an AI agent could automate this process while still following a reproducible and scientifically valid evaluation protocol.

## What it does

Recommender Workshop autonomously improves recommendation models for the KuaiRand-Pure short-video dataset. It starts with a Factorization Machine baseline, proposes changes, edits and trains candidate pipelines, evaluates them using GAUC and nDCG@5, and selects the best-performing model.

$$
\text{Primary Score} = \frac{\mathrm{GAUC} + \mathrm{nDCG@5}}{2}
$$

It also records experiment history, repairs failed implementations, and keeps test data isolated until final evaluation. Searches share a persistent evidence archive, so a later run starts already knowing which approaches earlier runs measured and what those measurements were.

## Results

Held-out test split. Validation selected the model; test was scored once, after selection, using the starter kit's own scorer.

| Metric | Official FM baseline | Ours | Delta |
| --- | --- | --- | --- |
| GAUC | 0.6610 | 0.665500 | +0.004500 |
| nDCG@5 | 0.5282 | 0.531409 | +0.003209 |
| **Primary** | **0.5946** | **0.598454** | **+0.003854** |

The kit reports a standard deviation of 0.0008 across five seeds, so the Primary gain is **4.8 standard deviations** above the baseline.

**What it cost to get there:**

These figures cover **the full run-1 search that produced the submitted model**.
The six-search comparison discussed below is a separate reproducibility
analysis; its resource usage is not included in this table.

| | |
| --- | --- |
| Iterations | 22 of 50 |
| LLM calls | 57 |
| Tokens (input + output) | 1,170,743 |
| Wall clock | 87 minutes |
| GPU-hours | **0** — CPU only |
| Manual interventions | 2, both resumes after provider outages; no human edits to any model |

The winning pipeline reached that score through a within-user pairwise ranking objective, leakage-safe prior-date and frequency features, score-space model averaging, and a temperature-scaled sampled-softmax loss — none of which we specified.

## How we built it

We developed and debugged the project in **Visual Studio Code**, using
**PowerShell**, terminal tools, Git CLI, and Python virtual environments to
launch runs, inspect failures, and reproduce candidate environments.

The implementation uses:

- NumPy for data processing and model training
- Anthropic Claude Opus and Claude Sonnet for the submitted search run, routed
  through LiteLLM's provider-normalized completion API. Opus handled
  high-reasoning experiment proposals, while Sonnet handled code mutation,
  repair, and reflection
- Git for versioning and isolating experiments
- KuaiRand-Pure and its official evaluation tools
- JSON and JSONL for checkpoints, logs, and reports

An orchestrator manages hypothesis generation, code modification, training, evaluation, recovery, and model selection within fixed time and iteration budgets. Every candidate runs on an ephemeral Git branch from its selected parent's commit, so each evaluated pipeline keeps an exact, reproducible source revision.

## Challenges we ran into

- Model edits frequently missed the exact-match patch format the applier requires, and retries repeated the original request because the model never saw its own rejected output or the parser's error.
- Edits also failed when they carried multiple replacements for one file, or when Windows CRLF line endings meant the file on disk was not byte-identical to the file the model had been shown. The parser was correct every time; the working copy was wrong.
- The agent initially focused too heavily on similar feature-engineering ideas, so we adjusted its prompts to encourage exploration across model architectures, losses, and multi-task learning.
- Tiny validation gains sometimes promoted much slower models, which consumed the remaining search budget without meaningful improvement. The objective has no compute term, so a change worth +0.00005 could lock a twenty-fold training cost into every descendant.
- A transient provider outage ended four queued runs in under three minutes, because our sequence driver treated a provider failure as specific to one run and immediately started the next.

## Accomplishments that we're proud of

We created an integrated autonomous ML workflow that can propose experiments, modify code, train models, recover from failures, and learn from previous results. We are especially proud of its reproducible Git-backed experiment history and safeguards against validation and test leakage.

It also reached a real improvement cheaply: 87 minutes, no GPU, and two operator restarts that touched nothing but the pause button.

## What we learned

Autonomous ML research requires more than good prompts. It also needs reliable execution, strict evaluation rules, persistent memory, budget management, and detailed failure tracking. Failed experiments are valuable when their context and results are properly recorded.

The result we did not expect concerns the selection signal itself. Across six independent searches, validation differences of the size this search routinely acts on did **not** order runs the way held-out test did: the rank correlation was 0.60 over six runs, and the run with the best validation score placed second on test. Repeating one identical change across three different search trees moved validation Primary by 0.0017 — wider than most of the gaps the search was promoting on.

So the agent reliably finds roughly +0.004 test Primary over the baseline, then resolves below the precision of its own selection signal. Knowing where that floor sits turned out to matter more than any single score, and it is the reason we report these six runs as one result measured six times rather than as a leaderboard.

## Team contributions

Isaac Ng, Timothy Lee, and Sean Ng contributed equally to the project.

## Built With

python · numpy · litellm · git · claude · codex · jsonl · kuairand
