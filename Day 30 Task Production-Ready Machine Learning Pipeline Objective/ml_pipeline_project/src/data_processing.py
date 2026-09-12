import os
import sys
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import config
from src.logger import get_logger

logger = get_logger("data_processing")


def create_raw_data():
    data = load_wine(as_frame=True)
    df = data.frame
    raw_path = os.path.join(config.DATA_DIR, "raw", "wine_data.csv")
    df.to_csv(raw_path, index=False)
    logger.info("Raw data created and saved at %s", raw_path)
    return raw_path


def load_raw_data():
    raw_path = os.path.join(config.DATA_DIR, "raw", "wine_data.csv")
    if not os.path.exists(raw_path):
        logger.warning("Raw data not found, creating new raw data")
        create_raw_data()
    df = pd.read_csv(raw_path)
    logger.info("Loaded raw data with shape %s", df.shape)
    return df


def get_features_and_target(df):
    x = df.drop("target", axis=1)
    y = df["target"]
    return x, y


def split_data(x, y):
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE
    )
    logger.info("Data split into train and test sets")
    return x_train, x_test, y_train, y_test
