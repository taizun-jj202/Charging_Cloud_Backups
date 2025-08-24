"""
Watchdog script to monitor a folder for new log files.
When a new file is detected, it executes a Python uploader script.
"""

import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()


# --- Configuration ---
# Folder to watch
WATCH_FOLDER    = os.getenv('WATCH_FOLDER')
UPLOADER_SCRIPT = os.getenv('UPLOADER_SCRIPT')
PYTHON_PATH     = os.getenv('CUSTOM_PYTHON_PATH')
# --- End Configuration ---


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggered when a file is created in the folder"""
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)
        print(f"[WATCHDOG] New file detected: {filename}")

        try:
            # Run your uploader script, passing the new file as argument
            result = subprocess.run(
                [PYTHON_PATH, UPLOADER_SCRIPT, event.src_path],
                capture_output=True,
                text=True
            )

            print(f"[WATCHDOG] Uploader stdout:\n{result.stdout}")
            print(f"[WATCHDOG] Uploader stderr:\n{result.stderr}")

            if result.returncode == 0:
                print(f"[WATCHDOG] Successfully uploaded {filename}")
            else:
                print(f"[WATCHDOG] Upload script failed for {filename}")

        except Exception as e:
            print(f"[WATCHDOG] Error while uploading {filename}: {e}")


def main():
    print(f"[WATCHDOG] Starting watchdog on: {WATCH_FOLDER}")
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
