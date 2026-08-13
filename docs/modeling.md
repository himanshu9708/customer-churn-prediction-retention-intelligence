# Phase 7 — ML Model Development

## Objective

Train baseline and tree-based binary classifiers for customer churn prediction using the Phase 6 feature dataset.

## Models

1. Logistic Regression
2. Random Forest
3. XGBoost

## Evaluation design

- Stratified 80/20 train-test split.
- `random_state=42` for reproducibility.
- Five-fold stratified cross-validation on the training set.
- Preprocessing is inside a scikit-learn `Pipeline` and `ColumnTransformer`, so imputers, scaling, and one-hot encoding are fitted only on training folds.
- The test set is held out until final evaluation.

## Metrics

Because churn prediction is a retention problem, accuracy is not sufficient. The comparison reports:

- ROC-AUC
- PR-AUC
- Recall
- Precision
- F1
- Accuracy
- Confusion matrix

PR-AUC and recall receive special attention because missing a genuinely at-risk customer can reduce the value of a retention program.

## Leakage controls

- `CustomerID` was removed in Phase 6.
- `Churn` is the target and is never included as a predictor.
- Test data is not used to fit preprocessing or models.
- Cross-validation is performed only on the training partition.

## Training

From the project root:

```bash
python -m src.models.train_models
```

The script writes model artifacts to `models/` and evaluation reports to `docs/model_results/`.
