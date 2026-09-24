from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="ML Prediction API")

model = joblib.load("model.pkl")

class_names = ["setosa", "versicolor", "virginica"]

class InputData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"message": "ML Prediction API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: InputData):
    input_array = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])
    prediction = model.predict(input_array)
    predicted_class = class_names[int(prediction[0])]
    return {"prediction": predicted_class}
