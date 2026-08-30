"""Launch or resume a sequential autonomous recommendation experiment run."""

import argparse
import json
import sys

from agent.graph.tree import SearchConfig
from agent.orchestrator import Orchestrator, RunConfig


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="Dedicated run output directory")
    parser.add_argument("--resume", action="store_true", help="Resume saved configuration and state")
    parser.add_argument("--data-dir", help="Raw KuaiRand-Pure CSV directory (new runs)")
    parser.add_argument("--config", help="JSON RunConfig overrides for a new run; no credentials")
    args = parser.parse_args(argv)
    if args.resume and (args.data_dir or args.config):
        parser.error("--resume uses saved settings; omit --data-dir and --config")
    try:
        if args.resume:
            report = Orchestrator.resume(args.run_dir)
        else:
            raw = {}
            if args.config:
                with open(args.config, encoding="utf-8") as stream:
                    raw = json.load(stream)
            raw["run_dir"] = args.run_dir
            if args.data_dir:
                raw["data_dir"] = args.data_dir
            raw["search"] = SearchConfig(**raw.get("search", {}))
            report = Orchestrator(RunConfig(**raw)).run()
        print(json.dumps({"stop_reason": report["stop_reason"],
                          "selected_node_id": report["selected_node_id"],
                          "final_test": report["final_test"]["status"]}, indent=2))
        return 0 if report["final_test"]["status"] == "success" else 2
    except Exception as exc:
        from agent.log import RunLogger
        from pathlib import Path
        artifact = RunLogger(Path(args.run_dir) / "events.jsonl").exception("cli.failed", exc, component="cli")
        if artifact:
            print(f"Error diagnostics: {artifact}", file=sys.stderr)
        # Avoid printing provider messages or diagnostic text containing secrets.
        print(f"Run stopped ({type(exc).__name__}); inspect the run state and local logs before resuming.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
