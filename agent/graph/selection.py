"""Deterministic best-first allocation; no model calls or filesystem access."""

import math
from dataclasses import dataclass

from agent.graph.node import NodeStatus


def _exceeds(delta: float, threshold: float) -> bool:
    """Strict gain past a threshold; an exact-threshold result stays a tie."""
    return delta > threshold and not math.isclose(delta, threshold, rel_tol=0, abs_tol=1e-12)


@dataclass
class BestFirstState:
    incumbent_id: str
    stagnant_evaluations: int = 0
    detours_started: int = 0
    detour_remaining: int = 0
    detour_parent_id: str | None = None
    review_required: bool = False

    def __post_init__(self):
        if not isinstance(self.incumbent_id, str) or not self.incumbent_id:
            raise ValueError("Invalid best-first incumbent")
        for name in ("stagnant_evaluations", "detours_started", "detour_remaining"):
            if type(getattr(self, name)) is not int or getattr(self, name) < 0:
                raise ValueError(f"Invalid best-first {name}")
        if type(self.review_required) is not bool:
            raise ValueError("Invalid best-first review flag")
        if self.detour_parent_id is not None and (
            not isinstance(self.detour_parent_id, str) or not self.detour_parent_id
        ):
            raise ValueError("Invalid detour parent")

    def choice(self, nodes, config):
        """Return (parent, reason) without reserving or consuming any budget.

        Other lineages are a cheap diversity proxy, not a claim that their
        architectures differ. Prefer their best score, then fall back to the
        best distinct checkpoint anywhere in the archive. Ties retain order.
        """
        if self.review_required:
            return None, "detour_exhausted"
        if self.detour_remaining:
            return nodes[self.detour_parent_id], "detour_continue"
        incumbent = nodes[self.incumbent_id]
        if self.stagnant_evaluations < config.stagnation_patience:
            return incumbent, "best_validation"
        if self.detours_started >= config.max_detours:
            return None, "detour_budget_exhausted"
        candidates = [n for n in nodes.values() if n.status == NodeStatus.SUCCESS
                      and n.node_id != incumbent.node_id
                      and n.git_commit_sha != incumbent.git_commit_sha]
        if not candidates:
            return None, "no_alternative"

        def ancestors(node):
            result = set()
            while node is not None:
                result.add(node.node_id)
                node = nodes.get(node.parent_id)
            return result

        lineage = ancestors(incumbent)
        alternatives = [n for n in candidates if n.node_id not in lineage
                        and incumbent.node_id not in ancestors(n)]
        parent = max(alternatives or candidates, key=lambda n: n.metrics.val_primary)
        return parent, "detour_start"

    def reserve(self, parent_id, reason, config):
        if reason == "detour_start":
            self.detours_started += 1
            self.detour_remaining = config.detour_attempts
            self.detour_parent_id = parent_id

    def complete(self, node, nodes, config):
        """Record one finished attempt against the incumbent.

        Only a gain larger than config.promotion_threshold moves the incumbent.
        A smaller gain is an ordinary completed evaluation: it falls through to
        the detour or stagnation branch below and stays in the archive, so
        best_node() can still select it as the final pipeline.
        """
        incumbent = nodes[self.incumbent_id]
        if node.metrics is not None and _exceeds(
                node.metrics.val_primary - incumbent.metrics.val_primary,
                config.promotion_threshold):
            self.incumbent_id = node.node_id
            self.stagnant_evaluations = 0
            self.detour_remaining = 0
            self.detour_parent_id = None
            return
        if self.detour_remaining:
            # Failed implementations consume a detour attempt, but cannot
            # become parents. A valid weaker result CAN be the next parent.
            self.detour_remaining -= 1
            if node.metrics is not None:
                self.detour_parent_id = node.node_id
            if not self.detour_remaining:
                self.detour_parent_id = None
                self.review_required = True
        elif node.metrics is not None:
            self.stagnant_evaluations += 1
