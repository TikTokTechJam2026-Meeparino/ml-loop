"""Merge the event logs under a run directory into one chronological JSONL file.

Each run writes its own events.jsonl. A sequence of runs therefore leaves the
timeline split across directories, which makes it awkward to read the whole
search as one narrative or to hand over a single log artifact.

Every record keeps its original fields untouched and gains a "collation" object
naming the source directory and the line it came from, so a merged record can
always be traced back. Records are ordered by timestamp, with ties broken by
source and original line number so that same-instant events keep their order.

Unparsable lines are preserved rather than dropped: they are emitted with the
original text under "raw_line" and counted in the summary.

    python scripts/collate_events.py --base-dir storage/ensemble-001
        --out storage/ensemble-001/events-merged.jsonl
"""

import argparse
import collections
import datetime
import json
import sys
from pathlib import Path


def read(path, source):
    """Yield (sort_key, record) for one log, preserving unparsable lines."""
    for number, line in enumerate(path.open(encoding="utf-8"), start=1):
        line = line.strip()
        if not line:
            continue
        collation = {"source": source, "line": number}
        try:
            record = json.loads(line)
        except ValueError:
            # Keep the text; a log collation must not discard evidence.
            collation["parsed"] = False
            yield (None, number, source), {"collation": collation, "raw_line": line}
            continue
        if not isinstance(record, dict):
            collation["parsed"] = False
            yield (None, number, source), {"collation": collation, "raw_line": line}
            continue
        stamp = record.get("timestamp")
        try:
            moment = datetime.datetime.fromisoformat(stamp)
        except (TypeError, ValueError):
            moment = None
        record["collation"] = collation
        yield (moment, number, source), record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-dir", required=True,
                        help="Directory searched recursively for events.jsonl files")
    parser.add_argument("--out", help="Output path (default: <base-dir>/events-merged.jsonl)")
    parser.add_argument("--exclude", action="append", default=[],
                        help="Skip sources whose relative path contains this text; repeatable")
    args = parser.parse_args(argv)

    base = Path(args.base_dir)
    if not base.is_dir():
        parser.error(f"{base} is not a directory")
    out = Path(args.out) if args.out else base / "events-merged.jsonl"

    logs = sorted(base.rglob("events.jsonl"))
    if out.resolve() in {p.resolve() for p in logs}:
        parser.error("Output path collides with an input log")
    entries, sources, skipped = [], [], []
    for path in logs:
        source = path.parent.relative_to(base).as_posix() or "."
        if any(token in source for token in args.exclude):
            skipped.append(source)
            continue
        found = list(read(path, source))
        entries.extend(found)
        sources.append((source, len(found)))
    if not entries:
        print(f"No event records found under {base}", file=sys.stderr)
        return 1

    # Undated records sort first so nothing is silently buried at the end.
    entries.sort(key=lambda item: (item[0][0] is not None,
                                   item[0][0] or datetime.datetime.min.replace(
                                       tzinfo=datetime.timezone.utc),
                                   item[0][2], item[0][1]))

    out.parent.mkdir(parents=True, exist_ok=True)
    unparsed = 0
    with out.open("w", encoding="utf-8", newline="\n") as stream:
        for _, record in entries:
            if "raw_line" in record:
                unparsed += 1
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    dated = [item[0][0] for item in entries if item[0][0] is not None]
    events = collections.Counter(r.get("event") for _, r in entries if "raw_line" not in r)
    # run_id is component-dependent: the orchestrator writes the run's own id,
    # while runner and environment subprocesses reuse the field for a
    # per-invocation id. Only the orchestrator's identifies the search.
    owners = collections.defaultdict(collections.Counter)
    for _, record in entries:
        if record.get("component") == "orchestrator" and record.get("run_id"):
            owners[record["collation"]["source"]][record["run_id"]] += 1
    print(f"Wrote {out}: {len(entries):,d} records from {len(sources)} log(s)")
    for source, count in sources:
        owned = owners.get(source)
        run_id = owned.most_common(1)[0][0] if owned else "no orchestrator events"
        print(f"  {source:<24} {count:>6,d}  {run_id}")
    for source in skipped:
        print(f"  {source:<24} {'excluded':>6}")
    if dated:
        print(f"  span {min(dated).isoformat()} .. {max(dated).isoformat()}")
    distinct = {rid for counts in owners.values() for rid in counts}
    print(f"  {len(distinct)} search run id(s), {len(events)} event type(s), "
          f"{unparsed} unparsable line(s)")
    print("  most frequent events: " + ", ".join(f"{name} {count:,d}"
                                                 for name, count in events.most_common(6)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
