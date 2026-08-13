"""Run Phase 3 cleaning and print a validation report."""
from src.data.ingestion import load_raw_data
from src.data.cleaning import clean_data


def main():
    raw = load_raw_data()
    cleaned = clean_data(raw)
    print("=== Phase 3 Cleaning Report ===")
    print(f"Raw rows: {len(raw):,}")
    print(f"Cleaned rows: {len(cleaned):,}")
    print(f"Rows removed: {len(raw)-len(cleaned):,}")
    print(f"Missing values remaining: {int(cleaned.isna().sum().sum()):,}")
    print(f"Duplicate rows remaining: {int(cleaned.duplicated().sum()):,}")
    print(f"Churn values: {sorted(cleaned['Churn'].unique().tolist())}")


if __name__ == "__main__":
    main()
