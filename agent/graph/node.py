"""Pure data models for candidate pipelines and their search state.

Metric calculation, UCT updates, relationship validation, status transitions,
and persistence belong to the tree or execution layer. These dataclasses do
not validate inputs, run Git commands, or calculate derived values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class NodeStatus(str, Enum):
    """Execution or search lifecycle state of a candidate."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PRUNED = "pruned"


@dataclass(frozen=True)
class MetricResult:
    """Completed validation result; val_primary is supplied by the caller.

    val_ndcg denotes nDCG@5. wall_clock_s records elapsed candidate execution
    time in seconds, including any repairs and retries.
    """

    val_gauc: float
    val_ndcg: float
    val_primary: float
    wall_clock_s: float


@dataclass(frozen=True)
class EdgeAction:
    """Transformation from the parent pipeline to this candidate.

    raw_diff is the resulting Git diff relative to the parent. tokens_used
    records proposal token usage; None means usage was unavailable. Repair
    token usage is recorded separately in RecoveryEvent.
    """

    label: str
    hypothesis: str
    raw_diff: str = ""
    tokens_used: int | None = None


@dataclass(frozen=True)
class RecoveryEvent:
    """One repair attempt, appended after its outcome is known.

    attempt is one-based. raw_diff describes this repair alone; succeeded
    indicates whether the subsequent execution and evaluation succeeded.
    """

    attempt: int
    error_summary: str
    succeeded: bool
    raw_diff: str = ""
    tokens_used: int | None = None


@dataclass
class SearchNode:
    """A candidate and mutable bookkeeping for a single-parent search tree.

    The root has no parent or incoming edge and has depth zero. Pending
    candidates may lack metrics and Git references. git_commit_sha is the
    full commit ID of this candidate, never its parent's commit; it is the
    authoritative navigation reference because git_branch can move or vanish.
    The repository location is supplied by the run's GitDriver.

    visit_count and value_sum describe backed-up search rewards, separate
    from this candidate's validation metrics. uct_value is an optional cache,
    not an authoritative statistic: tree.py must refresh it when selection
    inputs change, including the parent's visit count. None means uncomputed.
    No visits or rewards are recorded automatically on construction.

    Callers enforce ancestry/depth consistency and selection eligibility;
    unfinished, failed, and pruned candidates are not eligible pipelines.
    """

    node_id: str
    parent_id: str | None = None
    children_ids: list[str] = field(default_factory=list)
    depth: int = 0
    status: NodeStatus = NodeStatus.PENDING
    git_branch: str | None = None
    git_commit_sha: str | None = None
    incoming_edge: EdgeAction | None = None
    metrics: MetricResult | None = None
    visit_count: int = 0
    value_sum: float = 0.0
    uct_value: float | None = None
    recovery_events: list[RecoveryEvent] = field(default_factory=list)
