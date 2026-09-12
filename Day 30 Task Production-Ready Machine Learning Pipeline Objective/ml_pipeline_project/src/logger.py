import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configs import config


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(config.LOG_FILE)
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_format)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_format)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
