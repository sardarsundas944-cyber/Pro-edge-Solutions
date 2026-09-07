from irisml.preprocessing import load_data, split_data


def test_load_data():
    df = load_data("data/iris.csv")
    assert df.shape[0] > 0
    assert "target" in df.columns


def test_split_data():
    df = load_data("data/iris.csv")
    X_train, X_test, y_train, y_test = split_data(df, test_size=0.2, random_state=42)
    assert len(X_train) > len(X_test)
    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)
