"""Single-parent UCT search, candidate accounting, and JSON checkpoints.

The tree owns registered nodes: callers must use its methods for topology and
completion updates. A candidate iteration ends at record_result(), including
failed candidates. Repairs happen within that iteration. Genesis is evaluated
before constructing the tree and is not a candidate iteration.
"""

from __future__ import annotations

import json
import math
import os
import re
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from agent.graph.node import EdgeAction, MetricResult, NodeStatus, RecoveryEvent, SearchNode


@dataclass(frozen=True)
class SearchConfig:
    exploration_weight: float = math.sqrt(2.0)
    max_children: int = 3
    prune_delta: float = -0.01
    improvement_threshold: float = 0.002
    patience: int = 3
    max_iterations: int = 50
    max_wall_clock_s: float = 6 * 60 * 60

    def __post_init__(self) -> None:
        for name in ("max_children", "patience", "max_iterations"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        for name in ("exploration_weight", "improvement_threshold", "max_wall_clock_s", "prune_delta"):
            _finite(getattr(self, name), name)
        if self.exploration_weight < 0 or self.improvement_threshold < 0:
            raise ValueError("Exploration weight and improvement threshold must be nonnegative")
        if self.max_wall_clock_s <= 0 or self.prune_delta >= 0:
            raise ValueError("Time budget must be positive and prune_delta negative")


def _finite(value: float, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")


def _metrics(result: MetricResult) -> None:
    if not isinstance(result, MetricResult):
        raise ValueError("Expected MetricResult")
    for name in ("val_gauc", "val_ndcg", "val_primary"):
        value = getattr(result, name)
        _finite(value, name)
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be in [0, 1]")
    _finite(result.wall_clock_s, "wall_clock_s")
    if result.wall_clock_s < 0:
        raise ValueError("wall_clock_s must be nonnegative")
    if not math.isclose(result.val_primary, (result.val_gauc + result.val_ndcg) / 2, abs_tol=1e-12, rel_tol=0):
        raise ValueError("val_primary must equal the mean of GAUC and nDCG@5")


def _commit(commit: str | None) -> None:
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", commit) is None:
        raise ValueError("An evaluated candidate requires a full Git commit SHA")


class SearchTree:
    """Bounded, sequential UCT search over evaluated pipeline states.

    Each selected parent can spawn up to max_children attempts (failures count).
    Selection expands a node with available slots before descending by UCT.
    Exhausted subtrees are skipped, providing backtracking without deleting
    history. Use one in-flight candidate at a time; parallel MCTS would require
    path reservations/virtual loss and is deliberately not implemented here.
    """

    def __init__(self, root: SearchNode, config: SearchConfig | None = None,
                 *, started_at: float | None = None) -> None:
        if not root.node_id or root.parent_id is not None or root.depth != 0 or root.incoming_edge is not None:
            raise ValueError("Genesis must have an ID, depth zero, and no parent or edge")
        if root.children_ids or root.status != NodeStatus.SUCCESS:
            raise ValueError("Genesis must be successful and have no children")
        _metrics(root.metrics)
        _commit(root.git_commit_sha)
        if root.visit_count != 0 or root.value_sum != 0:
            raise ValueError("New genesis must have zero search statistics")
        self.config = config or SearchConfig()
        self.nodes: dict[str, SearchNode] = {root.node_id: root}
        self.root_id = root.node_id
        self.started_at = time.time() if started_at is None else started_at
        _finite(self.started_at, "started_at")
        self.completed_ids: list[str] = []
        self.best_history: list[float] = [root.metrics.val_primary]

    @property
    def iteration_count(self) -> int:
        """Number of completed attempts; failures count, genesis does not."""
        return len(self.completed_ids)

    def get_lineage_chain(self, node_id: str) -> list[SearchNode]:
        """Return genesis through the given node, inclusive, with edge metadata."""
        chain = []
        seen = set()
        while node_id is not None:
            if node_id in seen:
                raise ValueError("Cycle in tree ancestry")
            seen.add(node_id)
            node = self.nodes[node_id]
            chain.append(node)
            node_id = node.parent_id
        return list(reversed(chain))

    def uct_score(self, node_id: str) -> float:
        """Compute fresh UCT; cached values are never used for selection.

        Unvisited nodes have infinite priority. None represents that value in
        the persisted cache so JSON never requires a nonstandard Infinity.
        """
        node = self.nodes[node_id]
        if node.visit_count == 0:
            node.uct_value = None
            return math.inf
        parent = self.nodes[node.parent_id] if node.parent_id is not None else node
        score = node.value_sum / node.visit_count + self.config.exploration_weight * math.sqrt(
            math.log(max(1, parent.visit_count)) / node.visit_count)
        node.uct_value = score
        return score

    def _expandable_subtrees(self) -> set[str]:
        available: set[str] = set()
        for node in sorted(self.nodes.values(), key=lambda n: n.depth, reverse=True):
            if node.status == NodeStatus.SUCCESS and (
                len(node.children_ids) < self.config.max_children
                or any(child in available for child in node.children_ids)
            ):
                available.add(node.node_id)
        return available

    def select_parent(self, *, now: float | None = None) -> SearchNode | None:
        """Select an expansion point, or None if stopped or an attempt is active."""
        if self.should_stop(now=now) or any(
            n.status in (NodeStatus.PENDING, NodeStatus.RUNNING) for n in self.nodes.values()
        ):
            return None
        available = self._expandable_subtrees()
        if self.root_id not in available:
            return None
        node = self.nodes[self.root_id]
        while len(node.children_ids) >= self.config.max_children:
            candidates = [self.nodes[c] for c in node.children_ids if c in available]
            # Stable insertion-order tie breaking makes resumed selection repeatable.
            node = max(candidates, key=lambda n: self.uct_score(n.node_id))
        return node

    def add_node(self, node: SearchNode, *, now: float | None = None) -> None:
        """Register one fresh pending attempt and atomically link it to its parent."""
        if self.should_stop(now=now):
            raise ValueError("Search has stopped")
        if any(n.status in (NodeStatus.PENDING, NodeStatus.RUNNING) for n in self.nodes.values()):
            raise ValueError("Finish the active candidate before adding another")
        if not isinstance(node.node_id, str) or not node.node_id or node.node_id in self.nodes:
            raise ValueError("Node ID must be nonempty and unique")
        if node.parent_id not in self.nodes:
            raise ValueError("Unknown parent")
        parent = self.nodes[node.parent_id]
        if any(n.status != NodeStatus.SUCCESS for n in self.get_lineage_chain(parent.node_id)):
            raise ValueError("Parent lineage must be successful and unpruned")
        if len(parent.children_ids) >= self.config.max_children:
            raise ValueError("Parent has exhausted its child slots")
        if node.depth != parent.depth + 1 or not isinstance(node.incoming_edge, EdgeAction):
            raise ValueError("Candidate requires matching depth and an incoming edge")
        if (node.status != NodeStatus.PENDING or node.children_ids or node.metrics is not None
                or node.visit_count != 0 or node.value_sum != 0 or node.uct_value is not None):
            raise ValueError("Candidate must have fresh pending state")
        self.nodes[node.node_id] = node
        parent.children_ids.append(node.node_id)

    def mark_running(self, node_id: str) -> None:
        node = self.nodes[node_id]
        if node.status != NodeStatus.PENDING:
            raise ValueError("Only pending candidates can start")
        node.status = NodeStatus.RUNNING

    def record_result(self, node_id: str, metrics: MetricResult | None = None,
                      *, git_commit_sha: str | None = None) -> None:
        """Finish an attempt exactly once; None metrics denotes unrecoverable failure.

        Back up absolute validation Primary (zero for failure) through the
        candidate and all ancestors. Failed attempts do not invalidate parents.
        Successful evaluations are backed up even when subsequently pruned.
        """
        node = self.nodes[node_id]
        if node.status not in (NodeStatus.PENDING, NodeStatus.RUNNING):
            raise ValueError("Candidate is already finished")
        if metrics is not None:
            _metrics(metrics)
            _commit(git_commit_sha if git_commit_sha is not None else node.git_commit_sha)
        chain = self.get_lineage_chain(node_id)
        if git_commit_sha is not None:
            node.git_commit_sha = git_commit_sha
        node.metrics = metrics
        node.status = NodeStatus.SUCCESS if metrics is not None else NodeStatus.FAILED
        reward = metrics.val_primary if metrics is not None else 0.0
        for ancestor in chain:
            ancestor.visit_count += 1
            ancestor.value_sum += reward
        for registered in self.nodes.values():
            registered.uct_value = None
        self.completed_ids.append(node_id)
        self.best_history.append(max(self.best_history[-1], reward))
        if metrics is not None:
            delta = reward - self.nodes[node.parent_id].metrics.val_primary
            if delta < self.config.prune_delta and not math.isclose(delta, self.config.prune_delta, abs_tol=1e-12, rel_tol=0):
                self.prune(node_id)

    def prune(self, node_id: str) -> None:
        """Disable an evaluated subtree, retaining metrics and failure statuses."""
        if node_id == self.root_id:
            raise ValueError("Genesis cannot be pruned")
        subtree = []
        pending = [node_id]
        while pending:
            node = self.nodes[pending.pop()]
            if node.status in (NodeStatus.PENDING, NodeStatus.RUNNING):
                raise ValueError("Finish active attempts before pruning their subtree")
            subtree.append(node)
            pending.extend(node.children_ids)
        for node in subtree:
            if node.status == NodeStatus.SUCCESS:
                node.status = NodeStatus.PRUNED
            node.uct_value = None

    def best_node(self) -> SearchNode:
        """Best evaluated pipeline, including pruned history, with genesis fallback."""
        return max((n for n in self.nodes.values() if n.metrics is not None
                    and n.status in (NodeStatus.SUCCESS, NodeStatus.PRUNED)),
                   key=lambda n: n.metrics.val_primary)

    def stop_reason(self, *, now: float | None = None) -> str | None:
        """Budgets include failed attempts; wall time includes time while unloaded.

        Pass run start time to the constructor to include baseline initialization.
        The orchestrator must enforce job timeouts and reserve final inference
        time; polling this method cannot interrupt a running training process.
        """
        current = time.time() if now is None else now
        _finite(current, "now")
        if current - self.started_at >= self.config.max_wall_clock_s:
            return "time_budget"
        if self.iteration_count >= self.config.max_iterations:
            return "iteration_budget"
        if self.iteration_count >= self.config.patience:
            gain = self.best_history[-1] - self.best_history[-1 - self.config.patience]
            threshold = self.config.improvement_threshold
            if gain <= threshold or math.isclose(gain, threshold, abs_tol=1e-12, rel_tol=0):
                return "convergence"
        if not self._expandable_subtrees() and not any(
            n.status in (NodeStatus.PENDING, NodeStatus.RUNNING) for n in self.nodes.values()
        ):
            return "exhausted"
        return None

    def should_stop(self, *, now: float | None = None) -> bool:
        return self.stop_reason(now=now) is not None

    def save(self, path: str | Path = "storage/state_tree.json") -> None:
        """Atomically replace a versioned JSON checkpoint; no Git operations."""
        self._validate_checkpoint()
        payload = {
            "version": 1, "config": asdict(self.config), "root_id": self.root_id,
            "started_at": self.started_at, "completed_ids": self.completed_ids,
            "best_history": self.best_history,
            "nodes": [dict(asdict(node), uct_value=None) for node in self.nodes.values()],
        }
        encoded = json.dumps(payload, indent=2, allow_nan=False)
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        handle, name = tempfile.mkstemp(dir=destination.parent, prefix=f".{destination.name}.", suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                stream.write(encoded + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, destination)
        finally:
            Path(name).unlink(missing_ok=True)

    @classmethod
    def load(cls, path: str | Path = "storage/state_tree.json") -> SearchTree:
        """Restore typed records and reject inconsistent topology/accounting.

        An interrupted pending/running attempt stays active; the orchestrator
        must resume it or record failure before starting another candidate.
        """
        with Path(path).open(encoding="utf-8") as stream:
            payload = json.load(stream)
        if payload["version"] != 1:
            raise ValueError("Unsupported tree checkpoint version")
        nodes = {}
        for raw in payload["nodes"]:
            raw = dict(raw)
            raw["status"] = NodeStatus(raw["status"])
            raw["metrics"] = MetricResult(**raw["metrics"]) if raw["metrics"] is not None else None
            raw["incoming_edge"] = EdgeAction(**raw["incoming_edge"]) if raw["incoming_edge"] is not None else None
            raw["recovery_events"] = [RecoveryEvent(**event) for event in raw["recovery_events"]]
            raw["uct_value"] = None
            node = SearchNode(**raw)
            if not isinstance(node.node_id, str) or not node.node_id or node.node_id in nodes:
                raise ValueError("Invalid or duplicate node ID")
            nodes[node.node_id] = node
        root = nodes[payload["root_id"]]
        # Validate genesis through the ordinary constructor without mutating it.
        fresh_root = SearchNode(node_id=root.node_id, parent_id=root.parent_id,
                                depth=root.depth, incoming_edge=root.incoming_edge,
                                status=root.status, metrics=root.metrics, git_commit_sha=root.git_commit_sha)
        tree = cls(fresh_root, SearchConfig(**payload["config"]), started_at=payload["started_at"])
        tree.nodes = nodes
        tree.completed_ids = payload["completed_ids"]
        tree.best_history = payload["best_history"]
        tree._validate_checkpoint()
        return tree

    def _validate_checkpoint(self) -> None:
        completed = self.completed_ids
        if not isinstance(completed, list) or len(set(completed)) != len(completed) or self.root_id in completed:
            raise ValueError("Invalid completion history")
        expected_visits = dict.fromkeys(self.nodes, 0)
        expected_values = dict.fromkeys(self.nodes, 0.0)
        history = [self.nodes[self.root_id].metrics.val_primary]
        reached = {self.root_id}
        active = 0
        for node in self.nodes.values():
            if type(node.depth) is not int or node.depth < 0 or type(node.visit_count) is not int:
                raise ValueError("Invalid depth or visit count")
            if not isinstance(node.children_ids, list) or len(set(node.children_ids)) != len(node.children_ids):
                raise ValueError("Invalid child list")
            if len(node.children_ids) > self.config.max_children:
                raise ValueError("Child limit exceeded")
            for child_id in node.children_ids:
                child = self.nodes[child_id]
                if child_id in reached or child.parent_id != node.node_id or child.depth != node.depth + 1:
                    raise ValueError("Inconsistent tree topology")
                reached.add(child_id)
            if node.node_id != self.root_id and not isinstance(node.incoming_edge, EdgeAction):
                raise ValueError("Missing incoming edge")
            if node.status in (NodeStatus.SUCCESS, NodeStatus.PRUNED):
                _metrics(node.metrics)
                _commit(node.git_commit_sha)
            elif node.metrics is not None or node.children_ids:
                raise ValueError("Unsuccessful node has metrics or descendants")
            if node.status in (NodeStatus.PENDING, NodeStatus.RUNNING):
                active += 1
            elif node.node_id != self.root_id and node.node_id not in completed:
                raise ValueError("Completed node missing from history")
            chain = self.get_lineage_chain(node.node_id)
            if chain[0].node_id != self.root_id:
                raise ValueError("Disconnected node")
            if node.status != NodeStatus.PRUNED and any(n.status == NodeStatus.PRUNED for n in chain[:-1]) and node.status != NodeStatus.FAILED:
                raise ValueError("Active node under pruned ancestor")
        if reached != set(self.nodes) or active > 1:
            raise ValueError("Disconnected tree or multiple active attempts")
        seen = {self.root_id}
        for node_id in completed:
            node = self.nodes[node_id]
            if node.status not in (NodeStatus.SUCCESS, NodeStatus.PRUNED, NodeStatus.FAILED) or node.parent_id not in seen:
                raise ValueError("Invalid completion order")
            seen.add(node_id)
            reward = node.metrics.val_primary if node.metrics is not None else 0.0
            history.append(max(history[-1], reward))
            for ancestor in self.get_lineage_chain(node_id):
                expected_visits[ancestor.node_id] += 1
                expected_values[ancestor.node_id] += reward
        if len(self.nodes) - 1 > self.config.max_iterations or self.best_history != history:
            raise ValueError("Invalid iteration or score history")
        for node in self.nodes.values():
            _finite(node.value_sum, "value_sum")
            if node.visit_count != expected_visits[node.node_id] or not math.isclose(node.value_sum, expected_values[node.node_id], abs_tol=1e-12, rel_tol=0):
                raise ValueError("Search statistics disagree with completion history")
