import os
import pickle
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import config

def prepare_dataset():
    folder = os.path.dirname(config.DATASET_PATH)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(config.DATASET_PATH):
        iris = load_iris(as_frame=True)
        data = iris.frame
        data.to_csv(config.DATASET_PATH, index=False)
        print("Dataset created at:", config.DATASET_PATH)
    else:
        print("Dataset already exists at:", config.DATASET_PATH)

def train_model():
    data = pd.read_csv(config.DATASET_PATH)
    x = data.drop("target", axis=1)
    y = data["target"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
    )

    model = LogisticRegression(max_iter=200)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    print("Model Accuracy:", accuracy)

    folder = os.path.dirname(config.MODEL_PATH)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(config.MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("Model saved at:", config.MODEL_PATH)

def main():
    print("Starting Application:", config.APP_NAME)
    print("Version:", config.APP_VERSION)
    config.show_config()
    prepare_dataset()
    train_model()
    print("Application finished successfully")

if __name__ == "__main__":
    main()
