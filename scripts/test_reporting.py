"""Offline final report checks: python -B scripts/test_reporting.py."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.node import EdgeAction, MetricResult, NodeStatus, SearchNode
from agent.graph.tree import SearchConfig, SearchTree
from agent.reporting import FinalTestResult, build_report, write_report


class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.tree = SearchTree(SearchNode("root", status=NodeStatus.SUCCESS,
                                         metrics=MetricResult(.5, .5, .5, 1), git_commit_sha="a" * 40),
                               SearchConfig(strategy="uct"))
        for name, score in (("better", .6), ("failed", None)):
            self.tree.add_node(SearchNode(name, parent_id="root", depth=1,
                                          incoming_edge=EdgeAction(name, "Try capacity")))
            self.tree.record_result(name, MetricResult(score, score, score, 2) if score else None,
                                    git_commit_sha="b" * 40 if score else None)

    def report(self, **kwargs):
        return build_report(self.tree, selected_node_id="better", stop_reason="iteration_budget", **kwargs)

    def test_comparison_failed_attempts_and_artifact_index(self):
        report = self.report(artifacts={"better": {"checkpoint": "checkpoints/b.pkl"}})
        self.assertAlmostEqual(report["validation_comparison"]["primary_gain"], .1)
        self.assertEqual(report["completed_iterations"], 2)
        self.assertEqual(report["candidate_status_counts"], {"success": 1, "failed": 1})
        failed = next(n for n in report["nodes"] if n["node_id"] == "failed")
        self.assertIsNone(failed["validation"])
        self.assertIsNone(failed["parent_relative_primary"])
        self.assertEqual(report["final_test"]["status"], "not_run")
        self.assertEqual(report["nodes"][1]["artifacts"]["checkpoint"], "checkpoints/b.pkl")

    def test_test_results_are_separate_and_bound_to_selection(self):
        test = FinalTestResult("better", "success", {"GAUC": .4, "nDCG@5": .2, "primary": .3})
        report = self.report(final_test=test)
        self.assertEqual(report["final_test"]["scores"]["primary"], .3)
        self.assertEqual(report["validation_comparison"]["selected"]["val_primary"], .6)
        with self.assertRaises(ValueError):
            self.report(final_test=FinalTestResult("root", "timeout"))
        with self.assertRaises(ValueError):
            self.report(final_test=FinalTestResult("better", "success"))
        with self.assertRaises(ValueError):
            self.report(final_test=FinalTestResult("better", "failed", test.scores))

    def test_pruned_selection_and_genesis_fallback(self):
        self.tree.prune("better")
        self.assertEqual(self.report()["selected_node_id"], "better")
        report = build_report(self.tree, selected_node_id="root", stop_reason="time_budget")
        self.assertEqual(report["validation_comparison"]["primary_gain"], 0)
        with self.assertRaises(ValueError):
            build_report(self.tree, selected_node_id="failed", stop_reason="time_budget")

    def test_atomic_export_and_detached_snapshot(self):
        report = self.report()
        report["nodes"][0]["validation"]["val_primary"] = .1
        self.assertEqual(self.tree.nodes["root"].metrics.val_primary, .5)
        with tempfile.TemporaryDirectory() as directory:
            path = write_report(report, Path(directory) / "report.json")
            self.assertEqual(json.loads(path.read_text()), report)
            before = path.read_bytes()
            with self.assertRaises(ValueError):
                write_report({"invalid": float("nan")}, path)
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
