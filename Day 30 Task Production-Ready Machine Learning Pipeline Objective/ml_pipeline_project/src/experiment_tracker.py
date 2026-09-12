import os
import sys
import csv
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import config
from src.logger import get_logger

logger = get_logger("experiment_tracker")


def log_experiment(model_name, params, metrics, version):
    file_exists = os.path.exists(config.EXPERIMENT_FILE)

    with open(config.EXPERIMENT_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "model_name", "training_date", "parameters",
                "accuracy", "f1_score", "model_version"
            ])

        writer.writerow([
            model_name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(params),
            metrics.get("accuracy"),
            metrics.get("f1_score"),
            version
        ])

    logger.info("Experiment logged for model %s version %s", model_name, version)
