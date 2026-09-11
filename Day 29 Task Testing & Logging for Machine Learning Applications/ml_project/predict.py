from logger_config import setup_logger

logger = setup_logger("predict")

def make_prediction(model, input_data):
    if model is None:
        logger.error("make_prediction received None instead of a model")
        raise ValueError("Model cannot be None")

    if input_data is None or len(input_data) == 0:
        logger.error("make_prediction received empty input data")
        raise ValueError("Input data cannot be empty")

    try:
        predictions = model.predict(input_data)
        logger.info("Prediction generated for " + str(len(input_data)) + " rows")
        return predictions
    except Exception as error:
        logger.error("Prediction failed: " + str(error))
        raise
