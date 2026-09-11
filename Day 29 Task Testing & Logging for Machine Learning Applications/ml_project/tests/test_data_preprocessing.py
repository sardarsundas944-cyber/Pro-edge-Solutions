import sys
import os
import pandas as pd
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_preprocessing import load_data, clean_data, split_data

def test_load_data_valid_file():
    data = load_data("data/house_data.csv")
    assert data is not None
    assert len(data) > 0

def test_load_data_invalid_file():
    with pytest.raises(FileNotFoundError):
        load_data("data/does_not_exist.csv")

def test_clean_data_removes_missing_values():
    sample_data = pd.DataFrame({
        "size": [1000, 1200, None],
        "price": [200000, 220000, 250000]
    })
    cleaned = clean_data(sample_data)
    assert len(cleaned) == 2
    assert cleaned.isnull().sum().sum() == 0

def test_clean_data_with_none_input():
    with pytest.raises(ValueError):
        clean_data(None)

def test_split_data_valid_target():
    sample_data = pd.DataFrame({
        "size": [1000, 1200, 1400, 1600, 1800],
        "price": [200000, 220000, 240000, 260000, 280000]
    })
    X_train, X_test, y_train, y_test = split_data(sample_data, "price", test_size=0.2)
    assert len(X_train) + len(X_test) == 5
    assert "price" not in X_train.columns

def test_split_data_invalid_target():
    sample_data = pd.DataFrame({
        "size": [1000, 1200],
        "price": [200000, 220000]
    })
    with pytest.raises(ValueError):
        split_data(sample_data, "not_a_column")
