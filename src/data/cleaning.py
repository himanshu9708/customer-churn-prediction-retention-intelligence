"""Data cleaning functions for the customer churn dataset."""
import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

TEXT_COLUMNS = ["Gender", "Subscription Type", "Contract Length"]
NUMERIC_COLUMNS = [
    "CustomerID", "Age", "Tenure", "Usage Frequency",
    "Support Calls", "Payment Delay", "Total Spend", "Last Interaction"
]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw churn data without modifying the input dataframe."""
    cleaned = df.copy()

    for column in TEXT_COLUMNS:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned["Churn"] = pd.to_numeric(cleaned["Churn"], errors="coerce")

    duplicate_count = int(cleaned.duplicated().sum())
    cleaned = cleaned.drop_duplicates().copy()

    missing_target_count = int(cleaned["Churn"].isna().sum())
    cleaned = cleaned.dropna(subset=["Churn"]).copy()

    feature_numeric = [c for c in NUMERIC_COLUMNS if c != "CustomerID"]
    for column in feature_numeric:
        if cleaned[column].isna().any():
            cleaned[column] = cleaned[column].fillna(cleaned[column].median())

    for column in TEXT_COLUMNS:
        if cleaned[column].isna().any():
            mode = cleaned[column].mode(dropna=True)
            if mode.empty:
                raise ValueError(f"No value available to impute {column}.")
            cleaned[column] = cleaned[column].fillna(mode.iloc[0])

    cleaned["CustomerID"] = cleaned["CustomerID"].astype("Int64")
    cleaned["Churn"] = cleaned["Churn"].astype(int)

    logger.info(
        "Cleaning complete: removed %s duplicates and %s missing-target rows.",
        duplicate_count, missing_target_count
    )
    return cleaned
