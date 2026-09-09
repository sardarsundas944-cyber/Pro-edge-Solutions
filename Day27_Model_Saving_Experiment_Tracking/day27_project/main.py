from train_model import train_and_save
from load_model import load_and_predict
from compare_experiments import compare_experiments
import numpy as np

print("STEP 1: Training multiple experiments")
print("")

train_and_save(n_estimators=5, max_depth=1, version=1)
print("")
train_and_save(n_estimators=30, max_depth=3, version=2)
print("")
train_and_save(n_estimators=150, max_depth=6, version=3)

print("")
print("STEP 2: Loading a saved model and predicting")
print("")
predictions, X_test, y_test = load_and_predict("models/iris_random_forest_v3.pkl")

print("")
print("STEP 3: Comparing experiment history")
print("")
compare_experiments()
