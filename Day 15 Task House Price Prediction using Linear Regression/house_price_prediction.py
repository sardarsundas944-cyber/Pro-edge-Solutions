import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent / "data"
RESULTS_DIR = Path(__file__).resolve().parent / "results"
DATASET_PATH = DATA_DIR / "house_data.csv"


def load_dataset():
    DATA_DIR.mkdir(exist_ok=True)
    if DATASET_PATH.exists():
        df = pd.read_csv(DATASET_PATH)
        return df

    housing = fetch_california_housing(as_frame=True)
    df = housing.frame.copy()
    df.rename(columns={"MedHouseVal": "Price"}, inplace=True)
    df.to_csv(DATASET_PATH, index=False)
    return df


def preprocess_data(df):
    df = df.copy()
    df = df.dropna()
    feature_cols = [
        "MedInc",
        "HouseAge",
        "AveRooms",
        "AveBedrms",
        "Population",
        "AveOccup",
        "Latitude",
        "Longitude",
    ]
    target_col = "Price"

    if not all(col in df.columns for col in feature_cols + [target_col]):
        raise ValueError("Required columns are missing from the dataset.")

    X = df[feature_cols]
    y = df[target_col]
    return X, y


def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, preds)

    results = {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
    }

    comparison = pd.DataFrame({"Actual": y_test, "Predicted": preds})
    comparison = comparison.reset_index(drop=True)
    return model, preds, results, comparison


def save_visualization(comparison):
    RESULTS_DIR.mkdir(exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.scatter(comparison["Actual"], comparison["Predicted"], alpha=0.7)
    plt.plot(
        [comparison["Actual"].min(), comparison["Actual"].max()],
        [comparison["Actual"].min(), comparison["Actual"].max()],
        color="red",
        linestyle="--",
        label="Ideal fit",
    )
    plt.xlabel("Actual House Price")
    plt.ylabel("Predicted House Price")
    plt.title("Linear Regression: Actual vs Predicted Prices")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "actual_vs_predicted.png", dpi=200)
    plt.close()


def main():
    print("Loading dataset...")
    df = load_dataset()
    print(f"Dataset shape: {df.shape}")
    print(df.head())

    print("\nPreparing feature and target variables...")
    X, y = preprocess_data(df)

    print("Splitting data into training and testing sets...")
    model, preds, metrics, comparison = train_and_evaluate(X, y)

    print("\nModel performance metrics:")
    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")

    save_visualization(comparison)

    print(f"\nSaved prediction plot to: {RESULTS_DIR / 'actual_vs_predicted.png'}")
    print("\nSample predictions:")
    print(comparison.head())

    return metrics


if __name__ == "__main__":
    main()
