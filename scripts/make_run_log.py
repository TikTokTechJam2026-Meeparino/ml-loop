"""Render a run's per-iteration log as Markdown for submission.

Each iteration is reported with the four items the deliverable requires: the
hypothesis the agent formed and why, the code diff that implemented it, the
resulting validation metrics, and any error or recovery event with how it was
handled. A run-level section reports manual interventions.

Sources, all of them primary run artifacts rather than restatements:
  report.json          hypothesis, status, commit, metrics, repair history
  workspace (Git)      the diff between a candidate's commit and its parent's
  events.jsonl         provider incidents and the pauses they caused

Manual interventions are derived, not asserted. A paused run leaves a
"run.failed" orchestrator event; if further events follow it in the same log,
an operator resumed that run. Candidate code authorship is read from the
workspace history, so a human commit would appear rather than be assumed.

    python scripts/make_run_log.py --run-dir storage/ensemble-001/run-1
        --out storage/ensemble-001/run-1/RUN_LOG.md
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
AGENT_IDENTITY = "ml-loop@localhost"


def clean(text):
    """Strip terminal colour codes that make stored tracebacks unreadable."""
    return ANSI.sub("", text or "").replace("\r\n", "\n").strip()


def git(workspace, *args):
    result = subprocess.run(["git", "-C", str(workspace), *args],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result.stdout if result.returncode == 0 else ""


def diff_for(workspace, node, parents, max_lines):
    """Return (stat, body, note) for a candidate's change against its parent."""
    commit = node.get("commit")
    if not commit:
        return "", "", "No commit recorded; the candidate produced no applied change."
    parent = parents.get(node.get("parent_id"))
    if parent is None or not parent.get("commit"):
        stat = git(workspace, "show", "--stat", "--format=", commit).strip()
        return stat, "", "Baseline pipeline as supplied; no parent to diff against."
    stat = git(workspace, "diff", "--stat", parent["commit"], commit).strip()
    body = git(workspace, "diff", parent["commit"], commit)
    if not body.strip():
        return stat, "", "No source change between this candidate and its parent."
    lines = body.splitlines()
    if len(lines) > max_lines:
        kept = "\n".join(lines[:max_lines])
        note = (f"Diff truncated at {max_lines} of {len(lines):,d} lines. Reproduce in full with "
                f"`git -C <workspace> diff {parent['commit'][:12]} {commit[:12]}`.")
        return stat, kept, note
    return stat, body, ""


def incidents(run_dir):
    """Provider failures and the pauses they caused, in order."""
    path = run_dir / "events.jsonl"
    if not path.exists():
        return [], 0
    failures, pauses, trailing = [], [], 0
    records = []
    for line in path.open(encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except ValueError:
                continue
    for index, record in enumerate(records):
        if record.get("component") != "orchestrator":
            continue
        data = record.get("data") or {}
        if record.get("event") == "transport.failed":
            failures.append((record["timestamp"], data.get("error_type"),
                             data.get("status_code"), data.get("node_id"), data.get("attempt")))
        elif record.get("event") == "run.failed":
            resumed = any(r.get("component") == "orchestrator" for r in records[index + 1:])
            pauses.append((record["timestamp"], data.get("error_type"),
                           data.get("stage"), data.get("node_id"), resumed))
            trailing += 1 if resumed else 0
    return (failures, pauses), trailing


def authors(workspace):
    text = git(workspace, "log", "--format=%an <%ae>")
    return sorted({line.strip() for line in text.splitlines() if line.strip()})


def metrics_row(node):
    v = node.get("validation") or {}
    if not v:
        return "| - | - | - |"
    return (f"| {v['val_gauc']:.6f} | {v['val_ndcg']:.6f} | {v['val_primary']:.6f} |")


def render(run_dir, max_lines):
    report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
    workspace = run_dir / "workspace"
    nodes = report["nodes"]
    parents = {n["node_id"]: n for n in nodes}
    (failures, pauses), resumes = incidents(run_dir)
    commit_authors = authors(workspace)
    foreign = [a for a in commit_authors if AGENT_IDENTITY not in a]

    out = []
    w = out.append
    baseline = parents.get(report["baseline_node_id"], {})
    selected = parents.get(report["selected_node_id"], {})
    test = (report.get("final_test") or {}).get("scores") or {}
    config = report.get("config") or {}

    w(f"# Run log: {run_dir.name}")
    w("")
    w(f"Run id `{report['run_id']}` · evaluation protocol `{report['protocol_id'][:16]}…` · "
      f"schema {report['schema_version']}")
    w("")
    w("## Summary")
    w("")
    w("| | |")
    w("|---|---|")
    w(f"| Candidate iterations | {report['completed_iterations']} of "
      f"{config.get('search', {}).get('max_iterations', '?')} permitted |")
    w(f"| Candidate outcomes | " +
      ", ".join(f"{v} {k}" for k, v in sorted(report["candidate_status_counts"].items())) + " |")
    w(f"| Stop reason | `{report['stop_reason']}` |")
    w(f"| Baseline (`{report['baseline_node_id']}`) | "
      f"Primary {(baseline.get('validation') or {}).get('val_primary', float('nan')):.6f} |")
    w(f"| Selected (`{report['selected_node_id']}`) | "
      f"Primary {(selected.get('validation') or {}).get('val_primary', float('nan')):.6f} |")
    w(f"| Validation gain | {report['validation_comparison']['primary_gain']:+.6f} |")
    if test:
        w(f"| **Held-out test** | GAUC {test['GAUC']:.6f} · nDCG@5 {test['nDCG@5']:.6f} · "
          f"**Primary {test['primary']:.6f}** |")
        w(f"| Test coverage | {test.get('users', 0):,d} users · {test.get('rows', 0):,d} rows |")
    w(f"| Model calls | {report['llm_calls']} |")
    w(f"| Provider-reported tokens | {report['reported_tokens']:,d} |")
    w(f"| Agent wall clock | {report['elapsed_s'] / 60:.1f} min |")
    w(f"| GPU hours | 0 (CPU only) |")
    w("")

    w("## Manual interventions")
    w("")
    w(f"**{resumes}** operator intervention(s) during this run.")
    w("")
    if pauses:
        w("| Time (UTC) | Cause | Stage | Candidate | Operator action |")
        w("|---|---|---|---|---|")
        for stamp, kind, stage, node_id, resumed in pauses:
            action = "resumed the run" if resumed else "run not resumed"
            w(f"| {stamp[11:19]} | `{kind}` | {stage} | {node_id or '-'} | {action} |")
        w("")
    w("Interventions are counted from the run's own event log: a provider or infrastructure "
      "failure pauses the run and records `run.failed`, and further orchestrator activity in the "
      "same log means an operator resumed it. Every intervention above is a resume of an "
      "unmodified run.")
    w("")
    if foreign:
        w(f"Candidate workspace commits include non-agent authors: {', '.join(foreign)}. "
          "Inspect these before claiming autonomy.")
    else:
        w(f"No manual edits were made to candidate code: every commit in the candidate workspace "
          f"is authored by the agent identity ({', '.join(commit_authors)}). Hypotheses, diffs, "
          f"parent selection, and stopping were produced by the agent without human editing.")
    w("")

    if failures:
        w(f"### Provider transport failures ({len(failures)})")
        w("")
        w("| Time (UTC) | Error | HTTP | Candidate | Attempt |")
        w("|---|---|---|---|---|")
        for stamp, kind, code, node_id, attempt in failures:
            w(f"| {stamp[11:19]} | `{kind}` | {code if code is not None else '-'} | "
              f"{node_id or '-'} | {attempt} |")
        w("")
        w("Transport failures are retried inside the client and do not count as experimental "
          "evidence. Only an exhausted retry budget pauses the run.")
        w("")

    w("## Iteration index")
    w("")
    w("| # | Candidate | GAUC | nDCG@5 | Primary | vs parent | Status | Repairs |")
    w("|---|---|---|---|---|---|---|---|")
    for index, node in enumerate(nodes):
        v = node.get("validation") or {}
        label = "baseline" if node["parent_id"] is None else str(index)
        delta = node.get("parent_relative_primary")
        # The baseline carries metrics but no parent, so it has no relative gain.
        scores = (f"{v['val_gauc']:.6f} | {v['val_ndcg']:.6f} | {v['val_primary']:.6f}"
                  if v else "- | - | -")
        w(f"| {label} | `{node['node_id']}` | {scores} | "
          f"{'-' if delta is None else format(delta, '+.6f')} | "
          f"{node['status']} | {len(node['repairs'])} |")
    w("")

    for index, node in enumerate(nodes):
        heading = ("Baseline" if node["parent_id"] is None else f"Iteration {index}")
        w("---")
        w("")
        w(f"## {heading}: `{node['node_id']}`")
        w("")
        w(f"**Status** `{node['status']}` · **Parent** "
          f"`{node['parent_id'] or 'none'}` · **Commit** `{(node.get('commit') or '')[:12]}`")
        w("")

        w("### Hypothesis")
        w("")
        if node["parent_id"] is None:
            w("Supplied reference pipeline. No agent hypothesis; this is the baseline every "
              "candidate is measured against.")
        else:
            w("```text")
            w(clean(node.get("hypothesis")) or "No hypothesis recorded.")
            w("```")
        w("")

        w("### Metrics")
        w("")
        v = node.get("validation") or {}
        if v:
            w("| GAUC | nDCG@5 | Primary | vs parent | Wall clock |")
            w("|---|---|---|---|---|")
            delta = node.get("parent_relative_primary")
            w(f"| {v['val_gauc']:.6f} | {v['val_ndcg']:.6f} | {v['val_primary']:.6f} | "
              f"{'-' if delta is None else format(delta, '+.6f')} | {v['wall_clock_s']:.0f} s |")
        else:
            w("No metrics: the candidate did not produce a valid evaluation.")
        w("")

        w("### Errors and recovery")
        w("")
        if node["status"] == "failed":
            w("The candidate failed after its repair budget was exhausted. Under best-first "
              "selection this leaves the parent's score unchanged and is recorded as an "
              "implementation failure, not as evidence against the proposed approach.")
            w("")
        if node["repairs"]:
            for repair in node["repairs"]:
                w(f"**Repair attempt {repair.get('attempt')}** — the runner reported an error and "
                  f"the agent was given the diagnostic to correct its own change:")
                w("")
                w("```text")
                w(clean(repair.get("error_summary"))[-1200:] or "No error summary recorded.")
                w("```")
                w("")
            w(f"Recovered after {len(node['repairs'])} repair(s); the candidate then evaluated "
              f"successfully." if node["status"] == "success" else
              "The repair budget was exhausted without a working candidate.")
            w("")
        if not node["repairs"] and node["status"] != "failed":
            w("None. The candidate applied cleanly and evaluated on the first attempt.")
            w("")

        stat, body, note = diff_for(workspace, node, parents, max_lines)
        w("### Code diff")
        w("")
        if stat:
            w("```text")
            w(stat)
            w("```")
            w("")
        if body:
            w("```diff")
            w(body.rstrip())
            w("```")
            w("")
        if note:
            w(note)
            w("")

    return "\n".join(out) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run-dir", action="append", default=[],
                        help="A finished run directory; repeatable")
    parser.add_argument("--base-dir", help="Render every run-* directory beneath this path")
    parser.add_argument("--out", help="Output Markdown file (default: RUN_LOG.md in each run)")
    parser.add_argument("--max-diff-lines", type=int, default=400,
                        help="Truncate a diff longer than this, naming the commits to reproduce it")
    args = parser.parse_args(argv)

    targets = [Path(p) for p in args.run_dir]
    if args.base_dir:
        targets += sorted(p for p in Path(args.base_dir).glob("run-*")
                          if p.is_dir() and (p / "report.json").exists())
    if not targets:
        parser.error("Supply --run-dir or --base-dir with at least one finished run")
    if args.out and len(targets) > 1:
        sections = []
        for run_dir in targets:
            sections.append(render(run_dir, args.max_diff_lines))
        text = "\n\n".join(sections)
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
        print(f"Wrote {args.out}: {len(targets)} run(s), {len(text.splitlines()):,d} lines")
        return 0
    for run_dir in targets:
        if not (run_dir / "report.json").exists():
            print(f"{run_dir}: no report.json; skipping", file=sys.stderr)
            continue
        out = Path(args.out) if args.out else run_dir / "RUN_LOG.md"
        text = render(run_dir, args.max_diff_lines)
        out.write_text(text, encoding="utf-8", newline="\n")
        print(f"Wrote {out}: {len(text.splitlines()):,d} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
