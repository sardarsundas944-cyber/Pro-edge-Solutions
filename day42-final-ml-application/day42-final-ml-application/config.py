from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class BaseAppSettings(BaseSettings):
    app_name: str = "ML Prediction API"
    redis_host: str
    redis_port: int = 6379
    api_key: str
    debug: bool = False
    log_level: str = "info"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class DevelopmentSettings(BaseAppSettings):
    debug: bool = True
    log_level: str = "debug"

class ProductionSettings(BaseAppSettings):
    debug: bool = False
    log_level: str = "warning"

@lru_cache
def get_settings():
    app_env = os.getenv("APP_ENV", "development").lower()
    if app_env == "production":
        return ProductionSettings()
    return DevelopmentSettings()

settings = get_settings()
