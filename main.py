"""
This is the main file that starts the server.
"""

from src.service.windows_service import WindowsService

if __name__ == "__main__":
    service = WindowsService([])

    service.SvcDoRun()
