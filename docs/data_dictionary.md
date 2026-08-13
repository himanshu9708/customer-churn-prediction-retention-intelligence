# Data Dictionary

This is an initial dictionary based on the uploaded CSV. Definitions and cleaning decisions will be finalized after data inspection in the appropriate phases.

| Column | Type in raw CSV |
|---|---|
| `CustomerID` | `float64` |
| `Age` | `float64` |
| `Gender` | `object` |
| `Tenure` | `float64` |
| `Usage Frequency` | `float64` |
| `Support Calls` | `float64` |
| `Payment Delay` | `float64` |
| `Subscription Type` | `object` |
| `Contract Length` | `object` |
| `Total Spend` | `float64` |
| `Last Interaction` | `float64` |
| `Churn` | `float64` |

Target: `Churn` (0/1 in the observed non-null rows).
