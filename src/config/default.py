"""
    This file contains the default configuration for the application.
"""

import os
from dotenv import load_dotenv

CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))

TMP_DIR = os.path.join(ROOT_DIR, "tmp")
FILE_LOG_PATH = os.path.join(ROOT_DIR, "logs")

load_dotenv(".env.local")

# Websocket server configuration
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST")
WEBSOCKET_PORT = os.getenv("WEBSOCKET_PORT")
HOSTS_ALLOWLIST = os.getenv("HOSTS_ALLOWLIST").split(",")
DEFAULT_PRINTER = os.getenv("DEFAULT_PRINTER")
