# Day 39 - Production-Ready Configuration Management

This project upgrades the ML Prediction API with proper configuration management. Instead of hardcoding values in the code, all settings now come from environment variables and are validated using Pydantic Settings. The app also supports separate development and production configurations.

## Project Files

- main.py - FastAPI app that reads all settings from config.py
- config.py - Pydantic Settings classes for development and production
- train_model.py - trains a simple ML model and saves it as model.pkl
- requirements.txt - python packages needed
- Dockerfile - builds the API image
- docker-compose.yml - runs the API and Redis together, loads variables from .env
- .env - local development values (not committed to git)
- .env.example - template showing which variables are needed
- .env.production.example - template for production values
- .gitignore - keeps .env and other secrets out of version control
- screenshots - proof that config loading and validation work

## How Configuration Works

All settings are defined in config.py using Pydantic Settings.

```python
class BaseAppSettings(BaseSettings):
    app_name: str = "ML Prediction API"
    redis_host: str
    redis_port: int = 6379
    api_key: str
    debug: bool = False
    log_level: str = "info"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
```

redis_host and api_key have no default value, which means they are required. If they are missing, the app will raise a validation error and refuse to start.

There are two settings classes:

- DevelopmentSettings - debug is on, log level is "debug"
- ProductionSettings - debug is off, log level is "warning"

The app picks the right one based on the APP_ENV variable.

```python
def get_settings():
    app_env = os.getenv("APP_ENV", "development").lower()
    if app_env == "production":
        return ProductionSettings()
    return DevelopmentSettings()
```

## Local Development Setup

1. Copy the example file:

```
cp .env.example .env
```

2. Fill in your own values inside .env, for example:

```
APP_ENV=development
REDIS_HOST=redis
REDIS_PORT=6379
API_KEY=dev-local-key-123
```

3. Start the app with Docker Compose:

```
docker compose up --build
```

Docker Compose automatically loads the .env file and passes the variables into the container.

## Production Setup

For production, do not use a .env file inside the container. Instead, set the environment variables directly on your deployment platform (for example Render, Railway, AWS, or a Kubernetes secret).

Use .env.production.example as a reference for which variables need to be set:

```
APP_ENV=production
REDIS_HOST=your-production-redis-host
REDIS_PORT=6379
API_KEY=set-this-in-your-deployment-platform
```

When APP_ENV is set to production, the app automatically switches to ProductionSettings, turning off debug mode and lowering the log level.

## Checking the Active Configuration

Once the app is running, you can see the current configuration (without exposing the secret API key) at:

```
curl http://localhost:8000/config
```

## What Happens If a Required Variable Is Missing

If REDIS_HOST or API_KEY is not set anywhere (not in .env, not in the environment), Pydantic Settings raises a validation error and the app will not start. This prevents the API from running with broken or missing configuration.

## Keeping Secrets Safe

The .env file is listed in .gitignore so it is never pushed to GitHub. Only .env.example and .env.production.example are committed, and they contain placeholder values, not real secrets.

## Screenshots

Screenshots showing configuration behavior are inside the screenshots folder:

1. screenshots/1_dev_startup.png - app starting successfully in development mode
2. screenshots/2_dev_config_endpoint.png - /config endpoint showing development settings
3. screenshots/3_production_config_endpoint.png - /config endpoint showing production settings
4. screenshots/4_missing_variable_error.png - app failing to start when a required variable is missing

Note: these screenshots are sample outputs showing the expected result. Replace them with your own screenshots taken after running the commands on your machine.

## Pushing to GitHub

```
git add .
git commit -m "Day 39: production-ready configuration management"
git push origin main
```
