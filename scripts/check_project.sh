#!/bin/sh
set -eu

echo "Checking project structure..."

test -f api/main.py
test -f api/routes/predictions.py
test -f dashboard/app.py
test -f src/models/train_models.py
test -f src/evaluation/evaluate_models.py
test -f src/retention/retention_engine.py

echo "Project structure: OK"

python -m compileall -q api src dashboard

echo "Python compilation: OK"
