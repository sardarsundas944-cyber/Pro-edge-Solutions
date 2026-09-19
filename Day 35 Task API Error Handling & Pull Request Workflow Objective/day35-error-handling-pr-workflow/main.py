from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import joblib

app = FastAPI(title="Day 35 ML Prediction API with Error Handling")

model = None
class_names = None
model_load_error = None

try:
    model = joblib.load("model/model.joblib")
    class_names = joblib.load("model/class_names.joblib")
except Exception as e:
    model_load_error = str(e)

class PredictionRequest(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float

@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = err["loc"][-1]
        errors.append({"field": field, "message": err["msg"]})
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "One or more fields failed validation",
            "details": errors
        }
    )

@app.exception_handler(HTTPException)
def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
def general_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong while processing your request"
        }
    )

@app.get("/")
def home():
    return {"message": "Welcome to the ML Prediction API"}

@app.get("/health")
def health():
    if model is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "message": "Model is not loaded",
                "details": model_load_error
            }
        )
    return {"status": "ok", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded, cannot make predictions")

    input_data = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    try:
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
    except Exception:
        raise HTTPException(status_code=500, detail="Model failed to generate a prediction")

    confidence = float(max(probabilities))
    predicted_class = class_names[prediction]

    return PredictionResponse(prediction=predicted_class, confidence=round(confidence, 2))
