# logging_config.py

import logging
from logging.handlers import RotatingFileHandler

def setup_logging():

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console logs
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    # File logs
    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=5_000_000,
        backupCount=5
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    root_logger.addHandler(console)
    root_logger.addHandler(file_handler)