import joblib
import pandas as pd

from irisml.config import load_config


def run_prediction(config_path, input_path):
    config = load_config(config_path)
    model_path = config["model_path"]

    model = joblib.load(model_path)

    df = pd.read_csv(input_path)
    if "target" in df.columns:
        df = df.drop("target", axis=1)

    predictions = model.predict(df)

    for i, pred in enumerate(predictions):
        print(f"Row {i}: predicted class = {pred}")

    return predictions
