import sys
import os
import pytest
from sklearn.linear_model import LinearRegression

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import train_model, save_model, load_model

def test_train_model_returns_model():
    X_train = [[1000, 3], [1500, 4], [2000, 5]]
    y_train = [200000, 250000, 300000]
    model = train_model(X_train, y_train)
    assert model is not None
    assert isinstance(model, LinearRegression)

def test_train_model_none_input():
    with pytest.raises(ValueError):
        train_model(None, None)

def test_save_and_load_model(tmp_path):
    X_train = [[1000, 3], [1500, 4], [2000, 5]]
    y_train = [200000, 250000, 300000]
    model = train_model(X_train, y_train)

    file_path = os.path.join(tmp_path, "test_model.pkl")
    save_model(model, file_path)

    assert os.path.exists(file_path)

    loaded_model = load_model(file_path)
    assert isinstance(loaded_model, LinearRegression)

def test_load_model_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_model("models/does_not_exist.pkl")

def test_save_model_none_input():
    with pytest.raises(ValueError):
        save_model(None, "models/test.pkl")
