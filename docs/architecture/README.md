# System Architecture

## End-to-end flow

```text
Raw Customer CSV
      |
      v
Data Ingestion
      |
      v
Data Validation / Cleaning
      |
      v
EDA
      |
      v
Feature Engineering
      |
      v
Stratified Train/Test Split
      |
      +------------------------------+
      |                              |
      v                              v
Logistic Regression           Random Forest / XGBoost
      |                              |
      +--------------+---------------+
                     v
             Model Evaluation
                     |
                     v
              Champion Model
                     |
                     v
             Churn Probability
                     |
                     v
              Risk Tiering
                     |
                     v
         Retention Recommendations
               /            \
              v              v
        FastAPI API      Streamlit
                              Dashboard
```

## Phase responsibilities

| Phase | Responsibility |
|---|---|
| 1–3 | Project setup, ingestion, validation and cleaning |
| 4 | Exploratory data analysis |
| 5–6 | Data preparation and feature engineering |
| 7 | Model training |
| 8 | Evaluation and explainability |
| 9 | Retention intelligence |
| 10 | API and dashboard |
| 11 | Docker/local productionization |
| 12 | Automated testing and CI |
| 13 | Integration, reproducibility and documentation |

## Data and model boundaries

- `Churn` is the prediction target.
- `CustomerID` is an identifier and is not a predictor.
- Test data is held out from model fitting.
- Preprocessing is implemented inside model pipelines.
- Retention recommendations are rule-based and should not be interpreted as causal conclusions.
