"""Validate the raw customer churn dataset."""
from typing import Any

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "CustomerID", "Age", "Gender", "Tenure", "Usage Frequency",
    "Support Calls", "Payment Delay", "Subscription Type",
    "Contract Length", "Total Spend", "Last Interaction", "Churn",
]

EXPECTED_NUMERIC_COLUMNS = [
    "CustomerID", "Age", "Tenure", "Usage Frequency", "Support Calls",
    "Payment Delay", "Total Spend", "Last Interaction", "Churn",
]

EXPECTED_CATEGORICAL_COLUMNS = [
    "Gender", "Subscription Type", "Contract Length",
]


def validate_columns(df: pd.DataFrame) -> None:
    """Check that all project-required columns are present."""
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def validate_data_types(df: pd.DataFrame) -> None:
    """Check that raw fields have compatible data types."""
    for column in EXPECTED_NUMERIC_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise TypeError(f"Column '{column}' should be numeric, found {df[column].dtype}.")

    for column in EXPECTED_CATEGORICAL_COLUMNS:
        if not pd.api.types.is_object_dtype(df[column]):
            raise TypeError(f"Column '{column}' should be text-like, found {df[column].dtype}.")


def validate_target_values(df: pd.DataFrame) -> None:
    """Check that observed non-null churn labels are binary."""
    values = set(df["Churn"].dropna().unique())
    if not values.issubset({0, 1}):
        raise ValueError(f"Unexpected Churn values: {sorted(values)}. Expected only 0 and 1.")


def get_validation_report(df: pd.DataFrame) -> dict[str, Any]:
    """Return validation findings without changing the raw dataframe."""
    validate_columns(df)
    validate_data_types(df)
    validate_target_values(df)

    missing_values = df.isna().sum()
    report = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_value_columns": {
            column: int(count) for column, count in missing_values.items() if count > 0
        },
        "duplicate_rows": int(df.duplicated().sum()),
        "churn_values": sorted(df["Churn"].dropna().unique().tolist()),
        "status": "passed",
    }
    logger.info(
        "Validation passed: %s rows, %s columns, %s duplicate rows.",
        report["row_count"], report["column_count"], report["duplicate_rows"]
    )
    return report
