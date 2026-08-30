"""Declare candidate hyperparameters (editable pipeline module).

Responsibilities:
- Centralize learning rate, batch size, embedding dimensions, optimizer/loss
  settings, epoch limits, early-stopping settings, and random seed.
- Keep effective settings explicit and serializable for experiment records.

Constraints:
- Do not load data, train models, or write artifacts when imported.
- Do not embed credentials or machine-specific absolute paths.
- Dataset splits, target definitions, evaluation metrics, and runner-enforced
  resource limits are fixed externally and must not be overridden here.
- Keep architecture-specific settings flexible as the pipeline evolves.

DEFAULTS are overridden by explicit Runner.run(overrides=...) values.

The specifications above are authoritative. The implementation below provides
replaceable reference FM hyperparameters and validation, not a fixed search
space. Settings may evolve with the model while preserving these constraints.
"""

# Reference implementation: replaceable while preserving the contracts above.
import math

DEFAULTS = dict(k=16, lr=0.001, l2=1e-6, epochs=40, bs=8192, patience=4, seed=0)


def resolve(overrides):
    if set(overrides) - DEFAULTS.keys():
        raise ValueError('unknown configuration keys')
    config = {**DEFAULTS, **overrides}
    for key in ('k', 'epochs', 'bs', 'patience', 'seed'):
        value = config[key]
        if type(value) is not int or value < (0 if key == 'seed' else 1):
            raise ValueError(f'invalid {key}')
    for key in ('lr', 'l2'):
        if not math.isfinite(config[key]) or config[key] < 0 or (key == 'lr' and config[key] == 0):
            raise ValueError(f'invalid {key}')
    return config
