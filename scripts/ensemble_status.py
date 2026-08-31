"""Print live per-node progress for a sequential ensemble, without disturbing it.

Reads each run's published snapshot pointer, so it only ever sees a completely
written generation. Safe to run while the ensemble is executing.

    python scripts/ensemble_status.py --base-dir storage/ensemble-001
"""

import argparse
import datetime
import json
import sys
from pathlib import Path


def elapsed(run_dir):
    events = run_dir / "events.jsonl"
    if not events.exists():
        return None
    first = last = None
    with events.open(encoding="utf-8") as stream:
        for line in stream:
            try:
                record = json.loads(line)
            except ValueError:
                continue  # A partially flushed final line is not an error here.
            first = first or record
            last = record
    if first is None:
        return None
    return (datetime.datetime.fromisoformat(last["timestamp"])
            - datetime.datetime.fromisoformat(first["timestamp"])).total_seconds()


def show(run_dir):
    pointer = run_dir / "current.json"
    if not pointer.exists():
        print(f"{run_dir.name}: not started")
        return
    generation = json.loads(pointer.read_text(encoding="utf-8"))["generation"]
    tree = json.loads((run_dir / "snapshots" / generation / "tree.json").read_text(encoding="utf-8"))
    raw = tree["nodes"]
    nodes = raw if isinstance(raw, list) else list(raw.values())
    report = run_dir / "report.json"
    seconds = elapsed(run_dir)
    state = "done" if report.exists() else "running"
    header = f"{run_dir.name} [{state}]"
    if seconds is not None:
        header += f" {seconds / 60:.1f} min"
    print(header)
    best = None
    for node in nodes:
        metrics = node.get("metrics") or {}
        edge = node.get("incoming_edge") or {}
        primary = metrics.get("val_primary")
        if primary is not None and (best is None or primary > best[1]):
            best = (node["node_id"], primary)
        summary = " ".join((edge.get("hypothesis") or "genesis baseline").split())
        print("  %-10s %-9s %9s %6s  %s" % (
            node["node_id"], node["status"],
            "-" if primary is None else f"{primary:.6f}",
            "-" if not metrics.get("wall_clock_s") else f"{metrics['wall_clock_s']:.0f}s",
            summary[:88]))
    if best is not None:
        print(f"  best so far: {best[0]} at {best[1]:.6f}")
    if report.exists():
        payload = json.loads(report.read_text(encoding="utf-8"))
        test = payload.get("final_test") or {}
        print(f"  stop_reason={payload.get('stop_reason')} selected={payload.get('selected_node_id')} "
              f"test={(test.get('scores') or {}).get('primary')} "
              f"memory={json.dumps(payload.get('global_memory'))}")
    print()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-dir", required=True, help="Ensemble base directory")
    args = parser.parse_args(argv)
    base = Path(args.base_dir)
    directories = sorted(d for d in base.glob("run-*") if d.is_dir())
    if not directories:
        print(f"No run directories under {base}", file=sys.stderr)
        return 1
    for run_dir in directories:
        show(run_dir)
    archive = Path("storage/global_insights.json")
    if archive.exists():
        insights = json.loads(archive.read_text(encoding="utf-8"))["insights"]
        runs = {i["context"]["run_id"] for i in insights}
        print(f"shared archive: {len(insights)} insights from {len(runs)} run(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
