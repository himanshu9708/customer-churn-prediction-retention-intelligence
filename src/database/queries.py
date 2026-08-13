"""Reusable SQL analytics for the churn database."""
from sqlalchemy import create_engine, text

from src.database.loader import DEFAULT_DATABASE_URL


def get_churn_summary(database_url: str = DEFAULT_DATABASE_URL) -> dict:
    engine = create_engine(database_url)
    query = text("""
        SELECT
            COUNT(*) AS customers,
            SUM(churn) AS churned_customers,
            AVG(churn) AS churn_rate
        FROM customers
    """)
    with engine.connect() as connection:
        row = connection.execute(query).mappings().one()
    return dict(row)


def get_churn_by_contract(database_url: str = DEFAULT_DATABASE_URL):
    engine = create_engine(database_url)
    query = text("""
        SELECT contract_length,
               COUNT(*) AS customers,
               SUM(churn) AS churned_customers,
               AVG(churn) AS churn_rate
        FROM customers
        GROUP BY contract_length
        ORDER BY churn_rate DESC
    """)
    with engine.connect() as connection:
        return [dict(row) for row in connection.execute(query).mappings().all()]
