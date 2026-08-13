# Cleaning Decisions

## Phase 3 decisions

- Preserve the raw CSV unchanged.
- Remove exact duplicate rows.
- Strip surrounding whitespace from categorical values.
- Convert numeric fields explicitly; invalid numeric values become missing.
- Remove rows with missing `Churn`; the target cannot be safely inferred.
- Impute missing numeric feature values with the median.
- Impute missing categorical feature values with the mode.
- Retain `CustomerID` for identification, but exclude it from future model features.

## Actual result

- Raw rows: 440,833
- Cleaned rows: 440,832
- Rows removed: 1
- Duplicate rows removed: 0
- Missing-target rows removed: 1
- Missing values remaining: 0
- Duplicate rows remaining: 0

### Methodology note

For model training, imputation should ultimately be fitted inside the ML pipeline using training data only. The simple cleaning here is for establishing a clean analytical dataset; later model preparation will prevent leakage.
