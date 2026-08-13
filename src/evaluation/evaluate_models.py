"""Phase 8: model evaluation, threshold analysis, and explainability."""
from pathlib import Path
import json
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "customer_churn_features.csv"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "model_evaluation"
RANDOM_STATE = 42


def load_test_data():
    """Recreate the deterministic Phase 7 holdout."""
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["Churn"])
    y = df["Churn"].astype(int)
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=RANDOM_STATE
    )
    return X_test, y_test


def threshold_table(y_true, probabilities):
    rows = []
    for threshold in np.arange(0.10, 0.91, 0.05):
        pred = (probabilities >= threshold).astype(int)
        rows.append({
            "threshold": round(float(threshold), 2),
            "precision": precision_score(y_true, pred, zero_division=0),
            "recall": recall_score(y_true, pred, zero_division=0),
            "f1": f1_score(y_true, pred, zero_division=0),
            "predicted_positive_rate": float(pred.mean()),
        })
    return pd.DataFrame(rows)


def evaluate_model(path, X_test, y_test):
    model = joblib.load(path)
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.50).astype(int)

    metrics = {
        "model": path.stem,
        "roc_auc": roc_auc_score(y_test, probabilities),
        "pr_auc": average_precision_score(y_test, probabilities),
        "precision_at_0_50": precision_score(y_test, predictions, zero_division=0),
        "recall_at_0_50": recall_score(y_test, predictions, zero_division=0),
        "f1_at_0_50": f1_score(y_test, predictions, zero_division=0),
        "confusion_matrix_at_0_50": confusion_matrix(y_test, predictions).tolist(),
    }

    threshold_table(y_test, probabilities).to_csv(
        OUTPUT_DIR / f"{path.stem}_thresholds.csv", index=False
    )

    with open(OUTPUT_DIR / f"{path.stem}_evaluation.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Permutation importance on a bounded test sample keeps evaluation practical.
    sample_size = min(10000, len(X_test))
    sample = X_test.sample(sample_size, random_state=RANDOM_STATE)
    y_sample = y_test.loc[sample.index]

    importance = permutation_importance(
        model,
        sample,
        y_sample,
        scoring="roc_auc",
        n_repeats=3,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    names = sample.columns
    importance_df = pd.DataFrame({
        "feature": names,
        "importance_mean": importance.importances_mean,
        "importance_std": importance.importances_std,
    }).sort_values("importance_mean", ascending=False)

    importance_df.to_csv(
        OUTPUT_DIR / f"{path.stem}_permutation_importance.csv", index=False
    )

    return metrics


def main():
    warnings.filterwarnings("ignore")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    X_test, y_test = load_test_data()
    model_paths = sorted(MODEL_DIR.glob("*.joblib"))

    if not model_paths:
        raise FileNotFoundError(
            "No trained model artifacts found. Run Phase 7 first: "
            "python -m src.models.train_models"
        )

    results = []
    for path in model_paths:
        results.append(evaluate_model(path, X_test, y_test))

    comparison = pd.DataFrame(results).sort_values(
        ["pr_auc", "roc_auc"], ascending=False
    )
    comparison.to_csv(OUTPUT_DIR / "evaluation_comparison.csv", index=False)

    champion = comparison.iloc[0]["model"]
    (OUTPUT_DIR / "champion_model.txt").write_text(
        f"{champion}\nSelection priority: PR-AUC, then ROC-AUC.\n",
        encoding="utf-8",
    )

    print(comparison.to_string(index=False))
    print(f"\nChampion candidate: {champion}")
    print(f"Reports written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
