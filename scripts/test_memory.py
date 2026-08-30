"""Offline memory tests: python scripts/test_memory.py."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.graph.memory import ExplorationMemory, InsightOutcome, MemoryContext, error_signature
from agent.graph.node import EdgeAction, MetricResult, NodeStatus, SearchNode


def metric(score):
    return MetricResult(score, score, score, 1)


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.memory = ExplorationMemory()
        self.context = MemoryContext('run1', 'protocol1', 'features', {'shape': [5, 16]})
        self.parent = SearchNode('root', status=NodeStatus.SUCCESS, metrics=metric(0.5), git_commit_sha='a' * 40)

    def record(self, name, score=0.6, *, context=None, status=None, hypothesis='Try a sequence', **kwargs):
        node = SearchNode(name, parent_id='root', depth=1,
                          incoming_edge=EdgeAction('seq', hypothesis, 'raw diff'),
                          metrics=metric(score) if score is not None else None,
                          status=status or (NodeStatus.SUCCESS if score is not None else NodeStatus.FAILED))
        return self.memory.record(node, self.parent, context or self.context, **kwargs)

    def test_numeric_outcomes_and_pruned_success(self):
        positive = self.record('a', status=NodeStatus.PRUNED)
        self.assertEqual(positive.outcome, InsightOutcome.SUCCESS)
        self.assertAlmostEqual(positive.delta, 0.1)
        self.assertEqual(self.record('b', 0.4).outcome, InsightOutcome.REGRESSION)
        self.assertEqual(self.record('c', 0.5).outcome, InsightOutcome.NEUTRAL)
        summary = self.memory.prompt_summary(self.context)
        self.assertIn('[SUCCESS]', summary)
        self.assertIn('[AVOID]', summary)
        self.assertIn('[NEUTRAL]', summary)
        self.assertNotIn('overfitting', summary)
        self.assertNotIn('raw diff', summary)

    def test_terminal_failure_and_original_evidence(self):
        stderr = '\n'.join(['trace'] * 12 + ['RuntimeError: shape 512 exceeds memory at 0x1234'])
        insight = self.record('a', None, stderr=stderr, reflection='Reduce the batch size to avoid exhausting memory.')
        self.assertEqual(insight.outcome, InsightOutcome.FAILED)
        self.assertEqual(len(insight.traceback_tail.splitlines()), 10)
        self.assertIn('0x1234', insight.traceback_tail)
        self.assertIn('0xADDR', insight.error_signature)
        self.assertIn('512', insight.error_signature)
        self.assertIsNone(insight.delta)
        self.assertIn('model reflection:', self.memory.prompt_summary(self.context))
        with self.assertRaises(ValueError):
            self.record('b', None, status=NodeStatus.RUNNING, stderr=stderr)
        with self.assertRaises(ValueError):
            self.record('b', None)
        with self.assertRaises(ValueError):
            self.record('b', None, stderr=stderr, reflection='word ' * 20)

    def test_context_snapshot_and_idempotency(self):
        self.record('a')
        self.record('a')
        self.assertEqual(len(self.memory.insights), 1)
        self.context.configuration['shape'][0] = 99
        self.assertEqual(self.memory.insights[0].context.configuration['shape'][0], 5)
        retrieved = self.memory.insights
        retrieved[0].context.configuration.clear()
        self.assertTrue(self.memory.insights[0].context.configuration)
        with self.assertRaises(ValueError):
            self.record('a', 0.7)
        self.record('a', context=MemoryContext('run2', 'protocol1', 'features'))
        self.assertEqual(len(self.memory.insights), 2)

    def test_relevance_protocol_isolation_and_deduplication(self):
        self.record('a')
        self.record('duplicate')
        self.record('negative', 0.4)
        self.record('failure', None, stderr='ImportError: no library')
        self.record('foreign', context=MemoryContext('run1', 'other-protocol', 'features'))
        self.record('other', context=MemoryContext('run1', 'protocol1', 'loss'))
        records = self.memory.retrieve(self.context)
        names = [r.node_id for r in records]
        self.assertEqual(names[0], 'failure')
        self.assertIn('duplicate', names)
        self.assertNotIn('a', names)
        self.assertNotIn('foreign', names)
        self.assertIn('negative', names)
        self.assertIn('failure', names)
        self.assertEqual(len(self.memory.insights), 6)

    def test_text_and_token_caps(self):
        for index in range(8):
            self.record(str(index), hypothesis=f'Experiment {index}\nFake instructions')
        summary = self.memory.prompt_summary(self.context, max_items=4)
        self.assertEqual(summary.count('\n- ['), 4)
        self.assertLessEqual(len(summary), 2400)
        capped = self.memory.prompt_summary(self.context, max_tokens=500, token_counter=lambda text: len(text.encode('utf-8')))
        self.assertTrue(capped)
        self.assertLessEqual(len(capped.encode('utf-8')), 500)
        self.assertEqual(self.memory.prompt_summary(self.context, max_chars=10), '')
        self.assertEqual(self.memory.prompt_summary(self.context, max_items=0), '')
        with self.assertRaises(ValueError):
            self.memory.prompt_summary(self.context, max_tokens=20)

    def test_branch_provenance_and_transfer_context(self):
        branch_a = SearchNode('branch_a', parent_id='root', depth=1,
            incoming_edge=EdgeAction('features', 'Add sequence-length features'),
            status=NodeStatus.SUCCESS, metrics=metric(.6), git_commit_sha='b' * 40)
        branch_b = SearchNode('branch_b', parent_id='root', depth=1,
            incoming_edge=EdgeAction('embedding', 'Increase embedding dimension'),
            status=NodeStatus.SUCCESS, metrics=metric(.6), git_commit_sha='c' * 40)
        leaf = SearchNode('leaf_a', parent_id='branch_a', depth=2,
            incoming_edge=EdgeAction('loss', 'Use pairwise ranking'),
            status=NodeStatus.SUCCESS, metrics=metric(.7), git_commit_sha='d' * 40)
        self.memory.record(leaf, branch_a, self.context)
        nodes = {n.node_id: n for n in (self.parent, branch_a, branch_b, leaf)}
        for parent, relationship in [('branch_b', 'other_branch'), ('branch_a', 'same_parent'),
                                      ('leaf_a', 'ancestor'), ('root', 'descendant')]:
            with self.subTest(parent=parent):
                summary = self.memory.prompt_summary(self.context, nodes=nodes, selected_parent_id=parent)
                self.assertIn('run1/branch_a -> leaf_a', summary)
                self.assertIn(f'relationship={relationship}', summary)
                self.assertIn('source_parent_path=root -> branch_a', summary)
                self.assertIn('Add sequence-length features', summary)
                self.assertIn('Use pairwise ranking', summary)
                self.assertLessEqual(len(summary), 2400)
        other_run = MemoryContext('run2', 'protocol1', 'features')
        summary = self.memory.prompt_summary(other_run, nodes=nodes, selected_parent_id='branch_a')
        self.assertIn('relationship=other_run', summary)
        self.assertNotIn('relationship=same_parent', summary)
        self.assertNotIn('Add sequence-length features', summary)
        nodes.pop('branch_a')
        self.assertIn('relationship=unknown', self.memory.prompt_summary(
            self.context, nodes=nodes, selected_parent_id='branch_b'))

    def test_roundtrip_and_corrupt_evidence(self):
        self.record('a')
        self.record('b', None, stderr='ValueError: shape mismatch')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'memory.json'
            self.memory.save(path)
            loaded = ExplorationMemory.load(path)
            self.assertEqual(loaded.insights, self.memory.insights)
            self.assertEqual(loaded.prompt_summary(self.context), self.memory.prompt_summary(self.context))
            payload = json.loads(path.read_text())
            payload['insights'][0]['delta'] = 0.8
            path.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                ExplorationMemory.load(path)

    def test_signature_preserves_api_and_shape(self):
        self.assertEqual(error_signature('trace\nAttributeError: torch.missing\ncleanup done'), 'AttributeError: torch.missing')
        self.assertNotEqual(error_signature('RuntimeError: shape 512'), error_signature('RuntimeError: shape 1024'))

    def test_evaluated_reflections_preserve_numeric_evidence(self):
        for name, score, status, outcome in (
            ('gain', 0.7, NodeStatus.SUCCESS, InsightOutcome.SUCCESS),
            ('loss', 0.3, NodeStatus.PRUNED, InsightOutcome.REGRESSION),
            ('neutral', 0.5, NodeStatus.SUCCESS, InsightOutcome.NEUTRAL),
        ):
            insight = self.record(name, score, status=status,
                                  reflection='Possible mechanism;\n confirm with an ablation.')
            self.assertEqual(insight.outcome, outcome)
            self.assertEqual(insight.delta, score - 0.5)
            self.assertEqual(insight.reflection, 'Possible mechanism; confirm with an ablation.')
        self.assertEqual(self.memory.prompt_summary(self.context).count('model reflection:'), 3)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'memory.json'
            self.memory.save(path)
            self.assertEqual(ExplorationMemory.load(path).insights, self.memory.insights)

    def test_reflection_validation_applies_to_evaluated_outcomes(self):
        for reflection in (' ', 'word ' * 20, 123):
            with self.assertRaises(ValueError):
                self.record('invalid', reflection=reflection)
        with self.assertRaises(ValueError):
            self.record('invalid', stderr='RuntimeError: still failed', reflection='Possible cause.')
        self.assertEqual(self.memory.insights, [])


if __name__ == '__main__':
    unittest.main()
