# Day 31 Task - REST APIs, HTTP Methods & API Design

## Objective

Learn the fundamentals of REST APIs, HTTP methods, status codes, and JSON data exchange
by designing a full API contract for a Machine Learning Prediction Service, before
actually building the model service.

## What is in this folder

```
ml-prediction-api-contract/
├── README.md                  This file
├── API_CONTRACT.md            The full API contract (endpoints, schemas, status codes)
├── app.py                     A simple test server that follows the contract
├── schemas/
│   ├── request_schema.json    Schema for the /predict request
│   ├── response_schema.json   Schema for the /predict response
│   └── error_schema.json      Schema used by all error responses
├── examples/
│   ├── health_response.json   Example response from /health
│   ├── predict_request.json   Example request to /predict
│   ├── predict_response.json  Example response from /predict
│   └── error_response.json    Example error response
└── screenshots/
    ├── health_check.png       GET /health result
    ├── prediction_success.png POST /predict success result
    ├── prediction_error.png   POST /predict bad request result
    └── not_found.png          Unknown endpoint 404 result
```

## Endpoints Designed

| Endpoint  | Method | Description                          |
|-----------|--------|----------------------------------------|
| /health   | GET    | Check that the API is running          |
| /predict  | POST   | Send input features, get a prediction  |

Full details, JSON schemas and status codes are in `API_CONTRACT.md`.

## How to run the test server

```
pip install flask
python app.py
```

The server will start on `http://127.0.0.1:5000`

## How to test it

Health check:
```
curl http://127.0.0.1:5000/health
```

Prediction:
```
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"
```

## HTTP Status Codes Used

- 200 OK - request worked fine
- 400 Bad Request - input data missing or wrong
- 404 Not Found - endpoint does not exist
- 405 Method Not Allowed - wrong HTTP method used
- 500 Internal Server Error - server side problem
- 503 Service Unavailable - model not loaded

## Learning Resources Used

- REST API Design: https://restfulapi.net/
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- JSON Introduction: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/JSON
- REST API Tutorial: https://restfulapi.net/http-methods/

## Submission Checklist

- [x] REST API contract designed
- [x] Request and response schemas documented
- [x] Appropriate HTTP status codes defined
- [x] Example JSON requests and responses included
- [x] README.md updated with API documentation
- [ ] Changes pushed to GitHub
