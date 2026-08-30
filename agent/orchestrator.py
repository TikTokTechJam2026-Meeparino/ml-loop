# TODO: Store two configurable, parent-relative reflection thresholds in run
# configuration: breakthrough_delta (positive) and collapse_delta (negative).
# Trigger a bounded LLM reflection when Primary gain exceeds breakthrough_delta,
# loss falls below collapse_delta, or a candidate reaches FAILED after all repair
# retries are exhausted. Pruning alone must not trigger reflection, since it can
# propagate from an ancestor. Skip reflection for routine iterations and when
# time/token budgets cannot accommodate it; reflection failure must not discard
# the experiment result. Call agent.graph.reflection.ReflectionEngine.reflect()
# with the completed node, parent, MemoryContext, and redacted failure stderr.
# It returns a tentative interpretation or None when unavailable. Record once,
# after reflection, via ExplorationMemory.record(...,
# reflection=...), retaining numeric/error evidence; memory owns no thresholds
# and makes no LLM calls. Threshold values remain to be chosen in run config.
