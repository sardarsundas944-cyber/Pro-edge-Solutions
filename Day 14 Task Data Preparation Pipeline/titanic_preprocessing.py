"""Titanic data preparation pipeline for a machine learning workflow.

This project loads the Titanic dataset, inspects its structure, performs
train-test splitting, handles missing values using fits learned on training data
only, encodes categorical variables, and scales numeric features. The goal is to
produce a clean, leakage-safe preprocessing workflow.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATASET_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_dataset():
    """Load the Titanic dataset from seaborn or a public CSV fallback."""
    csv_path = Path("titanic.csv")

    try:
        return sns.load_dataset("titanic")
    except Exception:
        if csv_path.exists():
            return pd.read_csv(csv_path)

        try:
            df = pd.read_csv(DATASET_URL)
            df.to_csv(csv_path, index=False)
            return df
        except Exception as exc:
            raise RuntimeError("Unable to load the Titanic dataset from seaborn or the public CSV fallback.") from exc


def inspect_dataset(df):
    """Print and save a summary of dataset structure and missing values."""
    numeric_features = list(df.select_dtypes(include=["number"]).columns)
    categorical_features = list(df.select_dtypes(exclude=["number"]).columns)

    print("Dataset shape:", df.shape)
    print("\nData types:\n", df.dtypes)
    print("\nNumerical features:", numeric_features)
    print("\nCategorical features:", categorical_features)
    print("\nMissing values:\n", df.isnull().sum())

    missing_summary = df.isnull().sum().reset_index()
    missing_summary.columns = ["feature", "missing_values"]
    missing_summary.to_csv(OUTPUT_DIR / "missing_values_summary.csv", index=False)


def build_preprocessor(X_train):
    """Create a leakage-safe preprocessing pipeline for numeric and categorical features."""
    numeric_features = X_train.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = X_train.select_dtypes(exclude=["number"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )

    return preprocessor


def save_processed_data(X_train_processed, X_test_processed):
    """Persist processed train/test sets for inspection and downstream models."""
    pd.DataFrame(X_train_processed).to_csv(OUTPUT_DIR / "X_train_preprocessed.csv", index=False)
    pd.DataFrame(X_test_processed).to_csv(OUTPUT_DIR / "X_test_preprocessed.csv", index=False)


def create_visual_summary(df):
    """Create a small plot that summarizes a key relationship in the data."""
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="sex", hue="survived")
    plt.title("Survival Count by Sex")
    plt.xlabel("Sex")
    plt.ylabel("Count")
    plt.legend(title="Survived")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "survival_by_sex.png")
    plt.close()


def create_missing_values_plot(df):
    """Create a bar chart showing missing-value counts by feature."""
    missing = df.isnull().sum().sort_values(ascending=False)
    missing = missing[missing > 0]

    if missing.empty:
        return

    plt.figure(figsize=(10, 5))
    sns.barplot(x=missing.index.astype(str), y=missing.values, palette="viridis")
    plt.title("Missing Values by Feature")
    plt.xlabel("Feature")
    plt.ylabel("Missing Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "missing_values_distribution.png")
    plt.close()


def main():
    df = load_dataset()
    inspect_dataset(df)

    target = "survived"
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("\nTrain/test split: ")
    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)
    print("y_train distribution:\n", y_train.value_counts(normalize=True))
    print("y_test distribution:\n", y_test.value_counts(normalize=True))

    preprocessor = build_preprocessor(X_train)
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    print("\nProcessed train data shape:", X_train_processed.shape)
    print("Processed test data shape:", X_test_processed.shape)
    print("\nLeakage prevention summary:")
    print("- Train-test split was performed before preprocessing.")
    print("- Missing value imputers and scalers were fit only on the training set.")
    print("- The same fitted transformer was applied to the testing set to avoid leakage.")

    save_processed_data(X_train_processed, X_test_processed)
    create_visual_summary(df)
    create_missing_values_plot(df)

    print("\nSaved outputs in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
