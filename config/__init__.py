from .default import ROOT_DIR, get_config

# extract th values from the config dictionary
WEBSOCKET_PORT: str = get_config("WEBSOCKET", "WEBSOCKET_PORT")
WEBSOCKET_HOST: str = get_config("WEBSOCKET", "WEBSOCKET_HOST")
DB_USERNAME = get_config("DATABASE", "DB_USERNAME")
DB_PASSWORD = get_config("DATABASE", "DB_PASSWORD")
DB_DSN = get_config("DATABASE", "DB_DSN")
SERVICE_NAME = get_config("SERVICE", "SERVICE_NAME")
SERVICE_DISPLAY_NAME = get_config("SERVICE", "SERVICE_DISPLAY_NAME")
SERVICE_DESCRIPTION = get_config("SERVICE", "SERVICE_DESCRIPTION")


__all__ = [
    "WEBSOCKET_PORT",
    "WEBSOCKET_HOST",
    "DB_USERNAME",
    "DB_PASSWORD",
    "DB_DSN",
    "ROOT_DIR",
]
