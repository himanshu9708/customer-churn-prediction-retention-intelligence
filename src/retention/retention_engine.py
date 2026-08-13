"""Phase 9: convert churn probabilities into retention intelligence."""
from pathlib import Path
import json
import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "customer_churn_features.csv"
RAW_PATH = PROJECT_ROOT / "data" / "processed" / "customer_churn_cleaned.csv"
MODEL_DIR = PROJECT_ROOT / "models"
EVAL_DIR = PROJECT_ROOT / "docs" / "model_evaluation"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "retention"

RISK_THRESHOLDS = {"critical": 0.80, "high": 0.60, "medium": 0.40}

def risk_tier(p):
    if p >= RISK_THRESHOLDS["critical"]: return "Critical"
    if p >= RISK_THRESHOLDS["high"]: return "High"
    if p >= RISK_THRESHOLDS["medium"]: return "Medium"
    return "Low"

def intervention(row):
    reasons, actions = [], []
    if row["Support Calls"] >= 6:
        reasons.append("high support-call volume"); actions.append("proactive service recovery")
    if row["Payment Delay"] >= 15:
        reasons.append("high payment delay"); actions.append("billing/payment assistance")
    if row["Contract Length"] == "Monthly":
        reasons.append("monthly contract"); actions.append("contract-retention offer")
    if row["Usage Frequency"] <= 10:
        reasons.append("low usage frequency"); actions.append("product-engagement campaign")
    if row["Tenure"] <= 6:
        reasons.append("short tenure"); actions.append("onboarding intervention")
    if not actions:
        actions.append("standard retention outreach")
    return pd.Series({
        "risk_reason": "; ".join(reasons) if reasons else "no dominant rule-based risk signal",
        "recommended_action": "; ".join(actions),
        "intervention_priority": "multi-factor intervention" if len(actions) > 1 else actions[0],
    })

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    champion_file = EVAL_DIR / "champion_model.txt"
    if not champion_file.exists():
        raise FileNotFoundError("Run Phase 8 first to select the champion model.")
    champion = champion_file.read_text(encoding="utf-8").splitlines()[0].strip()
    model_path = MODEL_DIR / f"{champion}.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"Missing model artifact: {model_path}. Run Phase 7 training.")

    df = pd.read_csv(DATA_PATH)
    model = joblib.load(model_path)
    X = df.drop(columns=["Churn"])
    probabilities = model.predict_proba(X)[:, 1]

    output = df.copy()
    if RAW_PATH.exists():
        ids = pd.read_csv(RAW_PATH, usecols=["CustomerID"])["CustomerID"]
        if len(ids) == len(output):
            output.insert(0, "CustomerID", ids)

    output["churn_probability"] = probabilities
    output["risk_tier"] = output["churn_probability"].map(risk_tier)
    output = pd.concat([output, output.apply(intervention, axis=1)], axis=1)
    output["retention_priority_score"] = (output["churn_probability"] * 100).round(2)
    output = output.sort_values(["churn_probability", "Support Calls", "Payment Delay"], ascending=False)
    output.to_csv(OUTPUT_DIR / "customer_retention_priorities.csv", index=False)

    summary = output.groupby("risk_tier", observed=True).agg(
        customers=("churn_probability", "size"),
        avg_churn_probability=("churn_probability", "mean"),
    ).reset_index()
    summary["avg_churn_probability"] = summary["avg_churn_probability"].round(4)
    summary.to_csv(OUTPUT_DIR / "risk_tier_summary.csv", index=False)

    output.groupby("recommended_action", observed=True).size().reset_index(
        name="customers"
    ).sort_values("customers", ascending=False).to_csv(
        OUTPUT_DIR / "recommended_action_summary.csv", index=False
    )

    (OUTPUT_DIR / "retention_metadata.json").write_text(json.dumps({
        "champion_model": champion,
        "risk_thresholds": RISK_THRESHOLDS,
        "rows_scored": len(output),
        "recommendation_type": "transparent rule-based intervention",
        "probability_source": "Phase 8 champion model",
    }, indent=2), encoding="utf-8")

    print(f"Champion model: {champion}")
    print(f"Customers scored: {len(output):,}")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
