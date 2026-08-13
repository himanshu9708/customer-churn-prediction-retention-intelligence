"""Load the raw customer churn dataset."""
from pathlib import Path

import pandas as pd

from src.config.settings import RAW_DATA_PATH
from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_raw_data(file_path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw CSV and return it without modifying its values."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {file_path}")

    df = pd.read_csv(file_path)
    logger.info("Loaded %s rows and %s columns from %s", len(df), len(df.columns), file_path)
    return df
