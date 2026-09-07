import argparse

from irisml.train import run_training
from irisml.predict import run_prediction


def train_cli():
    parser = argparse.ArgumentParser(description="Train the iris model")
    parser.add_argument(
        "--config", type=str, default="configs/config.yaml", help="path to config file"
    )
    args = parser.parse_args()
    run_training(args.config)


def predict_cli():
    parser = argparse.ArgumentParser(description="Run prediction with the iris model")
    parser.add_argument(
        "--config", type=str, default="configs/config.yaml", help="path to config file"
    )
    parser.add_argument(
        "--input", type=str, required=True, help="path to input csv file"
    )
    args = parser.parse_args()
    run_prediction(args.config, args.input)


if __name__ == "__main__":
    train_cli()
