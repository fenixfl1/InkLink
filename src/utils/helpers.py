"""
Helper functions for the project are defined here.
"""

import logging
import uuid

import requests

from src.config.default import FILE_LOG_PATH, TMP_DIR


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


logger = get_file_logger(__name__, "helpers.log")


async def download_document(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = f"{TMP_DIR}\\{generateid()}.pdf"

            with open(file_path, "wb") as f:
                f.write(response.content)

            return file_path
        else:
            print(f"Failed to download PDF from {url}")
    except Exception as e:
        logger.error(f"An error occurred while downloading the PDF - {e}")
