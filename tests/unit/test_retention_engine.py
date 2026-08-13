import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.retention.retention_engine import risk_tier


def test_risk_tiers():
    assert risk_tier(0.90) == "Critical"
    assert risk_tier(0.80) == "Critical"
    assert risk_tier(0.70) == "High"
    assert risk_tier(0.60) == "High"
    assert risk_tier(0.50) == "Medium"
    assert risk_tier(0.40) == "Medium"
    assert risk_tier(0.39) == "Low"
