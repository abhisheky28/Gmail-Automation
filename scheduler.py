# scheduler.py
import time
import random
import subprocess

# --- Configuration ---
SCRIPT_TO_RUN = "main.py"
MIN_DELAY_MINUTES = 20
MAX_DELAY_MINUTES = 50

if __name__ == "__main__":
    print(f"[{time.ctime()}] Starting scheduler. Will run '{SCRIPT_TO_RUN}' every {MIN_DELAY_MINUTES}-{MAX_DELAY_MINUTES} minutes.")
    
    while True:
        try:
            print(f"[{time.ctime()}] Scheduler is triggering '{SCRIPT_TO_RUN}'.")
            # Execute the main script as a separate process.
            subprocess.run(["python", SCRIPT_TO_RUN], check=True)
            print(f"[{time.ctime()}] Main script finished execution.")

        except subprocess.CalledProcessError as e:
            print(f"[{time.ctime()}] Error during scheduled run of {SCRIPT_TO_RUN}: {e}")
        except FileNotFoundError:
            print(f"[{time.ctime()}] Error: 'python' command not found. Make sure Python is in your system's PATH.")
            break # Exit if python isn't found
        
        # Calculate the next run time with a random delay
        delay_seconds = random.randint(MIN_DELAY_MINUTES * 60, MAX_DELAY_MINUTES * 60)
        minutes, seconds = divmod(delay_seconds, 60)
        print(f"[{time.ctime()}] Next run scheduled in {minutes} minutes and {seconds} seconds.")
        
        time.sleep(delay_seconds)