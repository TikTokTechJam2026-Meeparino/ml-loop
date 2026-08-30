# Recommender Workshop

**Autonomous tree-search ML research for recommender systems.**

Recommender Workshop is designed to explore, optimize, and evaluate deep ranking pipelines on the **KuaiRand-Pure** short-video recommendation benchmark. It treats experimentation as a directed acyclic state graph: each accepted node is a runnable, evaluated pipeline pinned to a Git commit, and each edge records an atomic, hypothesis-driven change.

The goal is to automate the research loop—from feature engineering and model design to execution repair and final test inference—within a fixed experiment and time budget.

> **Status: early implementation.** The LLM client and its smoke-test script are implemented, and the reference starter kit is included. The autonomous search engine and evolving training pipeline remain scaffolding. No project benchmark results are claimed.

## Research objective

Rank items within logged user impressions for the primary **`long_view`** target, improving over a fixed **Factorization Machine (FM)** reference baseline.

The project defines its primary validation objective as:

\[
\mathrm{Primary} = \frac{\mathrm{GAUC} + \mathrm{nDCG@5}}{2}
\]

| Constraint | Target |
| --- | --- |
| Dataset | KuaiRand-Pure |
| Primary prediction target | `long_view` |
| Reference model | Fixed FM baseline |
| Search budget | At most 50 candidate iterations |
| Wall-clock budget | At most 6 hours per end-to-end run |
| Convergence parameters | Improvement threshold ε = 0.002; patience N = 3 |
| Human intervention | None after configuration and launch |

The dataset release, label derivation, impression grouping, split boundaries, GAUC weighting, and nDCG eligibility rules must be fixed before experiments begin. The score above is the project's specified objective; equivalence to an official benchmark protocol remains to be verified.

## Architecture

```mermaid
flowchart TD
    A[Validate configuration and freeze data splits] --> B[Train and evaluate FM genesis node]
    B --> C{Budget available and not converged?}
    C -->|Yes| D[Select parent using UCT / best-first policy]
    D --> E[Propose one atomic hypothesis]
    E --> F[Create isolated Git workspace]
    F --> G[Patch, train, and validate]
    G -->|Execution error| H{Repair budget available?}
    H -->|Yes| I[Apply bounded repair]
    I --> G
    H -->|No| J[Record failure outside candidate graph]
    G -->|Valid evaluation| K[Commit candidate and update graph]
    J --> C
    K --> C
    C -->|No| L[Freeze best validation-selected pipeline]
    L --> M[Run final test inference and export report]
```

### Evaluated pipeline graph

Each accepted node should retain its commit hash, parent reference, hypothesis, configuration, random seeds, validation metrics, resource usage, and artifact references. Edges identify the subsystem changed and the evidence motivating that change.

Only runnable candidates with valid evaluations enter the graph. Failed attempts remain in a separate experiment ledger so that execution errors do not create invalid pipeline states. Valid candidates that underperform remain useful evidence, even when their branches are no longer expanded.

### Parent selection and pruning

A hybrid **Upper Confidence Bound for Trees (UCT) / best-first** policy balances high validation scores with exploration of less-visited branches. The search backtracks when a branch plateaus and prunes unproductive expansion paths while preserving their history.

The precise selection formula, exploration coefficient, reward normalization, and pruning rules are implementation decisions that must be recorded in the run configuration.

### Git isolation and persistent memory

Each candidate transformation runs on an ephemeral branch in an isolated workspace based on its selected parent's commit. Dataset splits remain read-only; checkpoints and other bulky artifacts live outside Git and are referenced by the experiment ledger.

Search state, failure caches, and cross-branch insights persist outside candidate workspaces. Hypothesis records should include their configuration and data context so that the agent can avoid repeating refuted experiments without incorrectly rejecting a hypothesis under materially different conditions.

### Bounded self-repair

Runtime exceptions, tensor shape mismatches, and CUDA out-of-memory errors trigger a bounded repair loop. Repairs and their outcomes are logged, and retries consume the same wall-clock budget as the rest of the run.

A candidate that exhausts its repair allowance is recorded as failed. Repair must not silently change frozen data splits, evaluation rules, or the primary target to obtain a passing run.

## Search space

| Subsystem | Candidate transformations |
| --- | --- |
| Feature engineering | Out-of-fold historical response rates, temporal features, and feature crosses |
| Model backbone | FM extensions, DeepFM, DLRM, and attention-based architectures |
| Multi-task learning | Auxiliary `click`, `like`, `comment`, and `play_time` signals supporting the `long_view` head |
| Loss formulation | Ranking-aware, listwise, and counterfactual objectives |

Each experiment should test one explicit hypothesis within a subsystem. Auxiliary labels and derived features require checks against the selected dataset schema. Counterfactual objectives require justified exposure or propensity assumptions; they should not be enabled solely because interaction logs are available.

## Evaluation and stopping protocol

1. **Freeze the benchmark.** Record the dataset version, split manifest, preprocessing rules, target definition, ranking groups, metric implementation, seeds, and hardware. Keep test data out of search decisions.
2. **Establish the reference.** Train and evaluate the fixed FM pipeline to create the genesis node. All candidates use the same evaluation protocol.
3. **Search on validation data.** Log both component metrics, Primary, the improvement over FM, execution status, and elapsed time for every evaluated candidate.
4. **Enforce all limits.** Stop when the iteration cap, wall-clock deadline, or convergence condition is reached, whichever comes first. Failed candidates count toward the iteration cap; repairs stay within their candidate's iteration and have a separate retry bound.
5. **Select and freeze.** Choose the best valid pipeline by validation Primary before accessing the test set. If no candidate improves on FM, retain the reference pipeline.
6. **Run final inference.** Export test predictions and, where labels are available, final test metrics without using them for further tuning.

**Proposed convergence interpretation:** compare the best-so-far validation Primary at the start and end of each candidate iteration. An improvement below 0.002 increments a patience counter; an improvement of at least 0.002 resets it. Stop after three consecutive below-threshold iterations. Failed attempts provide no improvement. This operational definition should be confirmed and frozen before implementation.

The six-hour budget covers initialization, baseline training, search, repairs, and final inference. The scheduler must reserve time for final inference and artifact export, and enforce timeouts on running jobs rather than checking the deadline only between experiments. If the run cannot complete, it must report that limitation explicitly.

## Planned run artifacts

- A searchable experiment ledger and pipeline graph with commit references.
- Per-candidate hypotheses, configurations, metrics, logs, and failure or repair histories.
- A persistent cache of prior hypotheses and cross-branch findings.
- The selected pipeline's configuration, checkpoint references, and test predictions.
- A final report comparing the selected pipeline with FM, documenting resource use, stopping reason, and reproducibility details.

## Implementation roadmap

- [ ] Specify and validate the KuaiRand-Pure data and metric contract.
- [ ] Implement the fixed FM baseline and reproducible evaluation harness.
- [ ] Add the experiment ledger, pipeline graph, and Git workspace lifecycle.
- [ ] Implement parent selection, hypothesis generation, backtracking, and pruning.
- [ ] Add bounded execution repair, failure caching, and resource enforcement.
- [ ] Integrate feature, backbone, multi-task, and loss transformations.
- [ ] Implement convergence checks, final selection, test inference, and reporting.
- [ ] Validate a complete autonomous run under the 50-iteration and six-hour limits.

## Getting started

### Repository and workspace layout

```text
agent/
├── __init__.py
├── llm/
│   ├── __init__.py
│   ├── client.py              # LLM calls, token accounting, retries, model selection
│   └── mock_client.py         # Mock responses for offline testing
├── engine/
│   ├── __init__.py
│   ├── mutation.py            # Candidate diffs and bounded self-repair
│   ├── parser.py              # Search/replace and unified diff parsing
│   └── prompts.py             # Prompt templates and output format rules
├── graph/
│   ├── __init__.py
│   ├── node.py                # SearchNode, EdgeAction, MetricResult
│   ├── tree.py                # Selection, pruning, serialization
│   └── memory.py              # Insights and dead-end tracking
├── sandbox/
│   ├── __init__.py
│   ├── git_driver.py          # Inner repository lifecycle
│   └── runner.py              # Training and evaluation subprocesses
└── orchestrator.py            # Search loop and resource limits
workspace_template/           # Tracked empty starting pipeline stubs
├── data.py
├── features.py
├── model.py
├── train.py
├── evaluate.py
└── submit.py
workspace/                    # Ignored independent Git repo; same pipeline filenames
storage/                      # Ignored persistent outputs; .gitkeep is tracked
├── state_tree.json
├── run_log.jsonl
└── global_insights.json
data/kuairand-pure/            # Existing data layout preserved
├── starter-kit/              # Tracked fixed reference code and English README
└── KuaiRand-Pure/data/        # Ignored raw dataset; currently empty
checkpoints/                  # Ignored weights and predictions; .gitkeep is tracked
requirements.txt              # LLM client dependencies
main.py                       # Planned CLI entry point
README.md
```

The outer repository versions the agent and starting template. The inner `workspace/` repository versions evolving candidate pipelines independently; it is not a submodule and its files are not tracked by the outer repository.

The planned initializer copies `workspace_template/` into a new workspace, initializes its Git repository, and creates a genesis scaffold commit. That commit is not an evaluated search node until the baseline has run successfully. Subsequent runs resume the existing workspace without overwriting files or resetting its history. An existing directory that is not an initialized workspace must be reported rather than silently replaced. Template updates apply only to newly initialized workspaces.

Apart from `agent/llm/client.py`, agent modules, pipeline template files, and the root CLI are currently empty scaffolding. The template's `evaluate.py` and `submit.py` will integrate the fixed scoring and submission checks from the reference kit outside the editable workspace; the agent must not evolve the benchmark scoring rules. The template contains no data, checkpoints, or Git metadata. Initialization logic is not implemented yet. Runtime storage files are ignored by the outer repository and should be initialized by the agent when needed; the current local placeholders are empty, not valid serialized JSON state.

The root research CLI is not runnable yet. A reproducible FM baseline with a frozen evaluation contract remains a pending implementation milestone.

### LLM client setup and smoke test

Use Python 3.10 or newer for the client. Install dependencies from the project root:

```powershell
python -m pip install -r requirements.txt
```

For a fresh clone, copy `.env.example` to `.env` (do not overwrite existing credentials). Set `LLM_MODEL` to your provider/model identifier and replace `<YOUR-API-KEY>` in `LLM_API_KEY`. Optionally set `LLM_API_BASE` for a custom endpoint. `.env` is Git-ignored. Existing process environment variables take precedence over the file. No default model is selected because the correct model and provider depend on your key.

The client uses [LiteLLM's provider translation](https://docs.litellm.ai/docs/completion/input). Model identifiers use provider prefixes such as `anthropic/`, `gemini/`, `openrouter/`, `openai/`, or `ollama_chat/`. For local providers without authentication, leave the key blank. Providers using cloud credentials may require additional provider-specific environment configuration.

```powershell
# Offline tests: no dependencies, credentials, network requests, or token spend.
python scripts/test_llm.py

# Live smoke test: sends a small request using your .env settings; may incur charges.
python scripts/test_llm.py --live
```

```python
from agent.llm.client import LLMClient

client = LLMClient.from_env()
result = client.complete([
    {"role": "system", "content": "Be concise."},
    {"role": "user", "content": "Suggest one ranking experiment."},
])
print(result.text)
print(result.usage)
print(client.total_usage)
```

`complete(messages)` is the single completion interface for both the real and mock clients. It accepts text chat messages and supports a per-call model and output-token limit override. Create a separate client when changing provider credentials or endpoint. This initial interface is synchronous and text-only, without streaming or tool calls.

The wrapper retries transient failures with bounded exponential backoff and jitter, but does not retry authentication or invalid-request failures. `LLM_MAX_RETRIES` counts retries after the first attempt; `LLM_TIMEOUT` is per attempt, not a global research deadline. The future orchestrator must enforce the overall run budget. Usage totals count returned provider-reported tokens only, not potentially billed failed requests; missing usage is explicitly represented by `None`. Raw provider exception messages are not included in wrapper errors.
