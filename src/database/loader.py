"""Load cleaned churn data into PostgreSQL."""
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from src.config.settings import PROJECT_ROOT

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "customer_churn_cleaned.csv"
DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/churn_db"


def load_cleaned_data(path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load the Phase 3 cleaned dataset."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found: {path}")
    return pd.read_csv(path)


def prepare_for_sql(df: pd.DataFrame) -> pd.DataFrame:
    """Map Python column names to the SQL schema."""
    return df.rename(columns={
        "CustomerID": "customer_id",
        "Age": "age",
        "Gender": "gender",
        "Tenure": "tenure",
        "Usage Frequency": "usage_frequency",
        "Support Calls": "support_calls",
        "Payment Delay": "payment_delay",
        "Subscription Type": "subscription_type",
        "Contract Length": "contract_length",
        "Total Spend": "total_spend",
        "Last Interaction": "last_interaction",
        "Churn": "churn",
    })[
        [
            "customer_id", "age", "gender", "tenure", "usage_frequency",
            "support_calls", "payment_delay", "subscription_type",
            "contract_length", "total_spend", "last_interaction", "churn",
        ]
    ]


def load_to_postgres(
    database_url: str = DEFAULT_DATABASE_URL,
    replace: bool = True,
) -> int:
    """Create the table and load the cleaned dataset."""
    df = prepare_for_sql(load_cleaned_data())
    engine = create_engine(database_url)

    with engine.begin() as connection:
        schema_path = PROJECT_ROOT / "sql" / "schema.sql"
        connection.execute(text(schema_path.read_text(encoding="utf-8")))

    df.to_sql(
        "customers",
        engine,
        if_exists="replace" if replace else "append",
        index=False,
        method="multi",
        chunksize=5000,
    )

    return len(df)


if __name__ == "__main__":
    rows = load_to_postgres()
    print(f"Loaded {rows:,} customers into PostgreSQL.")
