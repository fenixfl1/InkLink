import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

from src.config.default import ROOT_DIR


class WatchEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # This method is called when the watched file is modified
        print(f"Changes detected in {event.src_path}. Restarting server...")
        subprocess.run(
            ["python", "server.py"]
        )  # Replace with your actual server start command


def hot_reload() -> None:
    event_handler = WatchEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=ROOT_DIR, recursive=False)
    observer.start()

    print("*" * 75)
    print(f'{ "Watching for changes in the server..." :^75}')
    print("*" * 75)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
