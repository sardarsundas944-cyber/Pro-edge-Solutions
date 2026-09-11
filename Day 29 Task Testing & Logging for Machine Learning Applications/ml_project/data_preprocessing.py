import pandas as pd
import os
from logger_config import setup_logger

logger = setup_logger("data_preprocessing")

def load_data(file_path):
    if not os.path.exists(file_path):
        logger.error("File not found: " + str(file_path))
        raise FileNotFoundError("File not found: " + str(file_path))

    data = pd.read_csv(file_path)

    if data.empty:
        logger.warning("Loaded data is empty: " + str(file_path))
    else:
        logger.info("Data loaded successfully with " + str(len(data)) + " rows")

    return data

def clean_data(data):
    if data is None:
        logger.error("clean_data received None instead of a dataframe")
        raise ValueError("Input data cannot be None")

    before_rows = len(data)
    cleaned = data.dropna()
    after_rows = len(cleaned)

    if before_rows != after_rows:
        logger.warning("Removed " + str(before_rows - after_rows) + " rows with missing values")
    else:
        logger.info("No missing values found during cleaning")

    return cleaned

def split_data(data, target_column, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split

    if target_column not in data.columns:
        logger.error("Target column not found: " + str(target_column))
        raise ValueError("Target column not found: " + str(target_column))

    X = data.drop(columns=[target_column])
    y = data[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    logger.info("Data split into train and test sets")

    return X_train, X_test, y_train, y_test
