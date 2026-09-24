from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import redis
import os

app = FastAPI(title="ML Prediction API")

model = joblib.load("model.pkl")

class_names = ["setosa", "versicolor", "virginica"]

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

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

@app.get("/redis-health")
def redis_health():
    redis_client.ping()
    return {"redis_status": "connected"}

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

    redis_client.incr("total_predictions")
    redis_client.incr(f"predictions:{predicted_class}")

    return {"prediction": predicted_class}

@app.get("/stats")
def stats():
    total = redis_client.get("total_predictions") or 0
    setosa_count = redis_client.get("predictions:setosa") or 0
    versicolor_count = redis_client.get("predictions:versicolor") or 0
    virginica_count = redis_client.get("predictions:virginica") or 0
    return {
        "total_predictions": int(total),
        "setosa": int(setosa_count),
        "versicolor": int(versicolor_count),
        "virginica": int(virginica_count)
    }
