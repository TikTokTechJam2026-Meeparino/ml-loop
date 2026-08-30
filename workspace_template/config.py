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

Configuration schema and override precedence await the runner contract.
"""
