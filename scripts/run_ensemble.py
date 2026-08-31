"""Run several independent searches in sequence over one shared insight archive.

Each run keeps its own tree, incumbent and genesis baseline, so architectural
choices stay uncorrelated between runs. The shared archive carries measured
evidence across them, so a later run does not spend candidates re-deriving a
dead end an earlier one already recorded. Runs are sequential by necessity: the
archive is written when a run reports and read when the next one is constructed.

Re-invoking the same command continues where an earlier invocation stopped:
completed runs are reported from their existing report.json, and a run left
paused by a provider outage or an interrupt is resumed with its saved settings.

    python scripts/run_ensemble.py --base-dir storage/ensemble-001
        --data-dir data/kuairand-pure/KuaiRand-Pure/data
        --config storage/run-ensemble.json --runs 4

Exit codes: 0 the best run finished its final test, 2 no run did, 3 the provider
was unavailable and the sequence stopped early.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.tree import SearchConfig
from agent.llm.client import LLMError
from agent.orchestrator import Orchestrator, RunConfig


def execute(run_dir, overrides, data_dir):
    """Report a finished run, resume a paused one, or start a fresh one."""
    report = run_dir / "report.json"
    if report.exists():
        return "completed", json.loads(report.read_text(encoding="utf-8"))
    if (run_dir / "current.json").exists():
        # Saved settings own the configuration; the deadline keeps running.
        return "resumed", Orchestrator.resume(str(run_dir))
    if run_dir.exists() and any(p.name != "run.lock" for p in run_dir.iterdir()):
        raise ValueError("Run directory is populated but has no snapshot to resume")
    settings = dict(overrides, run_dir=str(run_dir), data_dir=data_dir)
    settings["search"] = SearchConfig(**settings.get("search", {}))
    return "started", Orchestrator(RunConfig(**settings)).run()


def summarize(index, run_dir, action, report):
    selected = report.get("validation_comparison", {}).get("selected") or {}
    test = report.get("final_test") or {}
    return {
        "run": index,
        "action": action,
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


def finish(base, summaries, code):
    scored = [s for s in summaries if s["val_primary"] is not None]
    best = max(scored, key=lambda s: s["val_primary"], default=None)
    # Selection is on validation only; test scores are reported, never optimised.
    result = {"runs_completed": len(summaries), "best_by_validation": best,
              "summaries": summaries}
    print(json.dumps(result, indent=2))
    if summaries:
        base.mkdir(parents=True, exist_ok=True)
        (base / "ensemble.json").write_text(json.dumps(result, indent=2) + "\n",
                                            encoding="utf-8")
    if code is not None:
        return code
    return 0 if best is not None and best["test_status"] == "success" else 2


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
        try:
            action, report = execute(run_dir, overrides, args.data_dir)
        except LLMError as exc:
            # A provider outage is not specific to this run: every later run would
            # fail its first proposal the same way, turning one outage into a row
            # of dead runs. Stop instead; each paused run resumes on re-invocation.
            print(f"run-{index}: provider unavailable ({type(exc).__name__}). Sequence "
                  f"stopped with {len(summaries)} run(s) finished; re-run this command "
                  f"once the provider recovers to resume.", file=sys.stderr)
            return finish(base, summaries, 3)
        except Exception as exc:
            # A run-specific failure leaves the others worth attempting.
            print(f"run-{index}: stopped ({type(exc).__name__}); inspect {run_dir} "
                  f"and continue", file=sys.stderr)
            continue
        summaries.append(summarize(index, run_dir, action, report))
        print(json.dumps(summaries[-1], indent=2))
    return finish(base, summaries, None)


if __name__ == "__main__":
    raise SystemExit(main())
