# Day 41 - Deploying the ML Prediction API to the Cloud

This project takes the Dockerized ML Prediction API built in Days 37 to 40 and prepares it for a public deployment on Render or Railway.

Important note: the files in this folder are fully ready to deploy, but the actual deployment has to be done from your own Render or Railway account, because it needs your own login and a connected GitHub repository. The screenshots in this folder are labeled sample mockups so you know what to expect. Replace them with real screenshots and your real live URL once you deploy.

## Project Files

- main.py - the FastAPI app
- config.py - production ready settings using Pydantic Settings
- train_model.py - trains the ML model
- requirements.txt - python packages needed
- Dockerfile - builds the image, reads the PORT variable the cloud platform gives it
- docker-compose.yml - for testing locally before you deploy
- render.yaml - blueprint file so Render can set up the API and Redis automatically
- railway.toml - config file so Railway knows how to build and start the app
- .env - local development values
- .env.example - template showing which variables are needed
- .gitignore - keeps .env out of version control
- screenshots - sample mockups of the deployment process

## Step 1: Test Locally First

Before deploying, make sure everything works on your machine:

```
docker compose up --build
```

Then check:

```
curl http://localhost:8000/health
```

## Step 2: Push Your Code to GitHub

```
git init
git add .
git commit -m "Day 41: ready for cloud deployment"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

Make sure .env is not pushed. Check your repository on GitHub afterward to confirm only .env.example is there, not .env.

## Option A: Deploying to Render

1. Go to https://render.com and sign in or create an account
2. Click New, then Blueprint
3. Connect your GitHub repository
4. Render will detect the render.yaml file in this project and set up two services automatically, the API and a Redis instance
5. When asked for the API_KEY value, type in your own secret value, for example a random string
6. Click Apply and wait for the build to finish
7. Once the build finishes, Render gives you a public URL like:

```
https://ml-prediction-api-yourname.onrender.com
```

8. Open that URL in your browser to confirm the API responds

If you prefer not to use the blueprint file, you can also create the web service manually:

1. Click New, then Web Service
2. Connect your repository
3. Set the environment to Docker
4. Add environment variables manually: APP_ENV=production, REDIS_HOST, REDIS_PORT, API_KEY
5. Create a separate Redis instance from New, then Redis, and copy its host and port into the API service variables

## Option B: Deploying to Railway

1. Go to https://railway.app and sign in or create an account
2. Click New Project, then Deploy from GitHub repo
3. Select your repository
4. Railway will detect the Dockerfile and railway.toml and build the image automatically
5. Click New, then Database, then Add Redis to add a Redis service to the same project
6. Open the API service settings and add these environment variables:

```
APP_ENV=production
REDIS_HOST=<your Redis service internal host, shown in the Redis service Variables tab>
REDIS_PORT=<your Redis service port, usually 6379>
API_KEY=<your own secret value>
```

7. Under Settings, go to Networking and click Generate Domain to get a public URL like:

```
https://ml-prediction-api-production.up.railway.app
```

8. Open that URL to confirm the API responds

## Step 3: Configure Environment Variables Securely

Whichever platform you use, set environment variables through the dashboard, not through a committed .env file. This keeps secrets like API_KEY out of your GitHub repository. The config.py file in this project requires REDIS_HOST and API_KEY to be present, so if you forget to set them, the app will fail to start and the platform logs will show a validation error.

## Step 4: Test the Live API

Once deployed, replace YOUR_LIVE_URL below with your actual link and test each endpoint:

```
curl https://YOUR_LIVE_URL/
curl https://YOUR_LIVE_URL/health
curl https://YOUR_LIVE_URL/config
curl -X POST https://YOUR_LIVE_URL/predict -H "Content-Type: application/json" -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
curl https://YOUR_LIVE_URL/stats
```

You can also open https://YOUR_LIVE_URL/docs in your browser to test everything visually.

## Live API URL

Replace this line with your actual deployed URL once you finish deploying:

```
Live URL: https://REPLACE-WITH-YOUR-DEPLOYED-URL
```

## Screenshots

The screenshots folder contains sample mockups showing what each step should look like:

1. screenshots/1_environment_variables_dashboard.png - example of setting environment variables on the platform dashboard
2. screenshots/2_deployment_build_log.png - example of a successful build and deploy log
3. screenshots/3_live_endpoint_test.png - example of testing the root and health endpoints on the live URL
4. screenshots/4_live_predict_test.png - example of testing the predict endpoint on the live URL

These are marked as sample mockups because an actual live deployment can only be created from your own hosting account. After you deploy, take your own screenshots of the real dashboard and real curl responses, and replace these files.

## Pushing to GitHub

```
git add .
git commit -m "Day 41: deployed ML Prediction API to the cloud"
git push origin main
```
