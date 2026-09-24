# Day 40 - API Testing with Postman

This project adds a Postman test collection for the ML Prediction API that runs through the Docker Compose setup from Day 38. The collection tests every endpoint for both successful and failing scenarios.

## Project Files

- main.py - the FastAPI app being tested
- train_model.py - trains the ML model used by the API
- requirements.txt - python packages needed
- Dockerfile - builds the API image
- docker-compose.yml - runs the API and Redis together
- .dockerignore
- postman/ML_Prediction_API.postman_collection.json - the exported Postman collection
- postman/ML_Prediction_API.postman_environment.json - the Postman environment with the base_url variable
- screenshots - proof that the tests were run and passed

## Endpoints Covered By The Collection

- GET / - basic root message
- GET /health - health check
- GET /redis-health - checks the API can reach Redis
- POST /predict - makes a prediction
- GET /stats - returns prediction counts from Redis
- An unknown route to check 404 handling

## Test Cases Included

1. Root Endpoint - Success (expects 200)
2. Health Check - Success (expects 200)
3. Redis Health - Success (expects 200)
4. Predict - Valid Input - Success (expects 200 and a prediction field)
5. Predict - Invalid Input Type - Validation Error (sends text instead of a number, expects 422)
6. Predict - Missing Required Field - Validation Error (removes petal_width, expects 422)
7. Stats - Success (expects 200)
8. Unknown Endpoint - Not Found (expects 404)

Every endpoint has at least one success test, and the predict endpoint also has two failure tests to check input validation.

## Step 1: Start the API

Open a terminal inside this folder and run:

```
docker compose up --build
```

This starts the ML Prediction API on port 8000 and Redis on port 6379.

## Step 2: Import the Collection into Postman

1. Open Postman
2. Click Import
3. Select postman/ML_Prediction_API.postman_collection.json
4. Click Import again
5. Repeat the same steps for postman/ML_Prediction_API.postman_environment.json

## Step 3: Select the Environment

In the top right corner of Postman, select "ML Prediction API - Local" from the environment dropdown. This sets the base_url variable to http://localhost:8000.

## Step 4: Run the Collection

1. Click on the collection name
2. Click Run
3. Click Run ML Prediction API
4. Postman will send every request in order and show pass or fail for each test

You can also run a single request by clicking on it and pressing Send, then checking the Test Results tab.

## Understanding the Failure Tests

The two validation error tests are supposed to fail the request but pass the test, because we are checking that the API correctly rejects bad input.

- Sending sepal_length as text instead of a number should return a 422 status code
- Removing the petal_width field should also return a 422 status code

If the API returned a 200 status code for these cases instead, that would mean validation is broken, and the Postman test would fail, alerting us to the bug.

## Screenshots

Screenshots showing the collection running and individual test results are inside the screenshots folder:

1. screenshots/1_collection_runner_results.png - all 8 tests passing in the Collection Runner
2. screenshots/2_predict_valid_test.png - the valid predict request and its passing tests
3. screenshots/3_predict_invalid_type_test.png - the invalid input type request returning a 422 error
4. screenshots/4_predict_missing_field_test.png - the missing field request returning a 422 error

Note: these screenshots are sample outputs showing the expected result. Replace them with your own screenshots taken after running the collection in Postman on your machine.

## Pushing to GitHub

```
git add .
git commit -m "Day 40: API testing with Postman"
git push origin main
```
