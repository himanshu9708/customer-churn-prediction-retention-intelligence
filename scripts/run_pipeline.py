"""Run the reproducible customer-churn pipeline end to end.

This orchestrator intentionally runs existing phase modules instead of duplicating
their logic. Model training and evaluation require the local dataset/model
environment to be available.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(module: str) -> None:
    print(f"\n=== Running {module} ===")
    subprocess.run(
        [sys.executable, "-m", module],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    run("src.data.run_ingestion")
    run("src.data.run_cleaning")
    run("src.models.train_models")
    run("src.evaluation.evaluate_models")
    run("src.retention.retention_engine")
    print("\n=== Pipeline completed successfully ===")


if __name__ == "__main__":
    main()
