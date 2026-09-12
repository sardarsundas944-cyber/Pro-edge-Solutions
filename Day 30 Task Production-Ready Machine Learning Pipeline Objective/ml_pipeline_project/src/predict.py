import os
import sys
import joblib
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import config
from src.logger import get_logger

logger = get_logger("predict")


def load_model():
    model_path = os.path.join(config.MODEL_DIR, "latest_model.pkl")

    if not os.path.exists(model_path):
        logger.error("No trained model found at %s", model_path)
        raise FileNotFoundError("Model not found. Please train the model first.")

    model = joblib.load(model_path)
    logger.info("Model loaded from %s", model_path)
    return model


def predict(input_data):
    model = load_model()

    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    predictions = model.predict(input_data)
    logger.info("Prediction made for %s rows", len(input_data))
    return predictions


if __name__ == "__main__":
    from src.data_processing import load_raw_data, get_features_and_target

    df = load_raw_data()
    x, y = get_features_and_target(df)
    sample = x.iloc[:5]

    result = predict(sample)
    print("Predictions:", result)
