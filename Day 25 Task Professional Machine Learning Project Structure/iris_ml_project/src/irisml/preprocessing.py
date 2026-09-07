import pandas as pd
from sklearn.model_selection import train_test_split


def load_data(data_path):
    df = pd.read_csv(data_path)
    return df


def split_data(df, test_size=0.2, random_state=42):
    X = df.drop("target", axis=1)
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test
