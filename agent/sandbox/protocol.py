"""Fixed starter-kit contract, outside the editable candidate workspace.

Rows: (date, user_id, video_id, author_id, tab, duration_ms, long_view).
Prediction inputs are the first six columns only. This is the supplied
starter-kit protocol, not an independently verified official benchmark.
"""
import importlib.util
from pathlib import Path

STARTER = Path(__file__).resolve().parents[2] / 'data/kuairand-pure/starter-kit'


def reference(name):
    spec = importlib.util.spec_from_file_location('_fixed_' + name, STARTER / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load(data_dir):
    # Evaluation itself is stdlib-only; candidates need not install NumPy just
    # to access the fixed evaluator. Raw loading stays in the agent process.
    return reference('data').load(data_dir)


evaluate = reference('evaluate').evaluate
