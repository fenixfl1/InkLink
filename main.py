"""
This is the main file that starts the server.
"""

# from src.service.windows_service import WindowsService
from src.server import start_server

if __name__ == "__main__":
    start_server()
