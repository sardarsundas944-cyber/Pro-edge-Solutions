import os
import joblib
from sklearn.ensemble import RandomForestClassifier

from irisml.config import load_config
from irisml.preprocessing import load_data, split_data


def run_training(config_path):
    config = load_config(config_path)

    data_path = config["data_path"]
    model_path = config["model_path"]
    test_size = config.get("test_size", 0.2)
    random_state = config.get("random_state", 42)
    n_estimators = config.get("n_estimators", 100)

    df = load_data(data_path)
    X_train, X_test, y_train, y_test = split_data(df, test_size, random_state)

    model = RandomForestClassifier(
        n_estimators=n_estimators, random_state=random_state
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    print("Training accuracy:", train_score)
    print("Testing accuracy:", test_score)
    print("Model saved to:", model_path)

    return model
