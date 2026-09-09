import os
import csv
import joblib
from datetime import datetime
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def load_dataset():
    data = load_iris()
    X = data.data
    y = data.target
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_and_save(n_estimators, max_depth, version):
    X_train, X_test, y_train, y_test = load_dataset()

    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average="macro")
    recall = recall_score(y_test, predictions, average="macro")
    f1 = f1_score(y_test, predictions, average="macro")

    os.makedirs("models", exist_ok=True)
    model_name = "iris_random_forest_v" + str(version) + ".pkl"
    model_path = os.path.join("models", model_name)
    joblib.dump(model, model_path)

    print("Model trained and saved successfully")
    print("Model Name:", model_name)
    print("Model Path:", model_path)
    print("n_estimators:", n_estimators, "max_depth:", max_depth)
    print("Accuracy:", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall:", round(recall, 4))
    print("F1 Score:", round(f1, 4))

    log_experiment(model_name, "Iris Dataset", n_estimators, max_depth, accuracy, precision, recall, f1, version)

    return model, X_test, y_test, predictions


def log_experiment(model_name, dataset_name, n_estimators, max_depth, accuracy, precision, recall, f1, version):
    os.makedirs("experiments", exist_ok=True)
    log_file = "experiments/experiment_log.csv"
    file_exists = os.path.isfile(log_file)

    with open(log_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "Model Name", "Training Date", "Dataset Name", "n_estimators",
                "max_depth", "Accuracy", "Precision", "Recall", "F1 Score", "Model Version"
            ])
        writer.writerow([
            model_name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dataset_name,
            n_estimators,
            max_depth,
            round(accuracy, 4),
            round(precision, 4),
            round(recall, 4),
            round(f1, 4),
            version
        ])

    print("Experiment logged in experiments/experiment_log.csv")


if __name__ == "__main__":
    train_and_save(n_estimators=5, max_depth=1, version=1)
