"""
Helper functions for the project are defined here.
"""

import logging
import uuid

from src.config.default import FILE_LOG_PATH


def get_file_logger(name: str, log_file: str) -> logging.Logger:
    """
    Returns a logger object with the given name and logs to a file.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.

    Returns:
        logging.Logger: Logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler = logging.FileHandler(f"{FILE_LOG_PATH}\\{log_file}")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def generateid():
    """
    Generate a unique id for the user.
    """

    return str(uuid.uuid4())
