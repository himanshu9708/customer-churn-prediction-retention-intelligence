# Phase 10 — API & Dashboard Serving

## FastAPI

Start the API from the project root:

```bash
uvicorn api.main:app --reload
```

Health check:

```text
GET /health
```

Prediction endpoint:

```text
POST /api/v1/predict
```

The endpoint loads the Phase 8 champion model and applies the same Phase 6 feature definitions before scoring a customer.

Interactive API documentation is available at `/docs` while the server is running.

## Streamlit dashboard

First generate Phase 9 retention outputs:

```bash
python -m src.retention.retention_engine
```

Then start:

```bash
streamlit run dashboard/app.py
```

The dashboard shows total customers scored, High/Critical risk counts, average churn probability, risk-tier distribution, and the highest-priority retention customers.

## Production note

This phase provides a local serving prototype. Authentication, rate limiting, secret management, observability, model versioning, and deployment infrastructure are production-hardening tasks and are not claimed to be complete here.
