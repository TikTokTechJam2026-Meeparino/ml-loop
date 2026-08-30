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
The exact input-row schema and checkpoint serialization format remain to be set.
"""


class Predictor:
    """Inference interface; implementation may use any model architecture."""

    def predict(self, rows):
        """Return one finite real-valued score per row, preserving input order.

        Rows contain prediction inputs only, not evaluation labels. Apply the
        preprocessing restored from the checkpoint without fitting it again.
        Do not train, write files, or modify the checkpoint during inference.
        """
        raise NotImplementedError("Implement prediction using restored model state")


def load_predictor(checkpoint_path):
    """Return an object implementing Predictor.predict(rows).

    Read the explicitly supplied checkpoint file and restore the selected model,
    fitted preprocessing, and effective configuration. Use the selected best
    weights for evaluation if the file also contains latest training state.
    Fail clearly if the file is missing, corrupt, or incompatible; do not fall
    back to random weights, retrain, or search other checkpoint paths.
    Loading must not create or modify any files, including caches or sidecars.
    """
    raise NotImplementedError("Implement checkpoint loading for inference")
