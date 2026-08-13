import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from api.routes.predictions import risk_tier, recommendation


def test_api_risk_tier():
    assert risk_tier(0.85) == "Critical"
    assert risk_tier(0.65) == "High"
    assert risk_tier(0.45) == "Medium"
    assert risk_tier(0.20) == "Low"


def test_recommendation_for_high_support_calls():
    payload = {
        "support_calls": 8,
        "payment_delay": 0,
        "contract_length": "Yearly",
        "usage_frequency": 20,
        "tenure": 20,
    }
    reason, action = recommendation(payload)
    assert "support-call" in reason
    assert "service recovery" in action
