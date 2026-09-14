# Machine Learning Prediction API - Contract

## 1. Overview

This document describes the REST API contract for a Machine Learning Prediction Service.
It defines all endpoints, HTTP methods, request formats, response formats and status codes.
This contract is designed first, before the actual model service is built.

Base URL (example):
```
http://localhost:5000
```

All data is sent and received as JSON.
Content-Type for all requests and responses: `application/json`

---

## 2. Endpoints Summary

| Endpoint    | Method | Purpose                                |
|-------------|--------|-----------------------------------------|
| /health     | GET    | Check if the API is running             |
| /predict    | POST   | Send input data and get a prediction    |

---

## 3. Health Check Endpoint

### GET /health

Used to check that the server is alive and ready to accept requests.

**Request**

No body needed.

```
GET /health
```

**Response Schema**

| Field   | Type   | Description                  |
|---------|--------|-------------------------------|
| status  | string | "ok" if service is healthy    |
| model_loaded | boolean | true if the ML model is loaded |

**Success Response - 200 OK**

```json
{
  "status": "ok",
  "model_loaded": true
}
```

**Error Response - 503 Service Unavailable**

```json
{
  "status": "error",
  "message": "Model is not loaded yet"
}
```

---

## 4. Prediction Endpoint

### POST /predict

Used to send input data to the model and receive a prediction back.

**Request Schema**

| Field    | Type          | Required | Description                          |
|----------|---------------|----------|----------------------------------------|
| features | array[number] | yes      | List of numeric input feature values   |

**Sample Request**

```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

**Response Schema (Success)**

| Field       | Type   | Description                              |
|-------------|--------|-------------------------------------------|
| prediction  | string | Predicted class or value                  |
| confidence  | number | Confidence score of the prediction (0-1)  |

**Success Response - 200 OK**

```json
{
  "prediction": "versicolor",
  "confidence": 0.97
}
```

---

## 5. Error Handling

All errors follow the same JSON error format.

**Error Schema**

| Field   | Type   | Description                     |
|---------|--------|-----------------------------------|
| error   | string | Short error name                  |
| message | string | Human readable explanation of error |

**400 Bad Request - Missing or invalid input**

```json
{
  "error": "Bad Request",
  "message": "features field is required and must be a list of numbers"
}
```

**404 Not Found - Wrong endpoint**

```json
{
  "error": "Not Found",
  "message": "The requested endpoint does not exist"
}
```

**405 Method Not Allowed**

```json
{
  "error": "Method Not Allowed",
  "message": "This endpoint does not support the requested HTTP method"
}
```

**500 Internal Server Error**

```json
{
  "error": "Internal Server Error",
  "message": "Something went wrong while making the prediction"
}
```

**503 Service Unavailable**

```json
{
  "error": "Service Unavailable",
  "message": "Model is not loaded yet"
}
```

---

## 6. HTTP Status Codes Used

| Code | Meaning               | Used When                                   |
|------|-----------------------|----------------------------------------------|
| 200  | OK                    | Request successful                           |
| 400  | Bad Request           | Invalid or missing input data                |
| 404  | Not Found             | Endpoint does not exist                      |
| 405  | Method Not Allowed    | Wrong HTTP method used on an endpoint        |
| 500  | Internal Server Error | Unexpected server/model error                |
| 503  | Service Unavailable   | Model not loaded / service not ready         |

---

## 7. REST Principles Followed

- Stateless: every request contains all the data needed, server does not store client state
- Resource based URLs: /predict and /health represent resources/actions, not verbs in the URL
- Correct HTTP methods: GET is used for reading status, POST is used for sending data to be processed
- JSON used for all requests and responses
- Meaningful status codes returned instead of always returning 200
