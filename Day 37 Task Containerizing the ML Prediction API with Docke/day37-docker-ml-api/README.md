# Day 37 - Containerizing the ML Prediction API with Docker

This project takes the ML Prediction API from Day 36 and packages it into a Docker container so it can run the same way on any machine.

## Project Files

- main.py - the FastAPI app with the prediction endpoints
- train_model.py - trains a simple ML model and saves it as model.pkl
- requirements.txt - python packages needed
- Dockerfile - instructions to build the docker image
- .dockerignore - files and folders excluded from the docker image
- screenshots - proof that the container was built and tested

## What the API Does

The API loads a small machine learning model trained on the iris flower dataset. You send it 4 numbers and it tells you the predicted flower type.

Endpoints:
- GET / - basic message to check the API is up
- GET /health - health check endpoint
- POST /predict - send flower measurements and get a prediction

## Requirements

- Docker installed on your machine
- Get Docker here: https://docs.docker.com/get-started/

## How to Build the Docker Image

Open a terminal inside this folder and run:

```
docker build -t ml-prediction-api .
```

This will:
1. Pull a lightweight python base image
2. Install the required packages
3. Copy the project files into the image
4. Train the model inside the image
5. Set up the container to run the API on port 8000

## How to Run the Container

```
docker run -d -p 8000:8000 ml-prediction-api
```

This runs the container in the background and maps port 8000 on your computer to port 8000 inside the container.

Check that it is running:

```
docker ps
```

## How to Test the API

Open your browser or use curl.

Check the root endpoint:

```
curl http://localhost:8000/
```

Check the health endpoint:

```
curl http://localhost:8000/health
```

Make a prediction:

```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

You should get back something like:

```
{"prediction":"setosa"}
```

You can also open http://localhost:8000/docs in your browser to see the automatic FastAPI documentation and test the endpoints from there.

## Screenshots

Screenshots showing the build, run, and testing steps are inside the screenshots folder:

1. screenshots/1_docker_build.png - result of docker build
2. screenshots/2_docker_run.png - container running with docker run and docker ps
3. screenshots/3_health_check.png - testing the root and health endpoints
4. screenshots/4_predict_endpoint.png - testing the predict endpoint

Note: these screenshots are sample outputs showing the expected result. Replace them with your own screenshots taken after running the commands on your machine.

## Stopping the Container

```
docker ps
docker stop <container_id>
```

## Pushing to GitHub

```
git add .
git commit -m "Day 37: containerized ML Prediction API with Docker"
git push origin main
```
