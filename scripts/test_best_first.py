"""Offline allocation/checkpoint tests; no training or provider requests."""

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.node import EdgeAction, MetricResult, NodeStatus, SearchNode
from agent.graph.tree import SearchConfig, SearchTree


def score(value):
    return MetricResult(value, value, value, 1.0)


def tree(**kwargs):
    return SearchTree(SearchNode('root', status=NodeStatus.SUCCESS, metrics=score(.6),
                                 git_commit_sha='a' * 40), SearchConfig(**kwargs))


def add(search, name):
    parent = search.select_parent()
    node = SearchNode(name, parent_id=parent.node_id, depth=parent.depth + 1,
                      incoming_edge=EdgeAction(name, 'Synthetic hypothesis'))
    search.add_node(node)
    return node


def finish(search, name, value):
    node = add(search, name)
    search.record_result(name, score(value) if value is not None else None,
                         git_commit_sha=hashlib.sha1(name.encode()).hexdigest() if value is not None else None)
    return node


class BestFirstTests(unittest.TestCase):
    def test_immediate_promotion_without_child_cap_or_uct_backup(self):
        search = tree(max_children=1, patience=1)
        finish(search, 'winner', .61)
        self.assertEqual(search.select_parent().node_id, 'winner')
        for name, value in [('loss1', .59), ('loss2', .58), ('failure', None), ('tie', .61)]:
            self.assertEqual(finish(search, name, value).parent_id, 'winner')
        self.assertEqual(search.select_parent().node_id, 'winner')
        self.assertEqual(search.selection.stagnant_evaluations, 3)
        self.assertEqual(search.nodes['winner'].visit_count, 4)  # Failure adds no zero-reward visit.
        self.assertEqual(search.nodes['failure'].visit_count, 0)
        self.assertEqual(search.best_node().node_id, 'winner')
        self.assertEqual(search.nodes['loss2'].status, NodeStatus.SUCCESS)  # No auto-pruning.
        search._validate_checkpoint()

    def test_default_five_evaluations_then_two_attempt_detour(self):
        search = tree()
        finish(search, 'winner', .61)
        finish(search, 'broken', None)
        for i in range(5):
            self.assertEqual(search.select_parent().node_id, 'winner')
            finish(search, f'loss{i}', .605)
        self.assertEqual(search.selection.detours_started, 0)
        # Every loss is a child of the incumbent, so the detour leaves its
        # subtree for the root rather than descending further into it.
        self.assertEqual(search.select_parent().node_id, 'root')
        for _ in range(3):
            self.assertEqual(search.select_parent().node_id, 'root')
        self.assertEqual(search.selection.detours_started, 0)  # Reads never consume budget.
        first = finish(search, 'detour1', .50)
        self.assertEqual(search.selection.detours_started, 1)
        self.assertEqual(search.select_parent().node_id, first.node_id)  # Traverse a worse model.
        finish(search, 'detour2', .62)
        self.assertEqual(search.select_parent().node_id, 'detour2')
        self.assertEqual(search.selection.stagnant_evaluations, 0)
        self.assertEqual(search.selection.detour_remaining, 0)
        self.assertEqual(search.best_node().node_id, 'detour2')
        search._validate_checkpoint()

    def test_unsuccessful_detour_stops_even_if_locally_improved(self):
        search = tree(stagnation_patience=1)
        finish(search, 'winner', .61)
        finish(search, 'loser', .60)
        finish(search, 'detour1', .55)
        finish(search, 'detour2', .59)
        self.assertEqual(search.stop_reason(), 'stagnation')
        self.assertIsNone(search.select_parent())
        self.assertEqual(search.best_node().node_id, 'winner')
        self.assertTrue(search.selection.review_required)
        with self.assertRaises(ValueError):
            search.add_node(SearchNode('extra', parent_id='winner', depth=2,
                                       incoming_edge=EdgeAction('x', 'x')))

    def test_failed_detour_is_bounded_and_retries_its_parent(self):
        search = tree(stagnation_patience=1)
        finish(search, 'winner', .61)
        finish(search, 'loser', .605)
        before = search.nodes['loser'].visit_count
        finish(search, 'broken1', None)
        # 'loser' is a descendant of the incumbent, so the detour takes the root
        # instead and retries it; failed attempts still leave 'loser' untouched.
        self.assertEqual(search.select_parent().node_id, 'root')
        finish(search, 'broken2', None)
        self.assertEqual(search.nodes['loser'].visit_count, before)
        self.assertEqual(search.stop_reason(), 'stagnation')
        self.assertEqual(search.iteration_count, 4)

    def test_other_lineage_preferred_and_same_commit_excluded(self):
        """Legacy policy: the ancestry chain, root included, is ineligible."""
        search = tree(stagnation_patience=2, detour_allows_ancestors=False)
        finish(search, 'alternative', .59)  # Sibling of winner.
        finish(search, 'winner', .61)
        finish(search, 'descendant', .605)
        finish(search, 'descendant2', .604)
        self.assertEqual(search.select_parent().node_id, 'alternative')
        search.nodes['alternative'].git_commit_sha = search.nodes['winner'].git_commit_sha
        self.assertEqual(search.select_parent().node_id, 'descendant')

    def test_detour_prefers_root_over_a_sibling_and_never_its_own_subtree(self):
        """Current policy on the same shape: root outscores the sibling.

        'alternative' is a sibling of the incumbent, so the neighbourhood rule
        skips it and the root becomes the clean base. Once the root is the only
        option left it is still chosen ahead of the incumbent's descendants.
        """
        search = tree(stagnation_patience=2)
        finish(search, 'alternative', .59)
        finish(search, 'winner', .61)
        finish(search, 'descendant', .605)
        finish(search, 'descendant2', .604)
        self.assertEqual(search.select_parent().node_id, 'root')
        search.nodes['alternative'].git_commit_sha = search.nodes['winner'].git_commit_sha
        self.assertEqual(search.select_parent().node_id, 'root')

    def test_budget_and_no_unbounded_detour_cycles(self):
        search = tree(stagnation_patience=1, max_iterations=3)
        finish(search, 'winner', .61)
        finish(search, 'loser', .60)
        finish(search, 'detour', .59)
        self.assertEqual(search.stop_reason(), 'iteration_budget')
        self.assertEqual(search.selection.detour_remaining, 1)
        self.assertIsNone(search.select_parent())
        search = tree(stagnation_patience=1)
        finish(search, 'winner', .61)
        finish(search, 'loser', .60)
        finish(search, 'detour_win', .62)
        finish(search, 'loss_again', .61)
        self.assertEqual(search.stop_reason(), 'stagnation')
        self.assertEqual(search.selection.detours_started, 1)
        self.assertEqual(search.stop_reason(now=search.started_at + 21600), 'time_budget')

    def test_no_alternative_and_disabled_detours(self):
        search = tree(stagnation_patience=1)
        finish(search, 'same_code', .6)
        search.nodes['same_code'].git_commit_sha = search.nodes['root'].git_commit_sha
        self.assertEqual(search.selection_status()['reason'], 'no_alternative')
        self.assertEqual(search.stop_reason(), 'stagnation')
        search = tree(stagnation_patience=1, max_detours=0)
        finish(search, 'loser', .59)
        self.assertEqual(search.stop_reason(), 'stagnation')

    def test_checkpoint_before_during_after_detour_and_corruption(self):
        search = tree(stagnation_patience=1)
        finish(search, 'winner', .61)
        finish(search, 'loser', .60)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'tree.json'

            def reload():
                search.save(path)
                loaded = SearchTree.load(path)
                self.assertEqual(asdict(loaded.selection), asdict(search.selection))
                self.assertEqual(loaded.selection_status(), search.selection_status())
                return loaded

            search = reload()
            add(search, 'detour1')
            search.mark_running('detour1')
            search = reload()
            self.assertIsNone(search.select_parent())
            search.record_result('detour1', score(.55), git_commit_sha='d' * 40)
            search = reload()
            self.assertEqual(search.select_parent().node_id, 'detour1')
            finish(search, 'detour2', .54)
            search = reload()
            self.assertEqual(search.stop_reason(), 'stagnation')
            payload = json.loads(path.read_text())
            payload['selection']['detours_started'] = 0
            path.write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError, 'state disagrees'):
                SearchTree.load(path)

    def test_invalid_parent_does_not_reserve_detour(self):
        search = tree(stagnation_patience=1)
        finish(search, 'winner', .61)
        finish(search, 'loser', .60)
        before = asdict(search.selection)
        with self.assertRaisesRegex(ValueError, 'Parent differs'):
            search.add_node(SearchNode('wrong', parent_id='winner', depth=2,
                                       incoming_edge=EdgeAction('x', 'x')))
        self.assertEqual(asdict(search.selection), before)

    def test_sub_threshold_gain_is_archived_but_not_promoted(self):
        search = tree(promotion_threshold=1e-4, stagnation_patience=3)
        finish(search, 'noise', .6 + 5e-5)
        self.assertEqual(search.selection.incumbent_id, 'root')
        self.assertEqual(search.selection.stagnant_evaluations, 1)
        # Not the incumbent, but still the archive best and still selectable.
        self.assertEqual(search.best_node().node_id, 'noise')
        self.assertEqual(search.select_parent().node_id, 'root')
        finish(search, 'exact', .6 + 1e-4)  # Exactly at the threshold: a tie.
        self.assertEqual(search.selection.incumbent_id, 'root')
        finish(search, 'real', .6 + 2e-4)
        self.assertEqual(search.selection.incumbent_id, 'real')
        self.assertEqual(search.selection.stagnant_evaluations, 0)
        search._validate_checkpoint()

    def test_sub_threshold_gain_still_consumes_a_detour_attempt(self):
        search = tree(stagnation_patience=1, promotion_threshold=1e-3)
        finish(search, 'winner', .61)
        finish(search, 'loser', .605)
        finish(search, 'detour1', .606)
        self.assertEqual(search.selection.detour_parent_id, 'detour1')
        finish(search, 'detour2', .6105)  # +0.0005 over the incumbent: below threshold.
        self.assertEqual(search.selection.incumbent_id, 'winner')
        self.assertTrue(search.selection.review_required)
        self.assertEqual(search.best_node().node_id, 'detour2')
        search._validate_checkpoint()

    def test_saved_runs_keep_the_original_promotion_rule(self):
        self.assertEqual(SearchConfig().promotion_threshold, 1e-4)
        self.assertEqual(SearchConfig.from_saved({'strategy': 'best_first'}).promotion_threshold, 0.0)
        search = tree(promotion_threshold=0.0)
        finish(search, 'noise', .6 + 5e-5)
        self.assertEqual(search.selection.incumbent_id, 'noise')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'tree.json'
            search.save(path)
            payload = json.loads(path.read_text())
            payload['config'].pop('promotion_threshold')  # A checkpoint predating the field.
            path.write_text(json.dumps(payload))
            loaded = SearchTree.load(path)
            self.assertEqual(loaded.config.promotion_threshold, 0.0)
            self.assertEqual(loaded.selection.incumbent_id, 'noise')

    def test_detour_leaves_the_incumbent_neighbourhood(self):
        """A detour must skip the incumbent's parent and siblings.

        Mirrors storage/live-50-002, where excluding only the ancestry chain
        sent the detour to a near-identical sibling while the architecturally
        distinct grandparent stayed ineligible.
        """
        from agent.graph.selection import BestFirstState
        shape = {'root': (None, .60), 'gp': ('root', .6035), 'parent': ('gp', .6036),
                 'sib': ('parent', .6036), 'inc': ('parent', .6042)}
        nodes = {name: SearchNode(name, parent_id=par, status=NodeStatus.SUCCESS,
                                  metrics=score(value),
                                  git_commit_sha=hashlib.sha1(name.encode()).hexdigest())
                 for name, (par, value) in shape.items()}
        for allows, expected in ((False, 'sib'), (True, 'gp')):
            config = SearchConfig(stagnation_patience=1, detour_allows_ancestors=allows)
            state = BestFirstState('inc', stagnant_evaluations=1)
            parent, reason = state.choice(nodes, config)
            self.assertEqual((parent.node_id, reason), (expected, 'detour_start'))

    def test_saved_runs_keep_the_ancestry_chain_exclusion(self):
        self.assertIs(SearchConfig().detour_allows_ancestors, True)
        self.assertIs(SearchConfig.from_saved({'strategy': 'best_first'}).detour_allows_ancestors,
                      False)

    def test_config_validation(self):
        self.assertEqual(SearchConfig().strategy, 'best_first')
        self.assertEqual(SearchConfig.from_saved({}).strategy, 'uct')
        for kwargs in ({'strategy': 'unknown'}, {'detour_attempts': 0}, {'max_detours': -1},
                       {'max_detours': True}, {'stagnation_patience': True},
                       {'promotion_threshold': -1}, {'promotion_threshold': float('nan')},
                       {'detour_allows_ancestors': 1}, {'detour_allows_ancestors': 'yes'}):
            with self.assertRaises(ValueError):
                SearchConfig(**kwargs)


if __name__ == '__main__':
    unittest.main()
