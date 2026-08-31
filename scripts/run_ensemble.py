"""Run several independent searches in sequence over one shared insight archive.

Each run keeps its own tree, incumbent and genesis baseline, so architectural
choices stay uncorrelated between runs. The shared archive carries measured
evidence across them, so a later run does not spend candidates re-deriving a
dead end an earlier one already recorded. Runs are sequential by necessity: the
archive is written when a run reports and read when the next one is constructed.

    python scripts/run_ensemble.py --base-dir runs/ensemble
        --data-dir data/KuaiRand-Pure/data
        --config storage/run-ensemble.json --runs 4
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.tree import SearchConfig
from agent.orchestrator import Orchestrator, RunConfig


def summarize(index, run_dir, report):
    selected = report.get("validation_comparison", {}).get("selected") or {}
    test = report.get("final_test") or {}
    return {
        "run": index,
        "run_dir": str(run_dir),
        "stop_reason": report.get("stop_reason"),
        "iterations": report.get("completed_iterations"),
        "selected_node_id": report.get("selected_node_id"),
        "val_primary": selected.get("val_primary"),
        "test_status": test.get("status"),
        "test_primary": (test.get("scores") or {}).get("primary"),
        "llm_calls": report.get("llm_calls"),
        "global_memory": report.get("global_memory"),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-dir", required=True, help="Parent directory holding run-1..run-N")
    parser.add_argument("--data-dir", required=True, help="Raw KuaiRand-Pure CSV directory")
    parser.add_argument("--config", required=True,
                        help="JSON RunConfig overrides shared by every run; no credentials")
    parser.add_argument("--runs", type=int, default=4, help="Number of sequential runs")
    args = parser.parse_args(argv)
    if args.runs <= 0:
        parser.error("--runs must be a positive integer")
    base = Path(args.base_dir)
    with open(args.config, encoding="utf-8") as stream:
        overrides = json.load(stream)
    if not overrides.get("global_memory_path"):
        parser.error("Set global_memory_path in the config; without it the runs share nothing")

    summaries = []
    for index in range(1, args.runs + 1):
        run_dir = base / f"run-{index}"
        if run_dir.exists() and any(run_dir.iterdir()):
            # Populated directories belong to an earlier invocation; resuming one
            # is a deliberate act through main.py, not something to guess at here.
            print(f"run-{index}: skipped, {run_dir} is not empty", file=sys.stderr)
            continue
        settings = dict(overrides, run_dir=str(run_dir), data_dir=args.data_dir)
        settings["search"] = SearchConfig(**settings.get("search", {}))
        try:
            report = Orchestrator(RunConfig(**settings)).run()
        except Exception as exc:
            # A single failure must not discard the evidence the others recorded.
            print(f"run-{index}: stopped ({type(exc).__name__}); inspect {run_dir} and continue",
                  file=sys.stderr)
            continue
        summaries.append(summarize(index, run_dir, report))
        print(json.dumps(summaries[-1], indent=2))

    scored = [s for s in summaries if s["val_primary"] is not None]
    best = max(scored, key=lambda s: s["val_primary"], default=None)
    # Selection is on validation only; the test score is reported, never optimised.
    print(json.dumps({"runs_completed": len(summaries),
                      "best_by_validation": best, "summaries": summaries}, indent=2))
    if best is not None:
        payload = json.dumps({"best_by_validation": best, "summaries": summaries}, indent=2)
        (base / "ensemble.json").write_text(payload + "\n", encoding="utf-8")
    return 0 if best is not None and best["test_status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
