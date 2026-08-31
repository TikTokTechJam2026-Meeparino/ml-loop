"""Offline tree checks: python scripts/test_tree.py."""

import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.node import EdgeAction, MetricResult, NodeStatus, SearchNode
from agent.graph.tree import SearchConfig, SearchTree


def metrics(score):
    return MetricResult(score, score, score, 1.0)


def make_tree(**kwargs):
    return SearchTree(SearchNode('root', status=NodeStatus.SUCCESS,
                                 metrics=metrics(0.5), git_commit_sha='a' * 40),
                      SearchConfig(strategy="uct", **kwargs))


def candidate(tree, name, parent='root'):
    node = SearchNode(name, parent_id=parent, depth=tree.nodes[parent].depth + 1,
                      incoming_edge=EdgeAction(name, 'Test hypothesis'))
    tree.add_node(node)
    return node


def finish(tree, name, score, parent='root'):
    node = candidate(tree, name, parent)
    tree.mark_running(name)
    tree.record_result(name, metrics(score) if score is not None else None,
                       git_commit_sha='b' * 40 if score is not None else None)
    return node


class TreeTests(unittest.TestCase):
    def test_backup_selection_and_lineage(self):
        tree = make_tree(max_children=2, patience=50)
        self.assertEqual(tree.select_parent().node_id, 'root')
        finish(tree, 'a', 0.6)
        finish(tree, 'b', 0.55)
        self.assertEqual(tree.select_parent().node_id, 'a')
        self.assertAlmostEqual(tree.uct_score('a'), 0.6 + math.sqrt(2 * math.log(2)))
        finish(tree, 'c', 0.7, 'a')
        self.assertEqual(tree.nodes['root'].visit_count, 3)
        self.assertAlmostEqual(tree.nodes['root'].value_sum, 1.85)
        self.assertEqual(tree.nodes['a'].visit_count, 2)
        self.assertAlmostEqual(tree.nodes['a'].value_sum, 1.3)
        self.assertEqual([n.node_id for n in tree.get_lineage_chain('c')], ['root', 'a', 'c'])
        self.assertEqual(tree.best_node().node_id, 'c')

    def test_failures_exhaustion_and_backtracking(self):
        tree = make_tree(max_children=2, patience=50)
        finish(tree, 'a', 0.6)
        finish(tree, 'b', 0.55)
        finish(tree, 'a1', None, 'a')
        finish(tree, 'a2', None, 'a')
        self.assertEqual(tree.nodes['a'].status, NodeStatus.SUCCESS)
        self.assertEqual(tree.select_parent().node_id, 'b')
        finish(tree, 'b1', None, 'b')
        finish(tree, 'b2', None, 'b')
        self.assertEqual(tree.stop_reason(), 'exhausted')
        self.assertIsNone(tree.select_parent())
        self.assertEqual(tree.iteration_count, 6)

    def test_pruning_boundary_and_best_history(self):
        tree = make_tree(patience=50)
        boundary = finish(tree, 'boundary', 0.49)
        self.assertEqual(boundary.status, NodeStatus.SUCCESS)
        bad = finish(tree, 'bad', 0.489)
        self.assertEqual(bad.status, NodeStatus.PRUNED)
        finish(tree, 'good', 0.8, 'boundary')
        tree.prune('boundary')
        self.assertEqual(tree.nodes['good'].status, NodeStatus.PRUNED)
        self.assertEqual(tree.best_node().node_id, 'good')
        self.assertEqual(tree.select_parent().node_id, 'root')

    def test_rolling_convergence_including_exact_threshold(self):
        tree = make_tree()
        finish(tree, 'a', 0.501)
        finish(tree, 'b', None)
        finish(tree, 'c', 0.502)
        self.assertEqual(tree.stop_reason(), 'convergence')
        tree = make_tree()
        finish(tree, 'a', 0.501)
        finish(tree, 'b', 0.502)
        finish(tree, 'c', 0.503)
        self.assertIsNone(tree.stop_reason())

    def test_budgets_and_single_active_attempt(self):
        tree = make_tree(max_iterations=1)
        candidate(tree, 'a')
        self.assertIsNone(tree.select_parent())
        with self.assertRaises(ValueError):
            candidate(tree, 'b')
        tree.record_result('a')
        self.assertEqual(tree.stop_reason(), 'iteration_budget')
        with self.assertRaises(ValueError):
            candidate(tree, 'c')
        tree = make_tree()
        self.assertEqual(tree.stop_reason(now=tree.started_at + 21600), 'time_budget')

    def test_invalid_result_is_atomic_and_completion_is_once(self):
        tree = make_tree()
        node = candidate(tree, 'a')
        with self.assertRaises(ValueError):
            tree.record_result('a', MetricResult(0.5, 0.5, 0.7, 1), git_commit_sha='b' * 40)
        with self.assertRaises(ValueError):
            tree.record_result('a', metrics(0.6), git_commit_sha='HEAD')
        self.assertEqual(node.status, NodeStatus.PENDING)
        self.assertEqual(tree.iteration_count, 0)
        tree.record_result('a')
        with self.assertRaises(ValueError):
            tree.record_result('a')
        self.assertEqual(tree.nodes['root'].visit_count, 1)

    def test_reload_preserves_active_state_and_rejects_corruption(self):
        tree = make_tree(patience=50)
        finish(tree, 'a', 0.6)
        candidate(tree, 'b')
        tree.mark_running('b')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'tree.json'
            tree.save(path)
            loaded = SearchTree.load(path)
            self.assertEqual(loaded.nodes, tree.nodes)
            self.assertEqual(loaded.started_at, tree.started_at)
            self.assertEqual(loaded.best_history, tree.best_history)
            self.assertIsNone(loaded.select_parent())
            loaded.record_result('b')
            loaded.save(path)
            resumed = SearchTree.load(path)
            self.assertEqual(resumed.select_parent().node_id, loaded.select_parent().node_id)
            self.assertEqual(resumed.stop_reason(now=tree.started_at + 21600), 'time_budget')
            payload = json.loads(path.read_text())
            payload['nodes'][0]['visit_count'] += 1
            path.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                SearchTree.load(path)
            payload['nodes'][0]['visit_count'] -= 1
            payload['nodes'][1]['parent_id'] = 'a'
            path.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                SearchTree.load(path)

    def test_configuration_validation(self):
        for options in ({'max_children': 0}, {'patience': True}, {'exploration_weight': -1},
                        {'max_wall_clock_s': float('nan')}, {'prune_delta': 0}):
            with self.assertRaises(ValueError):
                SearchConfig(**options)

    def test_uct_cache_is_not_authoritative(self):
        tree = make_tree(max_children=2, patience=50)
        self.assertEqual(tree.uct_score('root'), math.inf)
        finish(tree, 'a', 0.6)
        old_score = tree.uct_score('a')
        finish(tree, 'b', 0.55)
        tree.nodes['a'].uct_value = -100
        self.assertGreater(tree.uct_score('a'), old_score)
        self.assertEqual(tree.select_parent().node_id, 'a')

    def test_invalid_save_preserves_checkpoint(self):
        tree = make_tree()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'tree.json'
            tree.save(path)
            original = path.read_bytes()
            tree.nodes['root'].children_ids.append('root')
            with self.assertRaises(ValueError):
                tree.save(path)
            self.assertEqual(path.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
