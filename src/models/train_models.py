"""Phase 7: leakage-safe churn model training and evaluation."""
from pathlib import Path
import json
import warnings

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, average_precision_score, classification_report,
    confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

try:
    from xgboost import XGBClassifier
except ImportError as exc:
    XGBClassifier = None
    _xgb_import_error = exc

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "customer_churn_features.csv"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "docs" / "model_results"

TARGET = "Churn"
RANDOM_STATE = 42


def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=[TARGET])
    y = df[TARGET].astype(int)
    return X, y


def build_preprocessor(X):
    numeric = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]

    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    return ColumnTransformer([
        ("numeric", numeric_pipe, numeric),
        ("categorical", categorical_pipe, categorical),
    ])


def build_models():
    models = {
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_leaf=2,
            class_weight="balanced",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        ),
    }

    if XGBClassifier is not None:
        models["xgboost"] = XGBClassifier(
            n_estimators=400,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            objective="binary:logistic",
            eval_metric="logloss",
            scale_pos_weight=1.0,
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )
    return models


def evaluate_model(model, X_test, y_test):
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]
    return {
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "pr_auc": average_precision_score(y_test, prob),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
    }


def main():
    warnings.filterwarnings("ignore")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    X, y = load_data()

    # The test set is held out before model fitting and preprocessing fitting.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=RANDOM_STATE
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    results = []

    for name, estimator in build_models().items():
        pipeline = Pipeline([
            ("preprocessor", build_preprocessor(X_train)),
            ("model", estimator),
        ])

        cv_auc = cross_val_score(
            pipeline, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=None
        )

        pipeline.fit(X_train, y_train)
        metrics = evaluate_model(pipeline, X_test, y_test)

        row = {
            "model": name,
            "cv_roc_auc_mean": float(cv_auc.mean()),
            "cv_roc_auc_std": float(cv_auc.std()),
            **{k: v for k, v in metrics.items() if k != "confusion_matrix"},
        }
        results.append(row)

        joblib.dump(pipeline, MODEL_DIR / f"{name}.joblib")

        with open(REPORT_DIR / f"{name}_classification_report.txt", "w") as f:
            f.write(classification_report(y_test, pipeline.predict(X_test), digits=4))
            f.write("\nConfusion matrix:\n")
            f.write(str(metrics["confusion_matrix"]))

        with open(REPORT_DIR / f"{name}_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

    comparison = pd.DataFrame(results).sort_values(
        ["pr_auc", "roc_auc"], ascending=False
    )
    comparison.to_csv(REPORT_DIR / "model_comparison.csv", index=False)

    metadata = {
        "random_state": RANDOM_STATE,
        "test_size": 0.20,
        "stratified": True,
        "target": TARGET,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "positive_rate_train": float(y_train.mean()),
        "positive_rate_test": float(y_test.mean()),
        "selection_priority": ["pr_auc", "roc_auc", "recall", "f1"],
    }
    with open(REPORT_DIR / "training_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(comparison.to_string(index=False))
    print("\nSaved models to:", MODEL_DIR)
    print("Saved reports to:", REPORT_DIR)


if __name__ == "__main__":
    main()
