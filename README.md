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
