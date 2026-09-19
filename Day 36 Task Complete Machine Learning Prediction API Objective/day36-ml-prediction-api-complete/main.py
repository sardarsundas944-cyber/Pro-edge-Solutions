from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import joblib
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ml_api")

app = FastAPI(title="Day 36 Complete ML Prediction API")

model = None
class_names = None
model_load_error = None

try:
    model = joblib.load("model/model.joblib")
    class_names = joblib.load("model/class_names.joblib")
    logger.info("Model loaded successfully")
except Exception as e:
    model_load_error = str(e)
    logger.error(f"Model failed to load: {model_load_error}")

class PredictionRequest(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request received: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code} for {request.url.path}")
    return response

@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = err["loc"][-1]
        errors.append({"field": field, "message": err["msg"]})
    logger.warning(f"Validation failed on {request.url.path}: {errors}")
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
    logger.warning(f"HTTP error on {request.url.path}: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
def general_error_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong while processing your request"
        }
    )

@app.get("/")
def home():
    return {"message": "Welcome to the Complete ML Prediction API"}

@app.get("/health", response_model=HealthResponse)
def health():
    if model is None:
        logger.warning("Health check called but model is not loaded")
        raise HTTPException(status_code=503, detail="Model is not loaded")
    return HealthResponse(status="ok", model_loaded=True)

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    if model is None:
        logger.error("Prediction requested but model is not loaded")
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
    except Exception as e:
        logger.error(f"Model failed during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Model failed to generate a prediction")

    confidence = round(float(max(probabilities)), 2)
    predicted_class = class_names[prediction]

    logger.info(f"Prediction made: input={input_data[0]} -> {predicted_class} ({confidence})")

    return PredictionResponse(prediction=predicted_class, confidence=confidence)
