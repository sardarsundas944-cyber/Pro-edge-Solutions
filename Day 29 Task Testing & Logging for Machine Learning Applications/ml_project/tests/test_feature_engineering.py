import sys
import os
import pandas as pd
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from feature_engineering import create_features, scale_features

def test_create_features_adds_new_column():
    sample_data = pd.DataFrame({
        "size": [1000, 2000],
        "bedrooms": [2, 4]
    })
    result = create_features(sample_data)
    assert "size_per_bedroom" in result.columns
    assert result["size_per_bedroom"][0] == 500

def test_create_features_missing_columns():
    sample_data = pd.DataFrame({
        "age": [10, 20]
    })
    result = create_features(sample_data)
    assert "size_per_bedroom" not in result.columns

def test_create_features_none_input():
    with pytest.raises(ValueError):
        create_features(None)

def test_scale_features_shape():
    X_train = pd.DataFrame({
        "size": [1000, 1200, 1400],
        "age": [5, 10, 15]
    })
    X_test = pd.DataFrame({
        "size": [1100, 1300],
        "age": [7, 12]
    })
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    assert X_train_scaled.shape == (3, 2)
    assert X_test_scaled.shape == (2, 2)

def test_scale_features_none_input():
    with pytest.raises(ValueError):
        scale_features(None, None)
