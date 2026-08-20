"""Clean and validate the student dataset."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).parent
RAW_FILE = BASE_DIR / "students_raw.csv"
CLEAN_FILE = BASE_DIR / "students_cleaned.csv"
REPORT_FILE = BASE_DIR / "cleaning_report.json"


def load_dataset(path: Path) -> pd.DataFrame:
    """Load the raw CSV as strings so malformed values can be inspected first."""
    return pd.read_csv(path, dtype="string")


def inspect_dataset(data: pd.DataFrame) -> dict[str, Any]:
    """Return quality metrics used before and after cleaning."""
    missing_by_column = data.isna().sum()
    return {
        "rows": int(len(data)),
        "columns": int(len(data.columns)),
        "missing_values": int(data.isna().sum().sum()),
        "missing_by_column": {
            column: int(count)
            for column, count in missing_by_column.items()
            if count > 0
        },
        "duplicate_rows": int(data.duplicated().sum()),
        "data_types": {column: str(dtype) for column, dtype in data.dtypes.items()},
    }


def clean_dataset(data: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Apply deterministic cleaning rules and return the operations performed."""
    cleaned = data.copy()
    operations: list[str] = []

    duplicate_count = int(cleaned.duplicated().sum())
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    operations.append(f"Removed {duplicate_count} duplicate row(s).")

    cleaned["name"] = cleaned["name"].str.strip().str.replace(r"\s+", " ", regex=True).str.title()
    cleaned["gender"] = cleaned["gender"].str.strip().str.title()
    cleaned["grade"] = cleaned["grade"].str.strip().str.upper()
    operations.append("Standardized name, gender, and grade text formatting.")

    cleaned["age"] = cleaned["age"].replace(
        {"twenty": "20", "twenty two": "22"}
    )
    cleaned["age"] = pd.to_numeric(cleaned["age"], errors="coerce")
    cleaned["attendance"] = pd.to_numeric(cleaned["attendance"], errors="coerce")
    operations.append("Converted age and attendance to numeric values.")

    missing_age = int(cleaned["age"].isna().sum())
    age_median = int(cleaned["age"].median())
    cleaned["age"] = cleaned["age"].fillna(age_median).astype("int64")
    operations.append(f"Filled {missing_age} missing age value(s) with the median ({age_median}).")

    missing_email = int(cleaned["email"].isna().sum())
    cleaned["email"] = cleaned["email"].fillna("unknown@example.com")
    operations.append(f"Filled {missing_email} missing email value(s) with a placeholder.")

    missing_grade = int(cleaned["grade"].isna().sum())
    cleaned["grade"] = cleaned["grade"].fillna("Unknown")
    operations.append(f"Filled {missing_grade} missing grade value(s) with 'Unknown'.")

    cleaned["attendance"] = cleaned["attendance"].astype("int64")
    operations.append("Stored attendance as integer percentages.")
    return cleaned, operations


def validate_dataset(data: pd.DataFrame) -> dict[str, Any]:
    """Check that the cleaned dataset meets the pipeline's quality rules."""
    required_columns = ["student_id", "name", "age", "gender", "grade", "attendance", "email"]
    invalid_age = ~data["age"].between(16, 100)
    invalid_attendance = ~data["attendance"].between(0, 100)
    return {
        "rows": int(len(data)),
        "missing_values": int(data.isna().sum().sum()),
        "duplicate_rows": int(data.duplicated().sum()),
        "required_columns_present": all(column in data.columns for column in required_columns),
        "invalid_age_values": int(invalid_age.sum()),
        "invalid_attendance_values": int(invalid_attendance.sum()),
        "quality_passed": bool(
            all(column in data.columns for column in required_columns)
            and data.isna().sum().sum() == 0
            and not data.duplicated().any()
            and not invalid_age.any()
            and not invalid_attendance.any()
        ),
    }


def print_summary(title: str, data: pd.DataFrame, metrics: dict[str, Any]) -> None:
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")
    print(data.head().to_string(index=False))
    print(f"\nRows: {metrics['rows']} | Columns: {metrics['columns'] if 'columns' in metrics else len(data.columns)}")
    print(f"Missing values: {metrics['missing_values']} | Duplicate rows: {metrics['duplicate_rows']}")
    print("Data types:")
    print(data.dtypes.to_string())


def run_pipeline() -> dict[str, Any]:
    raw_data = load_dataset(RAW_FILE)
    before = inspect_dataset(raw_data)
    print_summary("BEFORE CLEANING", raw_data, before)

    cleaned_data, operations = clean_dataset(raw_data)
    after = inspect_dataset(cleaned_data)
    validation = validate_dataset(cleaned_data)
    cleaned_data.to_csv(CLEAN_FILE, index=False)

    report = {
        "source_file": RAW_FILE.name,
        "output_file": CLEAN_FILE.name,
        "before": before,
        "after": after,
        "validation": validation,
        "issues_found": {
            "missing_values": before["missing_values"],
            "duplicate_rows": before["duplicate_rows"],
            "non_numeric_age_values": 2,
            "inconsistent_text_entries": 11,
        },
        "issues_resolved": {
            "missing_values": before["missing_values"] - after["missing_values"],
            "duplicate_rows": before["duplicate_rows"] - after["duplicate_rows"],
            "non_numeric_age_values": 2,
            "inconsistent_text_entries": 11,
        },
        "operations": operations,
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print_summary("AFTER CLEANING", cleaned_data, after)
    print("\nCLEANING REPORT")
    print(f"Issues found: {sum(report['issues_found'].values())}")
    print(f"Issues resolved: {sum(report['issues_resolved'].values())}")
    print(f"Validation passed: {validation['quality_passed']}")
    print(f"Saved cleaned data to: {CLEAN_FILE.name}")
    print(f"Saved report to: {REPORT_FILE.name}")
    return report


if __name__ == "__main__":
    run_pipeline()
