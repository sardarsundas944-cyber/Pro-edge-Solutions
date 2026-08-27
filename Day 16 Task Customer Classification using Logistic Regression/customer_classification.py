from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "data" / "customer_data.csv"
RESULTS_PATH = ROOT / "results" / "metrics.csv"
SCREENSHOT_DIR = ROOT / "screenshots"


def save_evaluation_visuals(metrics: pd.DataFrame, matrix: np.ndarray) -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    confusion_path = SCREENSHOT_DIR / "confusion_matrix.png"
    metrics_path = SCREENSHOT_DIR / "evaluation_metrics.png"

    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xticks([0, 1], ["Predicted No", "Predicted Yes"])
    plt.yticks([0, 1], ["Actual No", "Actual Yes"])
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            plt.text(j, i, str(matrix[i, j]), ha="center", va="center", color="black", fontsize=12)
    plt.xlabel("Predicted label")
    plt.ylabel("Actual label")
    plt.tight_layout()
    plt.savefig(confusion_path, dpi=200)
    plt.close()

    metric_values = [
        metrics["Accuracy"].iloc[0],
        metrics["Precision"].iloc[0],
        metrics["Recall"].iloc[0],
        metrics["F1 Score"].iloc[0],
    ]
    labels = ["Accuracy", "Precision", "Recall", "F1 Score"]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, metric_values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
    plt.title("Logistic Regression Model Evaluation")
    plt.ylim(0, 1.05)
    for index, value in enumerate(metric_values):
        plt.text(index, value + 0.02, f"{value:.3f}", ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(metrics_path, dpi=200)
    plt.close()

    print(f"Saved model visuals to {SCREENSHOT_DIR}")


def generate_demo_dataset(path: Path) -> pd.DataFrame:
    """Create a realistic customer classification dataset when no CSV is available."""
    rng = np.random.default_rng(42)
    n_rows = 1500

    df = pd.DataFrame(
        {
            "age": rng.integers(18, 70, size=n_rows),
            "annual_income": rng.normal(65000, 20000, size=n_rows),
            "monthly_spend": rng.normal(320, 140, size=n_rows),
            "tenure_months": rng.integers(6, 72, size=n_rows),
            "num_products": rng.integers(1, 5, size=n_rows),
            "satisfaction_score": rng.integers(1, 6, size=n_rows),
            "is_active_member": rng.binomial(1, 0.55, size=n_rows),
            "has_credit_card": rng.binomial(1, 0.72, size=n_rows),
            "gender": rng.choice(["Male", "Female"], size=n_rows),
            "city_segment": rng.choice(["Urban", "Suburban", "Rural"], size=n_rows),
        }
    )

    df["annual_income"] = df["annual_income"].clip(lower=15000, upper=200000)
    df["monthly_spend"] = df["monthly_spend"].clip(lower=40, upper=1500)

    score = (
        -12
        + (0.05 * df["age"])
        + (0.0002 * df["annual_income"])
        + (0.015 * df["monthly_spend"])
        + (0.03 * df["tenure_months"])
        + (1.2 * (df["num_products"] > 2).astype(int))
        - (0.7 * df["satisfaction_score"])
        - (1.3 * df["is_active_member"])
        + (0.8 * df["has_credit_card"])
    )
    probability = 1 / (1 + np.exp(-score))
    df["customer_churn"] = rng.random(n_rows) < probability
    df["customer_churn"] = df["customer_churn"].astype(int)

    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        print(f"Dataset not found at {path}. Generating a demo customer dataset...")
        return generate_demo_dataset(path)

    df = pd.read_csv(path)
    print(f"Loaded dataset from {path} with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df


def prepare_features_and_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    target_columns = ["customer_churn", "target", "churn"]

    target_name = next((col for col in target_columns if col in df.columns), None)
    if target_name is None:
        raise ValueError(
            "No target column found. Please include one of: customer_churn, target, or churn."
        )

    target = df[target_name]
    feature_frame = df.drop(columns=[target_name])

    for column in feature_frame.select_dtypes(include=["number"]).columns:
        feature_frame[column] = feature_frame[column].fillna(feature_frame[column].median())

    for column in feature_frame.select_dtypes(exclude=["number"]).columns:
        feature_frame[column] = feature_frame[column].fillna(feature_frame[column].mode().iloc[0])

    return feature_frame, target


def build_model() -> Pipeline:
    numeric_features = []
    categorical_features = []

    return Pipeline(
        steps=[
            (
                "preprocessor",
                ColumnTransformer(
                    transformers=[
                        ("num", "passthrough", numeric_features),
                        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
                    ],
                    remainder="drop",
                ),
            ),
            ("classifier", LogisticRegression(max_iter=2000, random_state=42)),
        ]
    )


def train_and_evaluate() -> tuple[Pipeline, pd.DataFrame, np.ndarray, np.ndarray]:
    df = load_dataset(DATASET_PATH)
    features, target = prepare_features_and_target(df)

    if features.empty:
        raise ValueError("Feature set is empty. Please check the dataset columns.")

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    numeric_columns = X_train.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = X_train.select_dtypes(exclude=[np.number]).columns.tolist()

    model = Pipeline(
        steps=[
            (
                "preprocessor",
                ColumnTransformer(
                    transformers=[
                        ("num", "passthrough", numeric_columns),
                        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
                    ],
                    remainder="drop",
                ),
            ),
            ("classifier", LogisticRegression(max_iter=2000, random_state=42)),
        ]
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)
    matrix = confusion_matrix(y_test, predictions)

    metrics = pd.DataFrame(
        [
            {
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1 Score": f1,
                "True Negatives": int(matrix[0, 0]),
                "False Positives": int(matrix[0, 1]),
                "False Negatives": int(matrix[1, 0]),
                "True Positives": int(matrix[1, 1]),
            }
        ]
    )

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(RESULTS_PATH, index=False)
    save_evaluation_visuals(metrics, matrix)

    print("\n=== Model Evaluation Metrics ===")
    print(metrics.to_string(index=False))
    print("\n=== Confusion Matrix ===")
    print(matrix)
    print("\n=== Classification Report ===")
    print(classification_report(y_test, predictions, zero_division=0))

    return model, metrics, y_test, predictions


if __name__ == "__main__":
    train_and_evaluate()
