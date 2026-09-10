import os
from dotenv import load_dotenv

load_dotenv()

DATASET_PATH = os.getenv("DATASET_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")
APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")
PROJECT_AUTHOR = os.getenv("PROJECT_AUTHOR")
TEST_SIZE = float(os.getenv("TEST_SIZE"))
RANDOM_STATE = int(os.getenv("RANDOM_STATE"))
DEBUG_MODE = os.getenv("DEBUG_MODE") == "True"

def show_config():
    print("App Name:", APP_NAME)
    print("App Version:", APP_VERSION)
    print("Author:", PROJECT_AUTHOR)
    print("Dataset Path:", DATASET_PATH)
    print("Model Path:", MODEL_PATH)
    print("Test Size:", TEST_SIZE)
    print("Random State:", RANDOM_STATE)
    print("Debug Mode:", DEBUG_MODE)
