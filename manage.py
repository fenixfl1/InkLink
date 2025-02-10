"""
This is the main file that starts the server.
"""

import asyncio
import sys
import subprocess
import win32serviceutil

from src.service.windows_service import WindowsService
from src.utils.helpers import download_document, get_file_logger

from src.server import start_server

logger = get_file_logger(__name__)


def main():
    param = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        # switch case for the command
        match param:
            case "--install":
                WindowsService.install()
            case "--remove":
                WindowsService.remove()
            case "--start":
                WindowsService.start()
            case "--stop":
                WindowsService.stop()
            case "--status":
                WindowsService.status()
            case "--restart":
                WindowsService.restart()
            case "--run":
                # service = WindowsService(["InkLinkService"])
                # service.SvcDoRun()
                asyncio.run(start_server())
            case "--test":
                try:
                    subprocess.run(["pytest", "tests"])
                except Exception as e:
                    print(f"An error occurred while running tests - {e}")
            case "--help":
                WindowsService.help()
            case _:
                print("Unknown command, use --help for more information")
                sys.exit(1)
    except Exception as e:
        print(e)
        logger.error(f"Error while running {param}: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt as e:
        print("Server stopped")
