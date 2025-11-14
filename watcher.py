# watcher.py
import time
import subprocess
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
CONFIG_FILE = 'config.json'
SCRIPT_TO_RUN = "main.py"
# <<<--- NEW: Cooldown period in seconds to prevent the script from re-triggering itself ---
COOLDOWN_SECONDS = 10

# --- Load config to get the path to watch ---
try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    contacts_file_path = config['file_paths']['contacts_file']
    watch_directory = os.path.dirname(contacts_file_path)
    watch_filename = os.path.basename(contacts_file_path)
except (FileNotFoundError, KeyError) as e:
    print(f"[{time.ctime()}] FATAL ERROR: Could not load watch path from {CONFIG_FILE}. Please check the config. Error: {e}")
    exit()

class ExcelEventHandler(FileSystemEventHandler):
    """Handles events for the contacts.xlsx file with a cooldown to prevent loops."""
    # <<<--- NEW: Track the last time the script was triggered ---
    def __init__(self):
        self.last_triggered = 0

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(watch_filename):
            # <<<--- NEW: Check if the cooldown period has passed ---
            current_time = time.time()
            if (current_time - self.last_triggered) < COOLDOWN_SECONDS:
                print(f"[{time.ctime()}] Change detected during cooldown. Ignoring.")
                return

            # <<<--- NEW: Update the trigger time before running the script ---
            self.last_triggered = current_time
            
            print(f"[{time.ctime()}] Detected change in {watch_filename}. Triggering main script.")
            try:
                subprocess.run(["python", SCRIPT_TO_RUN], check=True)
            except subprocess.CalledProcessError as e:
                print(f"[{time.ctime()}] Error running {SCRIPT_TO_RUN}: {e}")
            except FileNotFoundError:
                print(f"[{time.ctime()}] Error: 'python' command not found. Make sure Python is in your system's PATH.")

if __name__ == "__main__":
    path = watch_directory
    event_handler = ExcelEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    print(f"[{time.ctime()}] Starting file watcher for '{watch_filename}' in directory: '{path}'...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print(f"[{time.ctime()}] File watcher stopped by user.")
    
    observer.join()