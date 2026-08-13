from pathlib import Path

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException

from api.schemas import PredictionRequest, PredictionResponse

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "models"
EVAL_DIR = PROJECT_ROOT / "docs" / "model_evaluation"

router = APIRouter(tags=["predictions"])


def get_model():
    champion_file = EVAL_DIR / "champion_model.txt"
    if not champion_file.exists():
        raise HTTPException(
            status_code=503,
            detail="Champion model not selected. Run Phase 7 training and Phase 8 evaluation.",
        )
    champion = champion_file.read_text(encoding="utf-8").splitlines()[0].strip()
    path = MODEL_DIR / f"{champion}.joblib"
    if not path.exists():
        raise HTTPException(status_code=503, detail=f"Model artifact not found: {path.name}")
    return champion, joblib.load(path)


def risk_tier(probability: float) -> str:
    if probability >= 0.80:
        return "Critical"
    if probability >= 0.60:
        return "High"
    if probability >= 0.40:
        return "Medium"
    return "Low"


def recommendation(payload: dict) -> tuple[str, str]:
    reasons, actions = [], []
    if payload["support_calls"] >= 6:
        reasons.append("high support-call volume")
        actions.append("proactive service recovery")
    if payload["payment_delay"] >= 15:
        reasons.append("high payment delay")
        actions.append("billing/payment assistance")
    if payload["contract_length"] == "Monthly":
        reasons.append("monthly contract")
        actions.append("contract-retention offer")
    if payload["usage_frequency"] <= 10:
        reasons.append("low usage frequency")
        actions.append("product-engagement campaign")
    if payload["tenure"] <= 6:
        reasons.append("short tenure")
        actions.append("onboarding intervention")
    if not actions:
        actions.append("standard retention outreach")
    return (
        "; ".join(reasons) if reasons else "no dominant rule-based risk signal",
        "; ".join(actions),
    )


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    champion, model = get_model()
    payload = request.model_dump()

    row = pd.DataFrame([{
        "Age": payload["age"],
        "Gender": payload["gender"],
        "Tenure": payload["tenure"],
        "Usage Frequency": payload["usage_frequency"],
        "Support Calls": payload["support_calls"],
        "Payment Delay": payload["payment_delay"],
        "Subscription Type": payload["subscription_type"],
        "Contract Length": payload["contract_length"],
        "Total Spend": payload["total_spend"],
        "Last Interaction": payload["last_interaction"],
        # Phase 6 engineered predictors:
        "support_calls_per_tenure": payload["support_calls"] / max(payload["tenure"], 1),
        "usage_per_tenure": payload["usage_frequency"] / max(payload["tenure"], 1),
        "spend_per_tenure": payload["total_spend"] / max(payload["tenure"], 1),
        "tenure_band": pd.cut(
            [payload["tenure"]], [-float("inf"), 6, 12, 24, 48, float("inf")],
            labels=["0-6", "7-12", "13-24", "25-48", "49+"]
        )[0],
        "support_call_band": pd.cut(
            [payload["support_calls"]], [-float("inf"), 2, 5, 8, float("inf")],
            labels=["0-2", "3-5", "6-8", "9+"]
        )[0],
        "payment_delay_band": pd.cut(
            [payload["payment_delay"]], [-float("inf"), 0, 7, 14, 30, float("inf")],
            labels=["0", "1-7", "8-14", "15-30", "31+"]
        )[0],
        "usage_frequency_band": pd.cut(
            [payload["usage_frequency"]], [-float("inf"), 5, 10, 20, 30, float("inf")],
            labels=["0-5", "6-10", "11-20", "21-30", "31+"]
        )[0],
    }])

    probability = float(model.predict_proba(row)[:, 1][0])
    tier = risk_tier(probability)
    reason, action = recommendation(payload)

    return PredictionResponse(
        churn_probability=round(probability, 6),
        risk_tier=tier,
        recommended_action=action,
        risk_reason=reason,
        retention_priority_score=round(probability * 100, 2),
    )
