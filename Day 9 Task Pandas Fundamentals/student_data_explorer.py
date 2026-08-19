"""Explore and analyze a student dataset with Pandas."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "Student ID",
    "Student Name",
    "Department",
    "Semester",
    "Age",
    "Marks",
    "Attendance Percentage",
]


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """Load the student CSV and validate its required columns."""
    dataset = pd.read_csv(file_path)
    missing_columns = set(REQUIRED_COLUMNS) - set(dataset.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Dataset is missing required columns: {missing}")
    return dataset


def display_exploration(dataset: pd.DataFrame) -> None:
    """Display the first/last records, schema, columns, and data types."""
    print("\n=== First 5 Records ===")
    print(dataset.head(5).to_string(index=False))

    print("\n=== Last 5 Records ===")
    print(dataset.tail(5).to_string(index=False))

    print("\n=== Dataset Information ===")
    dataset.info()

    print("\n=== Column Names and Data Types ===")
    print(dataset.dtypes.to_string())


def filter_by_marks(dataset: pd.DataFrame, minimum_marks: float) -> pd.DataFrame:
    """Return students whose marks are greater than the supplied threshold."""
    return dataset.loc[dataset["Marks"] > minimum_marks, REQUIRED_COLUMNS]


def filter_by_department(dataset: pd.DataFrame, department: str) -> pd.DataFrame:
    """Return students in a department, matching its name case-insensitively."""
    department_mask = dataset["Department"].str.casefold() == department.casefold()
    return dataset.loc[department_mask, REQUIRED_COLUMNS]


def sort_by_marks(dataset: pd.DataFrame) -> pd.DataFrame:
    """Return all students sorted from highest to lowest marks."""
    return dataset.sort_values("Marks", ascending=False)[REQUIRED_COLUMNS]


def sort_by_attendance(dataset: pd.DataFrame) -> pd.DataFrame:
    """Return all students sorted from highest to lowest attendance."""
    return dataset.sort_values("Attendance Percentage", ascending=False)[REQUIRED_COLUMNS]


def analyze_dataset(dataset: pd.DataFrame) -> dict[str, object]:
    """Calculate overall and department-level academic insights."""
    highest_row = dataset.loc[dataset["Marks"].idxmax()]
    lowest_row = dataset.loc[dataset["Marks"].idxmin()]
    return {
        "total_students": len(dataset),
        "average_marks": dataset["Marks"].mean(),
        "highest_marks": highest_row[["Student Name", "Marks"]],
        "lowest_marks": lowest_row[["Student Name", "Marks"]],
        "department_student_count": dataset["Department"].value_counts().sort_index(),
        "department_average_marks": dataset.groupby("Department")["Marks"].mean().sort_values(ascending=False),
    }


def display_analysis(analysis: dict[str, object]) -> None:
    """Print calculated insights in a readable format."""
    print("\n=== Academic Analysis ===")
    print(f"Total students: {analysis['total_students']}")
    print(f"Average marks: {analysis['average_marks']:.2f}")

    highest = analysis["highest_marks"]
    lowest = analysis["lowest_marks"]
    print(f"Highest marks: {highest['Marks']} ({highest['Student Name']})")
    print(f"Lowest marks: {lowest['Marks']} ({lowest['Student Name']})")

    print("\nDepartment-wise student count:")
    print(analysis["department_student_count"].to_string())
    print("\nDepartment-wise average marks:")
    print(analysis["department_average_marks"].round(2).to_string())


def display_filtering_and_sorting(dataset: pd.DataFrame, minimum_marks: float, department: str) -> None:
    """Print the requested filtering and sorting views."""
    print(f"\n=== Students with Marks Greater Than {minimum_marks:g} ===")
    print(filter_by_marks(dataset, minimum_marks).to_string(index=False))

    print(f"\n=== Students in {department} ===")
    department_students = filter_by_department(dataset, department)
    if department_students.empty:
        print("No students found for this department.")
    else:
        print(department_students.to_string(index=False))

    print("\n=== Students Sorted by Marks ===")
    print(sort_by_marks(dataset).to_string(index=False))

    print("\n=== Students Sorted by Attendance Percentage ===")
    print(sort_by_attendance(dataset).to_string(index=False))


def parse_arguments() -> argparse.Namespace:
    """Parse optional command-line filters."""
    parser = argparse.ArgumentParser(description="Explore student academic data with Pandas.")
    parser.add_argument("--file", type=Path, default=Path(__file__).with_name("students.csv"))
    parser.add_argument("--minimum-marks", type=float, default=80)
    parser.add_argument("--department", default="Computer Science")
    return parser.parse_args()


def main() -> None:
    """Run the complete student data exploration workflow."""
    arguments = parse_arguments()
    dataset = load_dataset(arguments.file)
    display_exploration(dataset)
    display_filtering_and_sorting(dataset, arguments.minimum_marks, arguments.department)
    display_analysis(analyze_dataset(dataset))


if __name__ == "__main__":
    main()
