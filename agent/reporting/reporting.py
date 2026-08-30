"""Summarize evaluated pipelines and export a standalone JSON report."""

import json
import math
import os
import tempfile
from collections import Counter
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path

from agent.graph.node import NodeStatus
from agent.graph.tree import SearchTree


@dataclass(frozen=True)
class FinalTestResult:
    """Caller-supplied outcome from test inference after selection was frozen.

    artifact_dir links to the runner's predictions and execution report. Error
    text must be redacted by the caller. This record does not perform inference.
    """

    node_id: str
    status: str
    scores: dict[str, float] | None = None
    artifact_dir: str | None = None
    error: str | None = None


def build_report(tree: SearchTree, *, selected_node_id: str, stop_reason: str,
                 artifacts: Mapping[str, Mapping[str, str]] | None = None,
                 final_test: FinalTestResult | None = None) -> dict:
    """Build a detached report without selecting a node or changing search state.

    Artifacts map node IDs to named path references (checkpoint, logs, etc.).
    References are indexed, not copied or checked for existence. Missing test
    inference is explicitly reported, never inferred from validation metrics.
    """
    if not isinstance(stop_reason, str) or not stop_reason.strip():
        raise ValueError("Provide the actual search stop reason")
    selected = tree.nodes[selected_node_id]
    baseline = tree.nodes[tree.root_id]
    if selected.status not in (NodeStatus.SUCCESS, NodeStatus.PRUNED) or selected.metrics is None:
        raise ValueError("Selected pipeline must have a valid evaluation")
    if baseline.metrics is None:
        raise ValueError("Genesis must have validation metrics")
    references = {}
    for node_id, paths in (artifacts or {}).items():
        if node_id not in tree.nodes or not isinstance(paths, Mapping):
            raise ValueError("Artifacts must refer to registered nodes")
        if any(not isinstance(k, str) or not isinstance(v, str) for k, v in paths.items()):
            raise ValueError("Artifact names and references must be strings")
        references[node_id] = dict(paths)
    test = {"status": "not_run", "node_id": selected_node_id, "scores": None}
    if final_test is not None:
        if final_test.node_id != selected_node_id:
            raise ValueError("Test results must belong to the selected node")
        if final_test.status not in {"success", "failed", "timeout", "not_run"}:
            raise ValueError("Unknown final test status")
        if final_test.status == "success":
            scores = final_test.scores
            if not isinstance(scores, dict) or not {"GAUC", "nDCG@5", "primary"} <= scores.keys():
                raise ValueError("Successful test inference requires test scores")
            for key in ("GAUC", "nDCG@5", "primary"):
                value = scores[key]
                if isinstance(value, bool) or not isinstance(value, (float, int)) or not 0 <= value <= 1:
                    raise ValueError("Invalid test score")
            if not math.isclose(scores["primary"], (scores["GAUC"] + scores["nDCG@5"]) / 2,
                                rel_tol=0, abs_tol=1e-12):
                raise ValueError("Test Primary must equal the mean of GAUC and nDCG@5")
        elif final_test.scores is not None:
            raise ValueError("Unsuccessful test inference cannot carry scores")
        test = asdict(final_test)
    nodes = []
    for node in tree.nodes.values():
        parent = tree.nodes.get(node.parent_id)
        delta = (node.metrics.val_primary - parent.metrics.val_primary
                 if node.metrics is not None and parent is not None and parent.metrics is not None else None)
        nodes.append({
            "node_id": node.node_id, "parent_id": node.parent_id,
            "status": node.status.value, "commit": node.git_commit_sha,
            "hypothesis": node.incoming_edge.hypothesis if node.incoming_edge else None,
            "validation": asdict(node.metrics) if node.metrics else None,
            "parent_relative_primary": delta,
            "repairs": [asdict(event) for event in node.recovery_events],
            "artifacts": references.get(node.node_id, {}),
        })
    report = {
        "schema_version": 1, "stop_reason": stop_reason,
        "completed_iterations": tree.iteration_count,
        "candidate_status_counts": dict(Counter(n.status.value for n in tree.nodes.values()
                                                 if n.node_id != tree.root_id)),
        "baseline_node_id": tree.root_id, "selected_node_id": selected_node_id,
        "validation_comparison": {
            "baseline": asdict(baseline.metrics), "selected": asdict(selected.metrics),
            "primary_gain": selected.metrics.val_primary - baseline.metrics.val_primary,
        },
        "final_test": test, "nodes": nodes,
    }
    # Reject unserializable or nonfinite values now, before any output is written.
    return json.loads(json.dumps(report, allow_nan=False))


def write_report(report: dict, path: str | Path) -> Path:
    """Atomically write JSON; preserve an existing report if serialization fails."""
    payload = json.dumps(report, indent=2, allow_nan=False) + "\n"
    destination = Path(path).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=destination.parent, prefix=f".{destination.name}.", suffix=".tmp")
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination
