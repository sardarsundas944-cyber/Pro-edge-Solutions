import os
import sys
import joblib
from sklearn.metrics import accuracy_score, f1_score

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import config
from src.logger import get_logger
from src.data_processing import load_raw_data, get_features_and_target, split_data
from src.pipeline import build_pipeline
from src.experiment_tracker import log_experiment

logger = get_logger("train")


def train_model():
    logger.info("Training started")

    df = load_raw_data()
    x, y = get_features_and_target(df)
    x_train, x_test, y_train, y_test = split_data(x, y)

    pipeline = build_pipeline()
    pipeline.fit(x_train, y_train)
    logger.info("Model training finished")

    predictions = pipeline.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted")

    logger.info("Model accuracy: %s", accuracy)
    logger.info("Model f1 score: %s", f1)

    model_filename = f"{config.MODEL_NAME}_v{config.MODEL_VERSION}.pkl"
    model_path = os.path.join(config.MODEL_DIR, model_filename)
    joblib.dump(pipeline, model_path)
    logger.info("Model saved at %s", model_path)

    latest_path = os.path.join(config.MODEL_DIR, "latest_model.pkl")
    joblib.dump(pipeline, latest_path)
    logger.info("Latest model updated at %s", latest_path)

    params = {
        "n_estimators": config.N_ESTIMATORS,
        "max_depth": config.MAX_DEPTH,
        "random_state": config.RANDOM_STATE
    }
    metrics = {
        "accuracy": round(accuracy, 4),
        "f1_score": round(f1, 4)
    }

    log_experiment(config.MODEL_NAME, params, metrics, config.MODEL_VERSION)

    return pipeline, metrics


if __name__ == "__main__":
    train_model()
