import joblib
from train_model import load_dataset


def load_and_predict(model_path):
    X_train, X_test, y_train, y_test = load_dataset()

    model = joblib.load(model_path)
    predictions = model.predict(X_test)

    print("Model loaded successfully from:", model_path)
    print("Predictions on test data:")
    print(predictions)

    return predictions, X_test, y_test


if __name__ == "__main__":
    load_and_predict("models/iris_random_forest_v1.pkl")
