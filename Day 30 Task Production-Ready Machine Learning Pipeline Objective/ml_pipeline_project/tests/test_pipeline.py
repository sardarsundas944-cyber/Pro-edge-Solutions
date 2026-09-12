import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processing import load_raw_data, get_features_and_target, split_data
from src.pipeline import build_pipeline
from src.train import train_model
from src.predict import predict, load_model


def test_load_raw_data():
    df = load_raw_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0


def test_get_features_and_target():
    df = load_raw_data()
    x, y = get_features_and_target(df)
    assert "target" not in x.columns
    assert len(x) == len(y)


def test_split_data():
    df = load_raw_data()
    x, y = get_features_and_target(df)
    x_train, x_test, y_train, y_test = split_data(x, y)
    assert len(x_train) > len(x_test)
    assert len(x_train) == len(y_train)


def test_build_pipeline():
    pipeline = build_pipeline()
    steps = [name for name, step in pipeline.steps]
    assert "scaler" in steps
    assert "model" in steps


def test_train_model():
    pipeline, metrics = train_model()
    assert pipeline is not None
    assert metrics["accuracy"] >= 0
    assert metrics["accuracy"] <= 1


def test_load_model():
    train_model()
    model = load_model()
    assert model is not None


def test_predict_output_length():
    train_model()
    df = load_raw_data()
    x, y = get_features_and_target(df)
    sample = x.iloc[:5]
    result = predict(sample)
    assert len(result) == 5
