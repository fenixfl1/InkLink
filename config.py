"""
    This file contains the default configuration for the application.
"""

import os
import sys
from dotenv import load_dotenv


def resource_path(relative_path):
    """
    This function is used to get the absolute path of the file in the
    """
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

TMP_DIR = resource_path(f"{ROOT_DIR}\\tmp")
FILE_LOG_PATH = f"{ROOT_DIR}\\InkLinkLogs.log"
PDF_VIEWER_FOLDER = f"{ROOT_DIR}\\SumatraPDF"
PDF_VIEWER_PATH = f"{ROOT_DIR}\\SumatraPDF\\SumatraPDF.exe"
PDF_VIEWER_TEMP_FOLDER = f"{ROOT_DIR}\\SumatraPDF\\sumatrapdfcache"


load_dotenv(".env.local")


# Websocket server configuration
with open(resource_path(".InkLinkConfig.cfg"), "r") as f:
    config = f.read()
    WEBSOCKET_HOST = config.split("\n")[0].split("=")[1].strip()
    WEBSOCKET_PORT = config.split("\n")[1].split("=")[1].strip()
    HOSTS_ALLOWLIST = config.split("\n")[2].split("=")[1].split(",")
    CLIENTS_ALLOWLIST = config.split("\n")[3].split("=")[1].split(",")
