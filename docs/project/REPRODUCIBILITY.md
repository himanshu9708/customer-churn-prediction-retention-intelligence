# Reproducibility Guide

## 1. Environment

Use Python 3.12.

Create/activate your environment, then:

```bash
pip install -r requirements.txt
```

## 2. Validate the repository

```bash
sh scripts/check_project.sh
pytest -q
```

## 3. Run the pipeline

From the project root:

```bash
python scripts/run_pipeline.py
```

The orchestrator calls the existing ingestion, cleaning, training, evaluation and retention modules in order.

## 4. Start the API

```bash
uvicorn api.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 5. Start the dashboard

```bash
streamlit run dashboard/app.py
```

## 6. Docker

```bash
docker compose build
docker compose up
```

## Reproducibility controls

- Random seed: `42`
- Stratified test split: `20%`
- Five-fold stratified cross-validation
- Model preprocessing is inside sklearn pipelines
- Model comparison prioritizes PR-AUC and then ROC-AUC
- Risk thresholds are explicitly defined in the retention engine

## Important

The pipeline assumes the expected project data files and model dependencies are available. It does not download external data automatically.
