import os
from irisml.train import run_training


def test_run_training():
    model = run_training("configs/config.yaml")
    assert model is not None
    assert os.path.exists("models/iris_model.joblib")
