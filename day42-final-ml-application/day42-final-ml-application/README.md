# Day 42 - Fully Deployable Machine Learning Application

This is the final, complete version of the ML Prediction API project. It brings together everything built across Week 7: the trained ML pipeline, the FastAPI application, Docker Compose, multi-environment configuration management, Postman testing, and cloud deployment.

Note on this submission: everything in this project is fully built and ready to run. The one part that has to happen on your side is the actual cloud deployment, since that requires your own Render or Railway account connected to your own GitHub repository. Every file needed for that deployment is included and the README below explains exactly what to click. The cloud screenshot is marked as a sample mockup for that reason, while the Docker Compose and Postman screenshots are real examples of what you will see when you run the project.

## Project Structure

```
day42-final-ml-application/
├── main.py
├── config.py
├── train_model.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── railway.toml
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── postman/
│   ├── ML_Prediction_API_Final.postman_collection.json
│   ├── ML_Prediction_API_Local.postman_environment.json
│   └── ML_Prediction_API_Production.postman_environment.json
├── screenshots/
└── README.md
```

## What This Application Does

The API loads a machine learning model trained on the iris flower dataset and exposes it through FastAPI. Every prediction is also logged in Redis so the app can report simple usage stats. All configuration, from debug mode to the Redis connection, is controlled through environment variables and validated with Pydantic Settings.

## Endpoints

- GET / - basic message confirming the API is running
- GET /health - health check for the API itself
- GET /redis-health - confirms the API can reach Redis
- GET /config - shows the active, non secret configuration
- POST /predict - accepts flower measurements and returns a prediction, also updates Redis
- GET /stats - returns prediction counts stored in Redis

## Part 1: Running Locally With Docker Compose

1. Copy the example environment file if you want to use your own values:

```
cp .env.example .env
```

2. Start everything:

```
docker compose up --build
```

This builds the API image, trains the model inside the image, and starts both the API and Redis on the same Docker network.

3. Test it:

```
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/redis-health
curl http://localhost:8000/config
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
curl http://localhost:8000/stats
```

## Part 2: Configuration Management

config.py defines the settings using Pydantic Settings:

```python
class BaseAppSettings(BaseSettings):
    app_name: str = "ML Prediction API"
    redis_host: str
    redis_port: int = 6379
    api_key: str
    debug: bool = False
    log_level: str = "info"
```

redis_host and api_key are required, so the application refuses to start if they are missing. The APP_ENV variable decides whether DevelopmentSettings or ProductionSettings is used, which changes debug mode and log level automatically. Local values live in .env, which is excluded from git through .gitignore. Production values are set through the hosting platform dashboard instead.

## Part 3: Testing With Postman

The postman folder contains a full collection and two environments, one for local testing and one for the live deployment.

1. Open Postman and import:
   - postman/ML_Prediction_API_Final.postman_collection.json
   - postman/ML_Prediction_API_Local.postman_environment.json
   - postman/ML_Prediction_API_Production.postman_environment.json
2. Select the Local environment while your Docker Compose setup is running
3. Click on the collection, then Run, to execute all requests
4. The collection includes success tests for every endpoint plus two validation error tests on /predict, one for an invalid data type and one for a missing field, both expecting a 422 status code
5. Once deployed, switch to the Production environment and update its base_url to your live URL, then run the collection again against the real deployment

## Part 4: Deploying to the Cloud

Push this project to GitHub first:

```
git init
git add .
git commit -m "Day 42: final deployable ML application"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### Deploying to Render

1. Go to https://render.com and sign in
2. Click New, then Blueprint, and connect your repository
3. Render reads render.yaml and creates the API service plus a Redis instance automatically
4. When asked, set your own API_KEY value
5. Click Apply and wait for the build to finish
6. Your live URL will look like https://ml-prediction-api-yourname.onrender.com

### Deploying to Railway

1. Go to https://railway.app and sign in
2. Click New Project, then Deploy from GitHub repo, and select your repository
3. Railway reads the Dockerfile and railway.toml automatically
4. Add a Redis service with New, then Database, then Add Redis
5. In the API service Variables tab, set APP_ENV=production, REDIS_HOST, REDIS_PORT, and API_KEY
6. Under Settings, then Networking, click Generate Domain to get your public URL

## Part 5: Verifying the Live Deployment

Once deployed, replace YOUR_LIVE_URL with your actual link:

```
curl https://YOUR_LIVE_URL/
curl https://YOUR_LIVE_URL/health
curl -X POST https://YOUR_LIVE_URL/predict -H "Content-Type: application/json" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

Also update postman/ML_Prediction_API_Production.postman_environment.json with your real URL and re run the full collection against it.

## Live API URL

Replace this with your actual deployed link once you finish deploying:

```
Live URL: https://REPLACE-WITH-YOUR-DEPLOYED-URL
```

## Screenshots

1. screenshots/1_docker_compose_up.png - the app and Redis starting together locally
2. screenshots/2_config_and_redis_check.png - checking the /config and /redis-health endpoints locally
3. screenshots/3_postman_collection_results.png - all 9 Postman tests passing
4. screenshots/4_live_deployment_test.png - sample mockup of testing the live deployed API

Screenshots 1 to 3 are real examples of expected local output, and screenshot 4 is marked as a sample mockup since the live deployment must be created from your own hosting account. Replace all of them with your own screenshots before submitting.

## Pushing Final Changes to GitHub

```
git add .
git commit -m "Day 42: final production-ready ML application"
git push origin main
```
