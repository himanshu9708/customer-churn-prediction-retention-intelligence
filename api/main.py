from fastapi import FastAPI

from api.routes.predictions import router as predictions_router

app = FastAPI(
    title="Customer Churn Retention Intelligence API",
    version="1.0.0",
    description="Prediction and retention-priority serving layer.",
)

app.include_router(predictions_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
