from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import redis

from config import settings

app = FastAPI(title=settings.app_name)

model = joblib.load("model.pkl")

class_names = ["setosa", "versicolor", "virginica"]

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True
)

class InputData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
def read_root():
    return {"message": f"{settings.app_name} is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/config")
def get_config():
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "log_level": settings.log_level,
        "redis_host": settings.redis_host,
        "redis_port": settings.redis_port
    }

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
