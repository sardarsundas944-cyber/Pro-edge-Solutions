import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "outputs"
DATASET_PATH = DATA_DIR / "california_housing.csv"


def fetch_and_save_dataset():
    DATA_DIR.mkdir(exist_ok=True)
    if DATASET_PATH.exists():
        return pd.read_csv(DATASET_PATH)

    housing = fetch_california_housing(as_frame=True)
    df = housing.frame.copy()
    df.to_csv(DATASET_PATH, index=False)
    return df


def load_and_prepare_data():
    df = fetch_and_save_dataset()
    df = df.copy()

    if "MedHouseValue" in df.columns and "MedHouseVal" not in df.columns:
        df = df.rename(columns={"MedHouseValue": "MedHouseVal"})

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].median())
        else:
            df[column] = df[column].fillna(df[column].mode().iloc[0])

    X = df.drop(columns=["MedHouseVal"], errors="ignore")
    target_name = "MedHouseVal" if "MedHouseVal" in df.columns else "target"
    y = df[target_name]
    return df, X, y


def evaluate_model(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": float(mean_squared_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def train_and_predict(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X)
    metrics = evaluate_model(y, predictions)
    return model, predictions, metrics


def plot_feature_relationships(df, output_folder):
    output_folder.mkdir(exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.scatter(df["MedHouseVal"], df["MedInc"], alpha=0.6)
    plt.title("Median House Value vs Median Income")
    plt.xlabel("Median House Value")
    plt.ylabel("Median Income")
    plt.tight_layout()
    plt.savefig(output_folder / "house_value_vs_income.png", dpi=150)
    plt.close()

    plt.figure(figsize=(10, 6))
    corr = df[["MedHouseVal", "MedInc", "AveRooms", "AveBedrms", "Population"]].corr()
    plt.imshow(corr, cmap="coolwarm")
    plt.colorbar(label="Correlation coefficient")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
    plt.yticks(range(len(corr.index)), corr.index)
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(output_folder / "feature_correlation.png", dpi=150)
    plt.close()


def plot_predictions(actual, predicted, output_folder):
    output_folder.mkdir(exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.scatter(actual, predicted, alpha=0.5)
    plt.plot([actual.min(), actual.max()], [actual.min(), actual.max()], "r--", lw=2)
    plt.title("Actual vs Predicted House Values")
    plt.xlabel("Actual Value")
    plt.ylabel("Predicted Value")
    plt.tight_layout()
    plt.savefig(output_folder / "prediction_vs_actual.png", dpi=150)
    plt.close()


def save_metrics(metrics, output_folder):
    output_folder.mkdir(exist_ok=True)
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(output_folder / "model_metrics.csv", index=False)

    with open(output_folder / "model_summary.txt", "w", encoding="utf-8") as file:
        file.write("Regression Model Summary\n")
        file.write("=======================\n")
        for key, value in metrics.items():
            file.write(f"{key.upper()}: {value:.4f}\n")


def main():
    df, X, y = load_and_prepare_data()
    OUTPUT_DIR.mkdir(exist_ok=True)

    model, full_predictions, metrics = train_and_predict(X, y)
    save_metrics(metrics, OUTPUT_DIR)
    plot_feature_relationships(df, OUTPUT_DIR)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    final_predictions = model.predict(X_test)
    plot_predictions(y_test.to_numpy(), final_predictions, OUTPUT_DIR)

    print("Dataset shape:", df.shape)
    print("Target summary:")
    print(df["MedHouseVal"].describe())
    print("\nModel Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")

    return df, X, y, model, full_predictions, metrics


if __name__ == "__main__":
    main()
