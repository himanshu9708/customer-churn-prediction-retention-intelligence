from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(ge=0)
    gender: str
    tenure: int = Field(ge=0)
    usage_frequency: int = Field(ge=0)
    support_calls: int = Field(ge=0)
    payment_delay: int = Field(ge=0)
    subscription_type: str
    contract_length: str
    total_spend: float = Field(ge=0)
    last_interaction: int = Field(ge=0)


class PredictionResponse(BaseModel):
    churn_probability: float
    risk_tier: str
    recommended_action: str
    risk_reason: str
    retention_priority_score: float
