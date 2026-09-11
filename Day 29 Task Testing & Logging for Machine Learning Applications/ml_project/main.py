from logger_config import setup_logger
from data_preprocessing import load_data, clean_data, split_data
from feature_engineering import create_features, scale_features
from model import train_model, save_model, load_model
from predict import make_prediction

logger = setup_logger("main")

def run_pipeline():
    logger.info("Application started")

    try:
        data = load_data("data/house_data.csv")
        data = clean_data(data)
        data = create_features(data)

        X_train, X_test, y_train, y_test = split_data(data, "price")

        X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

        model = train_model(X_train_scaled, y_train)
        save_model(model, "models/house_price_model.pkl")

        loaded_model = load_model("models/house_price_model.pkl")
        predictions = make_prediction(loaded_model, X_test_scaled)

        logger.info("Sample predictions: " + str(predictions[:5]))
        logger.info("Application finished successfully")

    except Exception as error:
        logger.error("Application failed with error: " + str(error))
        raise

if __name__ == "__main__":
    run_pipeline()
