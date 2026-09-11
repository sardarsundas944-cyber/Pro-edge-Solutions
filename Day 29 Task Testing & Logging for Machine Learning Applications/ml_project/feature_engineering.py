from sklearn.preprocessing import StandardScaler
from logger_config import setup_logger

logger = setup_logger("feature_engineering")

def create_features(data):
    if data is None:
        logger.error("create_features received None instead of a dataframe")
        raise ValueError("Input data cannot be None")

    new_data = data.copy()

    if "size" in new_data.columns and "bedrooms" in new_data.columns:
        new_data["size_per_bedroom"] = new_data["size"] / new_data["bedrooms"]
        logger.info("Created new feature: size_per_bedroom")
    else:
        logger.warning("Required columns not found to create size_per_bedroom feature")

    return new_data

def scale_features(X_train, X_test):
    if X_train is None or X_test is None:
        logger.error("scale_features received None instead of data")
        raise ValueError("Input data cannot be None")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logger.info("Features scaled successfully")

    return X_train_scaled, X_test_scaled, scaler
