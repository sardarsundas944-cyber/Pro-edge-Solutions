import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_processing import create_raw_data, load_raw_data, get_features_and_target
from src.train import train_model
from src.predict import predict


def main():
    print("Step 1: Creating raw data")
    create_raw_data()

    print("Step 2: Training model")
    pipeline, metrics = train_model()
    print("Training metrics:", metrics)

    print("Step 3: Making sample predictions")
    df = load_raw_data()
    x, y = get_features_and_target(df)
    sample = x.iloc[:5]
    result = predict(sample)
    print("Sample predictions:", result)
    print("Actual values:      ", list(y.iloc[:5]))


if __name__ == "__main__":
    main()
