import os

import pandas as pd

from regression_pipeline import (
    evaluate_model,
    load_and_prepare_data,
    train_and_predict,
)


def test_load_and_prepare_data_returns_dataframe_and_target():
    df, X, y = load_and_prepare_data()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert X.shape[0] == y.shape[0]
    assert y.name in {"MedHouseVal", "target"}


def test_train_and_predict_returns_predictions_and_metrics():
    _, X, y = load_and_prepare_data()
    model, predictions, metrics = train_and_predict(X, y)

    assert model is not None
    assert len(predictions) == len(y)
    assert set(metrics) == {"mae", "mse", "rmse", "r2"}


def test_evaluate_model_returns_expected_error_keys():
    _, X, y = load_and_prepare_data()
    model, predictions, metrics = train_and_predict(X, y)
    report = evaluate_model(y, predictions)

    assert set(report) == {"mae", "mse", "rmse", "r2"}
    assert all(value >= 0 for value in report.values())


def test_outputs_directory_created():
    output_dir = "outputs"
    assert os.path.isdir(output_dir) is False or os.path.exists(output_dir)
