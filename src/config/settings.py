"""Project configuration for the customer churn project."""
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "customer_churn_dataset-training-master.csv"
MODEL_DIR = PROJECT_ROOT / "models"

APP_NAME = os.getenv("APP_NAME", "Customer Churn Retention Intelligence")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
