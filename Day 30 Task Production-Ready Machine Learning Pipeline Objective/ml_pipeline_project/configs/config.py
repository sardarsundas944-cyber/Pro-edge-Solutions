import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "configs", ".env")

load_dotenv(ENV_PATH)

MODEL_DIR = os.path.join(BASE_DIR, os.getenv("MODEL_DIR", "models"))
DATA_DIR = os.path.join(BASE_DIR, os.getenv("DATA_DIR", "data"))
LOG_DIR = os.path.join(BASE_DIR, os.getenv("LOG_DIR", "logs"))
LOG_FILE = os.path.join(BASE_DIR, os.getenv("LOG_FILE", "logs/app.log"))
EXPERIMENT_FILE = os.path.join(BASE_DIR, os.getenv("EXPERIMENT_FILE", "experiments/experiments.csv"))

MODEL_NAME = os.getenv("MODEL_NAME", "model")
MODEL_VERSION = os.getenv("MODEL_VERSION", "1.0.0")

TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
RANDOM_STATE = int(os.getenv("RANDOM_STATE", 42))
N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", 100))
MAX_DEPTH = int(os.getenv("MAX_DEPTH", 5))

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "raw"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "processed"), exist_ok=True)
os.makedirs(os.path.dirname(EXPERIMENT_FILE), exist_ok=True)
