import pandas as pd
import joblib

model_pipeline = joblib.load("model/titanic_pipeline.joblib")

raw_data = pd.DataFrame([
    {"Pclass": 1, "Sex": "female", "Age": 28, "SibSp": 0, "Parch": 0, "Fare": 80.0, "Embarked": "C"},
    {"Pclass": 3, "Sex": "male", "Age": None, "SibSp": 0, "Parch": 0, "Fare": 7.9, "Embarked": None},
    {"Pclass": 2, "Sex": "female", "Age": 35, "SibSp": 1, "Parch": 1, "Fare": 26.0, "Embarked": "S"}
])

predictions = model_pipeline.predict(raw_data)

raw_data["Prediction"] = predictions
print("Raw passenger input and predictions")
print(raw_data)
