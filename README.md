# Customer Churn Prediction & Retention Intelligence

End-to-end Data Science + ML Engineering project built in phases.

## Business goal

Predict customer churn probability and convert the prediction into:

**Prediction → Risk → Reason → Retention Action**

The project follows the architecture and development rules defined in the provided project specification. Phase 1 intentionally does **not** implement data cleaning, EDA, SQL, feature engineering, model training, API, or dashboard logic.

## Phase 1 completed

- Repository structure
- Basic configuration
- Simple logger
- `.gitignore`
- `.env.example`
- `requirements.txt`
- `pyproject.toml`
- README
- Placeholder modules
- Uploaded CSV placed in `data/raw/`

## Uploaded dataset

- Rows: 440,833
- Columns: 12
- Target: `Churn`
- Raw columns: CustomerID, Age, Gender, Tenure, Usage Frequency, Support Calls, Payment Delay, Subscription Type, Contract Length, Total Spend, Last Interaction, Churn

## Architecture

```text
Raw Customer Data
      ↓
Python / Pandas
      ↓
Data Cleaning
      ↓
EDA
      ↓
SQL Database
      ↓
Feature Engineering
      ↓
Train/Test Split
      ↓
ML Pipeline
      ↓
Logistic Regression / Random Forest / XGBoost
      ↓
Model Evaluation
      ↓
Churn Probability
      ↓
Risk Segmentation
      ↓
Retention Recommendation
      ↓
FastAPI
      ↓
Streamlit
      ↓
Docker / Deployment
```

## Important rule

Do not claim a model is best before evaluation. Do not use test data for training. Do not treat correlation or model explanations as causation.

## Run later

Create a Python 3.11+ virtual environment and install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows activation:

```powershell
.venv\Scripts\activate
```

The actual data pipeline starts in Phase 2.

## Development workflow

Each phase should be committed separately with a meaningful commit message. Continue to the next phase only after the current phase has been validated.

## Phase 3
Data cleaning has been implemented and validated against the uploaded CSV.

## Testing

Run the full test suite:

```bash
pytest -q
```

Run the structural validation:

```bash
sh scripts/check_project.sh
```

GitHub Actions runs these checks automatically for pushes and pull requests to `main`.


# Customer Churn Prediction & Retention Intelligence

## What this project does

This project builds an end-to-end customer churn system that goes beyond binary churn prediction. It:

1. Ingests and validates customer data.
2. Cleans and analyzes the dataset.
3. Engineers leakage-safe features.
4. Trains Logistic Regression, Random Forest and XGBoost models.
5. Evaluates models using ROC-AUC, PR-AUC, precision, recall and F1.
6. Selects a champion model.
7. Converts churn probabilities into customer risk tiers.
8. Generates transparent retention recommendations.
9. Serves predictions through FastAPI.
10. Presents retention priorities through Streamlit.
11. Provides Docker-based local deployment.
12. Runs automated tests through GitHub Actions.

## Quick start

```bash
pip install -r requirements.txt
sh scripts/check_project.sh
pytest -q
python scripts/run_pipeline.py
```

## Run the application

API:

```bash
uvicorn api.main:app --reload
```

Dashboard:

```bash
streamlit run dashboard/app.py
```

Docker:

```bash
docker compose build
docker compose up
```

## Project architecture

See `docs/architecture/README.md`.

## Reproducibility

See `docs/project/REPRODUCIBILITY.md`.

## Important modeling notes

- Accuracy is not used as the sole model-selection criterion.
- PR-AUC and recall are emphasized because the business objective is retention.
- Test data is kept separate from fitting and preprocessing.
- Risk thresholds are operating assumptions and should be calibrated with real campaign economics.
- Retention recommendations are transparent rules, not causal claims.

## Current scope

This repository is a local, reproducible ML application prototype. Full enterprise production deployment would additionally require authentication, secrets management, monitoring, model registry/versioning, CI/CD deployment, TLS, scaling, database migrations and operational controls.
