"""Phase 6: leakage-safe customer churn feature engineering."""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "customer_churn_cleaned.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "customer_churn_features.csv"

TARGET = "Churn"
ID_COLUMN = "CustomerID"


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data = data.drop(columns=[ID_COLUMN], errors="ignore")

    data["support_calls_per_tenure"] = (
        data["Support Calls"] / data["Tenure"].clip(lower=1)
    )
    data["usage_per_tenure"] = (
        data["Usage Frequency"] / data["Tenure"].clip(lower=1)
    )
    data["spend_per_tenure"] = (
        data["Total Spend"] / data["Tenure"].clip(lower=1)
    )

    data["tenure_band"] = pd.cut(
        data["Tenure"],
        bins=[-float("inf"), 6, 12, 24, 48, float("inf")],
        labels=["0-6", "7-12", "13-24", "25-48", "49+"],
    )
    data["support_call_band"] = pd.cut(
        data["Support Calls"],
        bins=[-float("inf"), 2, 5, 8, float("inf")],
        labels=["0-2", "3-5", "6-8", "9+"],
    )
    data["payment_delay_band"] = pd.cut(
        data["Payment Delay"],
        bins=[-float("inf"), 0, 7, 14, 30, float("inf")],
        labels=["0", "1-7", "8-14", "15-30", "31+"],
    )
    data["usage_frequency_band"] = pd.cut(
        data["Usage Frequency"],
        bins=[-float("inf"), 5, 10, 20, 30, float("inf")],
        labels=["0-5", "6-10", "11-20", "21-30", "31+"],
    )

    if TARGET in data.columns:
        feature_columns = [c for c in data.columns if c != TARGET]
        data = data[feature_columns + [TARGET]]
    return data


if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)
    features = engineer_features(df)
    features.to_csv(OUTPUT_PATH, index=False)
    print(f"Input shape: {df.shape}")
    print(f"Feature dataset shape: {features.shape}")
    print(f"Output: {OUTPUT_PATH}")
