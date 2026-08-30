# TODO: Store two configurable, parent-relative reflection thresholds in run
# configuration: breakthrough_delta (positive) and collapse_delta (negative).
# Trigger a bounded LLM reflection when Primary gain exceeds breakthrough_delta,
# loss falls below collapse_delta, or a candidate reaches FAILED after all repair
# retries are exhausted. Pruning alone must not trigger reflection, since it can
# propagate from an ancestor. Skip reflection for routine iterations and when
# time/token budgets cannot accommodate it; reflection failure must not discard
# the experiment result. Pass hypothesis, diff, parent/child metrics and relevant
# diagnostics, asking for a tentative explanation rather than an established
# cause. Store the optional interpretation via ExplorationMemory.record(...,
# reflection=...), retaining numeric/error evidence; memory owns no thresholds
# and makes no LLM calls. Threshold values remain to be chosen in run config.
