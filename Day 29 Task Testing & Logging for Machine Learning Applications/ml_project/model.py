import os
import joblib
from sklearn.linear_model import LinearRegression
from logger_config import setup_logger

logger = setup_logger("model")

def train_model(X_train, y_train):
    if X_train is None or y_train is None:
        logger.error("train_model received None instead of data")
        raise ValueError("Training data cannot be None")

    model = LinearRegression()
    model.fit(X_train, y_train)

    logger.info("Model training completed successfully")

    return model

def save_model(model, file_path):
    if model is None:
        logger.error("save_model received None instead of a model")
        raise ValueError("Model cannot be None")

    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    joblib.dump(model, file_path)
    logger.info("Model saved to " + str(file_path))

def load_model(file_path):
    if not os.path.exists(file_path):
        logger.error("Model file not found: " + str(file_path))
        raise FileNotFoundError("Model file not found: " + str(file_path))

    model = joblib.load(file_path)
    logger.info("Model loaded successfully from " + str(file_path))

    return model
