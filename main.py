"""
This is the main file that starts the server.
"""

from src.config.default import ROOT_DIR
from src.server import start_server
from watcher import hot_reload

if __name__ == "__main__":

    print("*" * 75)
    print(f"{ROOT_DIR}")
    print("*" * 75)
    hot_reload()
    start_server()
