# Data

The uploaded training CSV is stored at:

`data/raw/customer_churn_dataset-training-master.csv`

Phase 1 only initializes the repository. No cleaning, imputation, feature engineering, or model training has been performed yet.

## Current dataset snapshot

- Rows: 440,833
- Columns: 12
- Target column: `Churn`
- Columns:
- `CustomerID`
- `Age`
- `Gender`
- `Tenure`
- `Usage Frequency`
- `Support Calls`
- `Payment Delay`
- `Subscription Type`
- `Contract Length`
- `Total Spend`
- `Last Interaction`
- `Churn`

The raw file contains one missing value in each column, including the target. These issues will be handled explicitly in the data-cleaning phase rather than silently changed during initialization.
