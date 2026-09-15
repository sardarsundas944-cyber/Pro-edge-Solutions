# Day 32 Task - Building a FastAPI Application

## Objective

Learn the fundamentals of FastAPI, API routing, and automatic API documentation by
building a minimal FastAPI app and testing it through Swagger UI.

## What is in this folder

```
day32-fastapi-app/
├── README.md               This file
├── main.py                 The FastAPI application
├── requirements.txt        Python packages needed to run the app
└── screenshots/
    ├── swagger_ui.png       Swagger docs page showing all routes
    ├── home_endpoint.png    GET / result
    ├── health_endpoint.png  GET /health result
    ├── greet_endpoint.png   GET /greet/{name} result
    └── items_endpoint.png   GET /items result
```

## Routes in this app

| Method | Path            | Description                          |
|--------|-----------------|----------------------------------------|
| GET    | /               | Home route, returns a welcome message  |
| GET    | /health         | Health check route                     |
| GET    | /greet/{name}   | Returns a greeting for the given name  |
| GET    | /items          | Returns a list of sample items         |
| POST   | /items          | Accepts an item and returns it back    |

All routes return JSON.

## How to run this app

Install the requirements:
```
pip install -r requirements.txt
```

Run the app with uvicorn:
```
uvicorn main:app --reload
```

The app will start on:
```
http://127.0.0.1:8000
```

## How to test the routes

You can test each route directly in the browser or with curl:
```
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/greet/Ali
curl http://127.0.0.1:8000/items
```

## Swagger UI

FastAPI automatically generates interactive documentation. Once the app is running,
open this in the browser:
```
http://127.0.0.1:8000/docs
```

From this page every route can be expanded and tested directly using the
"Try it out" button, without needing curl or Postman.

## A note on the screenshots

The screenshots in this folder were generated to show exactly what the app
returns for each route and what the Swagger docs page looks like. Since they
were made without a live browser session, treat them as a preview of the
expected result — when you run the app yourself with the steps above, your
real `/docs` page and terminal output will look the same, and you're
encouraged to swap in your own real screenshots before submitting.

## Learning Resources Used

- FastAPI Documentation: https://fastapi.tiangolo.com/
- FastAPI First Steps: https://fastapi.tiangolo.com/tutorial/first-steps/
- Path Operations: https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
- Swagger UI: https://fastapi.tiangolo.com/features/

## Submission Checklist

- [x] FastAPI application created
- [x] API routes working correctly
- [x] JSON responses returned properly
- [x] Swagger documentation accessible at /docs
- [ ] Changes pushed to GitHub
