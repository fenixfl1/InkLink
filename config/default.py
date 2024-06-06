import logging
import os
import re
import sys
import configparser


def resource_path(relative_path):
    """Get the absolute path to a resource, works for PyInstaller bundles."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIT_PATH = "config.ini"
TMP_DIR = resource_path(f"{ROOT_DIR}\\tmp")

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

FILE_LOGGER_HANDLER = logging.FileHandler(resource_path("logs.log"))
FILE_LOGGER_HANDLER.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(FILE_LOGGER_HANDLER)
logger.propagate = False

if not os.path.exists(CONFIT_PATH):
    print("*" * 75)
    print(f"{CONFIT_PATH}")
    print("*" * 75)
    logger.error("Configuration file not found.")
    raise FileNotFoundError("Configuration file not found.")

config = configparser.ConfigParser()
config.read(CONFIT_PATH)


def get_config(section, key):
    return config.get(section, key)


def set_config(section, key, value):
    config.set(section, key, value)
    with open(CONFIT_PATH, "w") as configfile:
        config.write(configfile)


def validate_config(section, key, value):
    if not key or not value:
        return False
    return True


__WS = ["WEBSOCKET_HOST", "WEBSOCKET_PORT"]
__DATABASE = ["DB_USERNAME", "DB_PASSWORD", "DB_DSN"]

for key in __WS:
    if not get_config("WEBSOCKET", key):
        logger.error(f"Configuration for {key} not found.")
        raise KeyError(f"Configuration for {key} not found.")

for key in __DATABASE:
    if not get_config("DATABASE", key):
        logger.error(f"Configuration for {key} not found.")
        raise KeyError(f"Configuration for {key} not found.")
