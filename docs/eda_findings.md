# Phase 4 — EDA Findings

- Rows: 440,832
- Columns: 12
- Churn rate: 56.71%
- Non-churn rate: 43.29%

## Numeric correlations with Churn

- `Support Calls`: 0.5743
- `Payment Delay`: 0.3121
- `Age`: 0.2184
- `Last Interaction`: 0.1496
- `Usage Frequency`: -0.0461
- `Tenure`: -0.0519
- `Total Spend`: -0.4294

## Categorical churn rates

### Gender
- `Female`: 66.67%
- `Male`: 49.13%

### Subscription Type
- `Basic`: 58.18%
- `Standard`: 56.07%
- `Premium`: 55.94%

### Contract Length
- `Monthly`: 100.00%
- `Annual`: 46.08%
- `Quarterly`: 46.03%

## Interpretation

These are descriptive associations, not causal effects. Monthly contract length has 100% observed churn in this dataset and should be investigated for data-quality/business-rule reasons before model interpretation.
