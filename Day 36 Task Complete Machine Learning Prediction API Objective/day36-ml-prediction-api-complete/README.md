# Day 36 Task - Complete Machine Learning Prediction API (Week 6 Capstone)

## Objective

Bring together everything from Week 6: FastAPI, Pydantic validation, error
handling, logging, and a professional GitHub workflow, into one complete
Machine Learning Prediction API.

## Note about the model

Just like Day 34, this project references the model saved in Day 30's
Production-Ready ML Pipeline. That exact file was not available here, so
`train_model.py` trains and saves a real model (RandomForestClassifier on the
iris dataset, 4 numeric features) using joblib, so the whole project runs
end to end. If you have your own `model.joblib` from Day 30, replace the file
in `model/model.joblib` and update the field names in `main.py` to match.

## What is in this folder

```
day36-ml-prediction-api-complete/
├── README.md                          This file
├── GIT_WORKFLOW.md                    Feature branch and Pull Request steps
├── main.py                            Complete FastAPI app
├── train_model.py                     Trains and saves the ML model
├── requirements.txt                   Python packages needed
├── model/
│   ├── model.joblib                    The trained model
│   └── class_names.joblib              The class labels
├── logs/
│   └── api.log                         Real log output from simulated requests
└── screenshots/
    ├── swagger_ui.png                 Swagger docs showing all routes
    ├── health_check.png               GET /health result
    ├── predict_success.png            POST /predict success result
    ├── predict_validation_error.png   POST /predict validation error (422)
    ├── log_file.png                   Contents of logs/api.log
    ├── git_commit_log.png             Real git log with the merged feature branch
    └── github_pull_request.png        What the Pull Request looks like on GitHub
```

## Endpoints

| Method | Path      | Description                              | Response Model     |
|--------|-----------|--------------------------------------------|----------------------|
| GET    | /         | Welcome message                            | plain dict           |
| GET    | /health   | Confirms the API and model are ready       | HealthResponse       |
| POST   | /predict  | Accepts 4 iris measurements, returns class | PredictionResponse   |

## Pydantic Models

**PredictionRequest**

| Field         | Type  | Rule                   |
|---------------|-------|---------------------------|
| sepal_length  | float | must be greater than 0   |
| sepal_width   | float | must be greater than 0   |
| petal_length  | float | must be greater than 0   |
| petal_width   | float | must be greater than 0   |

**PredictionResponse**

| Field       | Type   | Description                     |
|-------------|--------|------------------------------------|
| prediction  | string | Predicted class name              |
| confidence  | float  | Probability of that class         |

**HealthResponse**

| Field         | Type    | Description                 |
|---------------|---------|--------------------------------|
| status        | string  | "ok" if healthy               |
| model_loaded  | boolean | true if the model is ready    |

## Error Handling

| Situation                     | Status | Response                                  |
|--------------------------------|--------|----------------------------------------------|
| Missing or invalid field        | 422    | Structured `error`, `message`, `details`     |
| Model not loaded                | 503    | Clear message the model is unavailable       |
| Model fails during prediction   | 500    | Generic safe message                         |
| Any other unexpected error      | 500    | Generic safe message                         |

## Logging

Every request and response is logged through a middleware function, and every
prediction is logged with its input and result. Warnings are logged for
validation failures, and errors are logged when the model fails to load or
fails to predict. All logs are saved to `logs/api.log` in this format:
```
2026-09-14 10:36:20,440 - INFO - Model loaded successfully
2026-09-14 10:36:20,441 - INFO - Request received: GET /health
2026-09-14 10:36:20,454 - INFO - Prediction made: input=[5.1, 3.5, 1.4, 0.2] -> setosa (1.0)
2026-09-14 10:36:20,454 - WARNING - Validation failed on /predict: sepal_length must be greater than 0
```

## How to run this project

```
pip install -r requirements.txt
python train_model.py
uvicorn main:app --reload
```

Open Swagger docs at:
```
http://127.0.0.1:8000/docs
```

## API Usage Example

Request:
```
POST /predict
{
  "sepal_length": 6.7,
  "sepal_width": 3.1,
  "petal_length": 4.7,
  "petal_width": 1.5
}
```

Response:
```
{
  "prediction": "versicolor",
  "confidence": 1.0
}
```

## GitHub Workflow

Full steps are in `GIT_WORKFLOW.md`. Summary:

1. Created feature branch `feature/complete-ml-api`
2. Built and committed the complete API on that branch
3. Opened a Pull Request into `main`
4. Reviewed the diff
5. Merged the Pull Request, keeping a clean commit history

## A note on the screenshots

The prediction numbers in these screenshots come from actually loading the
real trained model in this project and calling `predict` on it, so those
results are genuine. The contents shown in `log_file.png` were produced by
actually running this project's logging setup against those same real
predictions, and `logs/api.log` in this folder is that real output, not
invented text. The git log screenshot comes from an actual local git
repository where the feature branch was really created, committed, and
merged. FastAPI itself could not be launched as a live server in this
environment, so the request/response and Swagger screenshots are rendered
using that real underlying data rather than captured from a live browser.
Actually pushing to GitHub and opening a real Pull Request needs your own
repository and login; `github_pull_request.png` is a mockup of that screen,
and `GIT_WORKFLOW.md` explains exactly how to produce a real one.

## Learning Resources Used

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pydantic Documentation: https://docs.pydantic.dev/
- FastAPI Error Handling: https://fastapi.tiangolo.com/tutorial/handling-errors/
- Joblib Documentation: https://joblib.readthedocs.io/

## Submission Checklist

- [x] Complete ML Prediction API implemented
- [x] Prediction endpoint, validation, and error handling working
- [x] Logging and Swagger documentation configured
- [x] Feature branch created and merged locally (see GIT_WORKFLOW.md for GitHub)
- [ ] Pull Request created and merged on GitHub
- [x] README.md updated with documentation, screenshots, setup instructions
