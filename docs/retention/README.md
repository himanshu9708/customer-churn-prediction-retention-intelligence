# Phase 9 — Retention Intelligence

Convert champion-model churn probabilities into operational retention priorities.

## Risk tiers

- Critical: >= 0.80
- High: 0.60–0.79
- Medium: 0.40–0.59
- Low: < 0.40

These are initial operating thresholds, not proven optimal business cutoffs.

## Intervention rules

- High support calls → proactive service recovery
- High payment delay → billing/payment assistance
- Monthly contract → contract-retention offer
- Low usage → product-engagement campaign
- Short tenure → onboarding intervention
- Multiple signals → multi-factor intervention

These recommendations are transparent rules, not causal claims.

## Run

```bash
python -m src.models.train_models
python -m src.evaluation.evaluate_models
python -m src.retention.retention_engine
```

Outputs are written to `docs/retention/`.
