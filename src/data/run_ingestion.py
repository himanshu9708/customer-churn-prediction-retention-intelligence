"""Run Phase 2 raw-data ingestion and validation."""
from src.data.ingestion import load_raw_data
from src.data.validation import get_validation_report


def main() -> None:
    df = load_raw_data()
    report = get_validation_report(df)

    print("\n=== Phase 2 Validation Report ===")
    print(f"Rows: {report['row_count']:,}")
    print(f"Columns: {report['column_count']}")
    print(f"Duplicate rows: {report['duplicate_rows']:,}")
    print(f"Churn values: {report['churn_values']}")
    print(f"Missing-value columns: {len(report['missing_value_columns'])}")
    print(f"Status: {report['status']}")

    if report["missing_value_columns"]:
        print("\nMissing values found:")
        for column, count in report["missing_value_columns"].items():
            print(f"  {column}: {count}")


if __name__ == "__main__":
    main()
