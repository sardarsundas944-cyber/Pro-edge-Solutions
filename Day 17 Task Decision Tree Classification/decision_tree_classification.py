"""Decision Tree Classification workflow for Day 17.

The source dataset is scikit-learn's Wisconsin Diagnostic Breast Cancer dataset,
a public classification dataset commonly mirrored on Kaggle. The script exports
the source data, evaluation tables, and figures used in the project README.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, plot_tree


RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"


def load_and_prepare_data():
    """Load the public dataset and return features, target, and a flat frame."""
    dataset = load_breast_cancer(as_frame=True)
    data = dataset.frame.copy()
    data.columns = [column.replace(" ", "_") for column in data.columns]
    data["target_name"] = data["target"].map(dict(enumerate(dataset.target_names)))
    DATA_DIR.mkdir(exist_ok=True)
    data.to_csv(DATA_DIR / "breast_cancer.csv", index=False)

    features = data.drop(columns=["target", "target_name"])
    target = data["target"]
    return features, target, data


def make_model(max_depth=None):
    """Build a preprocessing and classifier pipeline."""
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "classifier",
                DecisionTreeClassifier(
                    criterion="gini",
                    max_depth=max_depth,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def evaluate(model, features, target):
    """Return the requested classification metrics for a data split."""
    predictions = model.predict(features)
    return {
        "accuracy": accuracy_score(target, predictions),
        "precision": precision_score(target, predictions, zero_division=0),
        "recall": recall_score(target, predictions, zero_division=0),
        "f1_score": f1_score(target, predictions, zero_division=0),
        "predictions": predictions,
    }


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    features, target, data = load_and_prepare_data()

    print("Dataset shape:", data.shape)
    print("Missing values:", int(data.isna().sum().sum()))
    print("Class distribution:")
    print(data["target_name"].value_counts().to_string())

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        stratify=target,
        random_state=RANDOM_STATE,
    )

    baseline = make_model()
    baseline.fit(x_train, y_train)
    train_metrics = evaluate(baseline, x_train, y_train)
    test_metrics = evaluate(baseline, x_test, y_test)

    metric_names = ["accuracy", "precision", "recall", "f1_score"]
    summary = pd.DataFrame(
        {
            "metric": metric_names,
            "training_score": [train_metrics[name] for name in metric_names],
            "testing_score": [test_metrics[name] for name in metric_names],
        }
    )
    summary.to_csv(OUTPUT_DIR / "baseline_metrics.csv", index=False)
    print("\nBaseline metrics:")
    print(summary.to_string(index=False, float_format=lambda value: f"{value:.3f}"))

    matrix = confusion_matrix(y_test, test_metrics["predictions"])
    pd.DataFrame(
        matrix,
        index=["actual_malignant", "actual_benign"],
        columns=["predicted_malignant", "predicted_benign"],
    ).to_csv(OUTPUT_DIR / "confusion_matrix.csv")

    ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=["malignant", "benign"],
    ).plot(cmap="Blues", values_format="d")
    plt.title("Decision Tree Confusion Matrix")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=160)
    plt.close()

    depths = [1, 2, 3, 4, 5, 7, None]
    depth_rows = []
    for depth in depths:
        model = make_model(max_depth=depth)
        model.fit(x_train, y_train)
        train_result = evaluate(model, x_train, y_train)
        test_result = evaluate(model, x_test, y_test)
        depth_rows.append(
            {
                "max_depth": "unlimited" if depth is None else depth,
                "training_accuracy": train_result["accuracy"],
                "testing_accuracy": test_result["accuracy"],
                "training_f1": train_result["f1_score"],
                "testing_f1": test_result["f1_score"],
                "generalization_gap": train_result["accuracy"] - test_result["accuracy"],
            }
        )

    depth_results = pd.DataFrame(depth_rows)
    depth_results.to_csv(OUTPUT_DIR / "depth_experiment.csv", index=False)
    print("\nDepth experiment:")
    print(depth_results.to_string(index=False, float_format=lambda value: f"{value:.3f}"))

    plt.figure(figsize=(8, 5))
    plt.plot(depth_results["max_depth"].astype(str), depth_results["training_accuracy"], marker="o", label="Training")
    plt.plot(depth_results["max_depth"].astype(str), depth_results["testing_accuracy"], marker="o", label="Testing")
    plt.xlabel("Maximum tree depth")
    plt.ylabel("Accuracy")
    plt.title("Effect of Tree Depth on Accuracy")
    plt.ylim(0.75, 1.02)
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "depth_comparison.png", dpi=160)
    plt.close()

    plt.figure(figsize=(20, 10))
    plot_tree(
        baseline.named_steps["classifier"],
        feature_names=features.columns,
        class_names=list(dataset_name for dataset_name in load_breast_cancer().target_names),
        filled=True,
        max_depth=3,
        fontsize=7,
    )
    plt.title("Baseline Decision Tree (first three levels)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "decision_tree.png", dpi=160)
    plt.close()

    print("\nSaved data/, outputs/, and figures successfully.")


if __name__ == "__main__":
    main()
