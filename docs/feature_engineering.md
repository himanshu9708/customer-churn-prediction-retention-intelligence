# Phase 6 — Feature Engineering

## Objective

Create ML-ready predictors from the cleaned customer dataset without using the target to construct features.

## Identifier and target

- `CustomerID` is excluded from the predictor matrix because it is an identifier.
- `Churn` remains the target and is never used to calculate predictors.

## Engineered numerical features

| Feature | Definition |
|---|---|
| `support_calls_per_tenure` | Support Calls / max(Tenure, 1) |
| `usage_per_tenure` | Usage Frequency / max(Tenure, 1) |
| `spend_per_tenure` | Total Spend / max(Tenure, 1) |

## Engineered categorical bands

- `tenure_band`: 0-6, 7-12, 13-24, 25-48, 49+
- `support_call_band`: 0-2, 3-5, 6-8, 9+
- `payment_delay_band`: 0, 1-7, 8-14, 15-30, 31+
- `usage_frequency_band`: 0-5, 6-10, 11-20, 21-30, 31+

## Leakage policy

No target-derived encoding, target mean encoding, future information, or post-outcome variables are introduced. Train/test splitting and learned preprocessing will be handled later using training data only.

## Output

`data/processed/customer_churn_features.csv`
