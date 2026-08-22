from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def load_dataset():
    """Download the dataset if it is not already available locally."""
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    dataset_path = DATA_DIR / "tips.csv"
    if not dataset_path.exists():
        df = pd.read_csv(DATA_URL)
        df.to_csv(dataset_path, index=False)
    return pd.read_csv(dataset_path)


def clean_dataset(df):
    """Clean and standardize the data before analysis."""
    df = df.copy()
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

    for col in ["sex", "smoker", "day", "time"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    if "tip" in df.columns and "total_bill" in df.columns:
        df["tip_percentage"] = (df["tip"] / df["total_bill"]) * 100

    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    object_columns = df.select_dtypes(include=["object", "string", "str"]).columns
    for col in object_columns:
        if df[col].isna().any():
            mode_value = df[col].mode()
            if not mode_value.empty:
                df[col] = df[col].fillna(mode_value.iloc[0])

    df = df.drop_duplicates().reset_index(drop=True)
    return df


def generate_summary(df):
    """Produce the key statistical summary metrics for the project."""
    missing_values = df.isna().sum()
    duplicate_count = df.duplicated().sum()
    summary_stats = df.describe(include="all").transpose()
    return missing_values, duplicate_count, summary_stats


def plot_bar_chart(df):
    avg_by_day = df.groupby("day")["total_bill"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_by_day.plot(kind="bar", color=["#4C72B0", "#55A868", "#C44E52", "#8172B3"], ax=ax)
    ax.set_title("Average Total Bill by Day")
    ax.set_xlabel("Day")
    ax.set_ylabel("Average Total Bill ($)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "average_total_bill_by_day.png", dpi=200)
    plt.close(fig)


def plot_line_chart(df):
    day_time_summary = (
        df.groupby(["day", "time"]) ["total_bill"].mean().unstack(fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    day_time_summary.plot(kind="line", marker="o", ax=ax, linewidth=2)
    ax.set_title("Average Total Bill by Day and Meal Time")
    ax.set_xlabel("Day")
    ax.set_ylabel("Average Total Bill ($)")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "average_total_bill_by_day_and_time.png", dpi=200)
    plt.close(fig)


def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["total_bill"], bins=15, color="#66B3FF", edgecolor="black")
    ax.set_title("Distribution of Total Bill Amounts")
    ax.set_xlabel("Total Bill ($)")
    ax.set_ylabel("Frequency")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "total_bill_distribution.png", dpi=200)
    plt.close(fig)


def main():
    print("Loading dataset...")
    df = load_dataset()
    print(f"Initial shape: {df.shape}")

    print("Cleaning dataset...")
    df = clean_dataset(df)

    missing_values, duplicate_count, summary_stats = generate_summary(df)
    print("\nDataset information:")
    print(df.info())
    print("\nMissing values by column:")
    print(missing_values[missing_values > 0])
    print(f"\nDuplicate rows removed: {duplicate_count}")
    print("\nSummary statistics:")
    print(summary_stats)

    plot_bar_chart(df)
    plot_line_chart(df)
    plot_histogram(df)

    print("\nGenerated charts:")
    for file_name in [
        "average_total_bill_by_day.png",
        "average_total_bill_by_day_and_time.png",
        "total_bill_distribution.png",
    ]:
        print(f"- {OUTPUT_DIR / file_name}")

    avg_bill_by_day = df.groupby("day")["total_bill"].mean().sort_values(ascending=False)
    average_tip_pct = df["tip_percentage"].mean()
    smoker_bill = df.groupby("smoker")["total_bill"].mean()
    table_size_bill = df.groupby("size")["total_bill"].mean().sort_values(ascending=False)
    weekend_bill = df[df["day"].isin(["Sat", "Sun"])]["total_bill"].mean()
    weekday_bill = df[df["day"].isin(["Thur", "Fri"])]["total_bill"].mean()

    insights = [
        f"Saturday and Sunday are the busiest spending days, with average bills of ${avg_bill_by_day.get('Sat', 0):.2f} and ${avg_bill_by_day.get('Sun', 0):.2f} respectively.",
        f"The average tip percentage is {average_tip_pct:.2f}% across all restaurant visits, showing a strong relationship between service quality and the final bill.",
        f"Smokers spend an average of ${smoker_bill.get('Yes', 0):.2f} compared with ${smoker_bill.get('No', 0):.2f} for non-smokers, indicating a distinct spending pattern by customer type.",
        f"The average bill for larger groups is ${table_size_bill.iloc[0]:.2f}, highlighting how party size influences ordering behavior.",
        f"Weekend dining averages ${weekend_bill:.2f}, which is higher than weekday dining at ${weekday_bill:.2f}, suggesting stronger spending during leisure dining periods.",
    ]

    print("\nKey insights:")
    for idx, insight in enumerate(insights, start=1):
        print(f"{idx}. {insight}")

    print("\nProject completed successfully.")


if __name__ == "__main__":
    main()
