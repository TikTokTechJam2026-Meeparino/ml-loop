"""Define the prediction model (editable pipeline module).

Responsibilities:
- Implement a neural or tabular architecture, such as FM, DeepFM, or DCN.
- Consume inputs produced by features.py and hyperparameters from config.py.
- Expose serializable model state for inclusion in the single checkpoint file
  and support restoring it for inference without retraining or sidecar files.

Constraints:
- Produce one finite real-valued ranking score per input row, in input order.
- Higher scores must indicate stronger predicted relevance for long_view.
- Keep dataset splitting and authoritative evaluation outside this module.
- Keep architecture choices flexible; do not assume a particular ML framework.

The evaluation worker calls load_predictor(checkpoint_path), then predict(rows)
on the returned object. These entry points must retain their signatures.
Input rows are (date, user_id, video_id, author_id, tab, duration_ms), without
evaluation labels. Coordinate checkpoint serialization with train.py.

The specifications above and entry-point contracts below are authoritative.
The implementation below is a replaceable reference FM ported from the starter
kit, not a required architecture. NumPy, pickle, and FM-specific internal state
are reference choices; replacements must continue satisfying the contracts.
This reference implementation loads trusted pickle checkpoints only.
"""

# Reference implementation: replaceable while preserving the contracts above.
import pickle
import numpy as np
from features import transform

def sigmoid(x): return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))

class FM:
    def __init__(self, dim, k=16, lr=0.001, l2=1e-6, seed=0):
        rng = np.random.default_rng(seed)
        self.V = rng.normal(0, 0.01, (dim, k)).astype(np.float32)
        self.W = np.zeros(dim, dtype=np.float32)
        self.b = np.float32(0.0)
        self.lr, self.l2 = lr, l2
        self.mV = np.zeros_like(self.V); self.vV = np.zeros_like(self.V)
        self.mW = np.zeros_like(self.W); self.vW = np.zeros_like(self.W)
        self.t = 0

    def logits(self, X):
        E = self.V[X]                                   # (B,F,k)
        S = E.sum(1)                                    # (B,k)
        inter = 0.5 * ((S ** 2).sum(1) - (E ** 2).sum((1, 2)))
        return self.b + self.W[X].sum(1) + inter, E, S

    def step(self, X, y):
        B = len(y)
        z, E, S = self.logits(X)
        g = ((sigmoid(z) - y) / B).astype(np.float32)    # (B,)
        gV = np.zeros_like(self.V); gW = np.zeros_like(self.W)
        np.add.at(gW, X, g[:, None])
        np.add.at(gV, X, g[:, None, None] * (S[:, None, :] - E))
        gV += self.l2 * self.V; gW += self.l2 * self.W
        self.t += 1
        b1, b2, eps = 0.9, 0.999, 1e-8
        for P, G, M, Vv in ((self.V, gV, self.mV, self.vV), (self.W, gW, self.mW, self.vW)):
            M *= b1; M += (1 - b1) * G
            Vv *= b2; Vv += (1 - b2) * (G * G)
            P -= self.lr * (M / (1 - b1 ** self.t)) / (np.sqrt(Vv / (1 - b2 ** self.t)) + eps)
        self.b -= self.lr * g.sum()
        return float(-np.mean(y * np.log(sigmoid(z) + 1e-9) + (1 - y) * np.log(1 - sigmoid(z) + 1e-9)))

    def predict(self, X, bs=200_000):
        return np.concatenate([self.logits(X[i:i + bs])[0] for i in range(0, len(X), bs)])

def read_checkpoint(path):
    with open(path, 'rb') as stream:
        state = pickle.load(stream)
    if state.get('version') != 1:
        raise ValueError('unsupported checkpoint version')
    for key in ('config', 'features_state', 'model_state', 'training_state', 'context'):
        if key not in state:
            raise ValueError('missing checkpoint field: ' + key)
    return state


class Predictor:
    """Inference interface; implementation may use any model architecture."""

    def __init__(self, state):
        config = state['config']
        self.features = state['features_state']
        self.model = FM(self.features['dim'], k=config['k'], lr=config['lr'], l2=config['l2'], seed=config['seed'])
        weights = state['model_state']
        for name in ('V', 'W', 'b'):
            value = weights[name]
            if np.shape(value) != np.shape(getattr(self.model, name)) or not np.isfinite(value).all():
                raise ValueError('incompatible or nonfinite model weights: ' + name)
            setattr(self.model, name, value)

    def predict(self, rows):
        """Return one finite real-valued score per row, preserving input order.

        Rows contain prediction inputs only, not evaluation labels. Apply the
        preprocessing restored from the checkpoint without fitting it again.
        Do not train, write files, or modify the checkpoint during inference.
        """
        if not len(rows):
            return np.empty(0, dtype=np.float32)
        return self.model.predict(transform(rows, self.features))


def load_predictor(checkpoint_path):
    """Return an object implementing Predictor.predict(rows).

    Read the explicitly supplied checkpoint file and restore the selected model,
    fitted preprocessing, and effective configuration. Use the selected best
    weights for evaluation if the file also contains latest training state.
    Fail clearly if the file is missing, corrupt, or incompatible; do not fall
    back to random weights, retrain, or search other checkpoint paths.
    Loading must not create or modify any files, including caches or sidecars.
    Restore config, features_state, and model_state from the checkpoint
    dictionary (for example, one saved with torch.save). Report missing or
    incompatible contents clearly. Use a format appropriate to the model.
    """
    return Predictor(read_checkpoint(checkpoint_path))
