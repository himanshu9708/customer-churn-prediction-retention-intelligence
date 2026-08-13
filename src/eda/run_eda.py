"""Reproducible Phase 4 exploratory data analysis."""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from src.config.settings import PROJECT_ROOT

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "customer_churn_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "eda_outputs"
NUMERIC_FEATURES = ["Age","Tenure","Usage Frequency","Support Calls","Payment Delay","Total Spend","Last Interaction"]
CATEGORICAL_FEATURES = ["Gender","Subscription Type","Contract Length"]

def load_data():
    return pd.read_csv(DATA_PATH)

def run_eda(df):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    counts = df["Churn"].value_counts().sort_index()
    counts.to_csv(OUTPUT_DIR / "churn_class_counts.csv", header=["count"])
    pd.DataFrame({"churn_rate":[df["Churn"].mean()], "non_churn_rate":[1-df["Churn"].mean()]}).to_csv(
        OUTPUT_DIR / "churn_class_balance.csv", index=False
    )

    plt.figure(figsize=(7,5))
    plt.bar(counts.index.astype(str), counts.values)
    plt.title("Customer Churn Distribution")
    plt.xlabel("Churn")
    plt.ylabel("Customer count")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "churn_distribution.png", dpi=160)
    plt.close()

    for column in NUMERIC_FEATURES:
        groups = [df.loc[df["Churn"] == value, column].dropna().values for value in [0,1]]
        plt.figure(figsize=(8,5))
        plt.boxplot(groups, labels=["0","1"])
        plt.title(f"{column} by Churn")
        plt.xlabel("Churn")
        plt.ylabel(column)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"{column.lower().replace(' ','_')}_by_churn.png", dpi=160)
        plt.close()

    for column in CATEGORICAL_FEATURES:
        rates = df.groupby(column)["Churn"].mean().sort_values(ascending=False)
        rates.to_csv(OUTPUT_DIR / f"{column.lower().replace(' ','_')}_churn_rate.csv", header=["churn_rate"])
        plt.figure(figsize=(8,5))
        plt.bar(rates.index.astype(str), rates.values)
        plt.ylabel("Churn rate")
        plt.title(f"Churn Rate by {column}")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"{column.lower().replace(' ','_')}_churn_rate.png", dpi=160)
        plt.close()

    corr = df[NUMERIC_FEATURES + ["Churn"]].corr(numeric_only=True)
    corr.to_csv(OUTPUT_DIR / "numeric_correlation_matrix.csv")
    plt.figure(figsize=(10,7))
    plt.imshow(corr.values, aspect="auto")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.index)), corr.index)
    plt.colorbar(label="Correlation")
    plt.title("Numeric Feature Correlation Matrix")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "numeric_correlation_heatmap.png", dpi=160)
    plt.close()

    df[NUMERIC_FEATURES].describe().T.to_csv(OUTPUT_DIR / "numeric_summary_statistics.csv")

if __name__ == "__main__":
    run_eda(load_data())
