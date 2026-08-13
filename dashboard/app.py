import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
RETENTION = ROOT / "docs" / "retention"

st.set_page_config(page_title="Customer Churn Retention Intelligence", layout="wide")
st.title("Customer Churn Retention Intelligence")

summary_path = RETENTION / "risk_tier_summary.csv"
priority_path = RETENTION / "customer_retention_priorities.csv"

if not summary_path.exists() or not priority_path.exists():
    st.warning(
        "Retention outputs are not available yet. Run Phase 9 first: "
        "`python -m src.retention.retention_engine`."
    )
    st.stop()

summary = pd.read_csv(summary_path)
customers = pd.read_csv(priority_path)

c1, c2, c3 = st.columns(3)
c1.metric("Customers scored", f"{len(customers):,}")
c2.metric("High + Critical", f"{customers['risk_tier'].isin(['High', 'Critical']).sum():,}")
c3.metric("Average churn probability", f"{customers['churn_probability'].mean():.1%}")

st.subheader("Risk distribution")
st.dataframe(summary, use_container_width=True)

st.subheader("Highest-priority customers")
columns = [
    "CustomerID", "churn_probability", "risk_tier",
    "risk_reason", "recommended_action", "retention_priority_score",
]
available = [c for c in columns if c in customers.columns]
st.dataframe(customers[available].head(100), use_container_width=True)

st.caption(
    "Risk tiers and interventions are operating rules from Phase 9. "
    "They should be validated against real retention outcomes."
)
