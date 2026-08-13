# Phase 8 — Model Evaluation & Explainability

Run after Phase 7 training:

```bash
python -m src.evaluation.evaluate_models
```

The evaluator:

1. Recreates the same stratified 80/20 holdout using `random_state=42`.
2. Loads only trained model artifacts from `models/`.
3. Computes ROC-AUC and PR-AUC.
4. Evaluates precision, recall, and F1 at the default 0.50 threshold.
5. Generates a threshold table from 0.10 to 0.90.
6. Computes permutation importance on a bounded test sample.
7. Selects a champion candidate by PR-AUC, then ROC-AUC.

## Threshold policy

The 0.50 threshold is a baseline, not a final business decision. Retention campaigns have costs, so the final threshold should be selected using campaign capacity and the relative cost of false negatives versus false positives.

## Explainability

Permutation importance is model-agnostic and is used first. It measures how much predictive performance falls when a feature is shuffled. It should be interpreted as association with predictive performance, not causal importance.

SHAP can be added later if the selected model and environment support it.
