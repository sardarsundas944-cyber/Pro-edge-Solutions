import numpy as np
from train_model import train_and_save
from load_model import load_and_predict


def verify(n_estimators, max_depth, version):
    model, X_test, y_test, original_predictions = train_and_save(n_estimators, max_depth, version)

    model_path = "models/iris_random_forest_v" + str(version) + ".pkl"
    loaded_predictions, loaded_X_test, loaded_y_test = load_and_predict(model_path)

    print("")
    print("Original Predictions:", original_predictions)
    print("Loaded Predictions:  ", loaded_predictions)

    if np.array_equal(original_predictions, loaded_predictions):
        print("SUCCESS: Loaded model predictions match the original model predictions")
    else:
        print("FAILED: Predictions do not match")


if __name__ == "__main__":
    verify(n_estimators=60, max_depth=4, version=4)
