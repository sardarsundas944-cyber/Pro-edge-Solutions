from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib

app = FastAPI(title="Day 34 ML Prediction API")

model = joblib.load("model/model.joblib")
class_names = joblib.load("model/class_names.joblib")

class PredictionRequest(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float

@app.get("/")
def home():
    return {"message": "Welcome to the ML Prediction API"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    input_data = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    confidence = float(max(probabilities))
    predicted_class = class_names[prediction]

    return PredictionResponse(prediction=predicted_class, confidence=round(confidence, 2))
