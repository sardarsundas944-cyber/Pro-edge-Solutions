# Day 38 - Multi-Service Deployment with Docker Compose

This project extends the Day 37 Dockerized ML Prediction API by adding a second service, Redis, and running both together using Docker Compose.

## Project Files

- main.py - FastAPI app with prediction endpoints and Redis integration
- train_model.py - trains a simple ML model and saves it as model.pkl
- requirements.txt - python packages needed
- Dockerfile - instructions to build the API image
- docker-compose.yml - runs the API service and the Redis service together
- .dockerignore - files and folders excluded from the docker image
- screenshots - proof that both services started and communicated

## What Changed From Day 37

The API now connects to a Redis service to store prediction counts. Every time someone calls the predict endpoint, the API increases a counter in Redis. This shows that the two containers can talk to each other over the same Docker network.

## Endpoints

- GET / - basic message to check the API is up
- GET /health - health check endpoint
- GET /redis-health - checks that the API can reach Redis
- POST /predict - send flower measurements and get a prediction, also updates Redis
- GET /stats - returns the prediction counts stored in Redis

## Requirements

- Docker installed on your machine
- Docker Compose (comes bundled with Docker Desktop)
- Get Docker here: https://docs.docker.com/get-started/

## How the Services Are Connected

The docker-compose.yml file defines two services, api and redis. Docker Compose automatically creates a network so both containers can reach each other by their service name. The API connects to Redis using the hostname "redis" which is passed in through environment variables, not hardcoded in the code.

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## How to Start Both Services

Open a terminal inside this folder and run:

```
docker compose up --build
```

This will:
1. Build the API image
2. Pull the Redis image
3. Start both containers on the same network
4. Map port 8000 for the API and port 6379 for Redis

To run it in the background, add -d:

```
docker compose up --build -d
```

Check both containers are running:

```
docker compose ps
```

## How to Test the Services

Check the API is up:

```
curl http://localhost:8000/
```

Check the API can talk to Redis:

```
curl http://localhost:8000/redis-health
```

Make a prediction, which also updates Redis:

```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

Check the stored stats from Redis:

```
curl http://localhost:8000/stats
```

You can also open http://localhost:8000/docs in your browser to test the endpoints.

## Screenshots

Screenshots showing the setup and testing steps are inside the screenshots folder:

1. screenshots/1_compose_up.png - result of docker compose up
2. screenshots/2_compose_ps.png - both containers running
3. screenshots/3_redis_health.png - checking the API can reach Redis
4. screenshots/4_predict_and_stats.png - making a prediction and reading stats from Redis

Note: these screenshots are sample outputs showing the expected result. Replace them with your own screenshots taken after running the commands on your machine.

## Stopping the Services

```
docker compose down
```

## Pushing to GitHub

```
git add .
git commit -m "Day 38: multi-service deployment with Docker Compose"
git push origin main
```
