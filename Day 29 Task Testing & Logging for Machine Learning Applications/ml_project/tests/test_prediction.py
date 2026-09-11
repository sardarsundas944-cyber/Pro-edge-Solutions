import sys
import os
import pytest
from sklearn.linear_model import LinearRegression

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from predict import make_prediction

def test_make_prediction_valid_input():
    X_train = [[1000, 3], [1500, 4], [2000, 5]]
    y_train = [200000, 250000, 300000]
    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = make_prediction(model, [[1200, 3]])
    assert predictions is not None
    assert len(predictions) == 1

def test_make_prediction_none_model():
    with pytest.raises(ValueError):
        make_prediction(None, [[1200, 3]])

def test_make_prediction_empty_input():
    X_train = [[1000, 3], [1500, 4], [2000, 5]]
    y_train = [200000, 250000, 300000]
    model = LinearRegression()
    model.fit(X_train, y_train)

    with pytest.raises(ValueError):
        make_prediction(model, [])

def test_make_prediction_multiple_rows():
    X_train = [[1000, 3], [1500, 4], [2000, 5]]
    y_train = [200000, 250000, 300000]
    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = make_prediction(model, [[1200, 3], [1800, 4]])
    assert len(predictions) == 2
