# Automated Sales Outreach Engine - Setup Guide

This document provides instructions on how to run the automation engine's background services on different operating systems.

## Prerequisites

1.  Ensure Python 3.8+ is installed.
2.  Navigate to the project directory in your terminal.
3.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Background Services

The engine relies on two long-running scripts: `watcher.py` and `scheduler.py`. They should be started and left to run in the background.

### On Linux / macOS

Using `nohup` is a simple and effective way to run a script in the background and ensure it keeps running even after you close the terminal.

1.  **Start the File Watcher:**
    ```bash
    nohup python -u watcher.py > watcher.log 2>&1 &
    ```
    *   `nohup`: Prevents the process from being terminated when the terminal closes.
    *   `python -u`: Runs Python in unbuffered mode, so logs appear in real-time.
    *   `> watcher.log 2>&1`: Redirects all output (stdout and stderr) to a log file.
    *   `&`: Puts the process into the background.

2.  **Start the Scheduler:**
    ```bash
    nohup python -u scheduler.py > scheduler.log 2>&1 &
    ```

3.  **To Stop the Services:**
    You can find the process ID (PID) and stop them manually.
    ```bash
    # Find the PIDs
    ps aux | grep watcher.py
    ps aux | grep scheduler.py

    # Stop the process using its PID
    kill <PID_of_watcher>
    kill <PID_of_scheduler>
    ```

### On Windows

On Windows, you can use `pythonw.exe` to run the scripts without a visible console window.

1.  **Open Command Prompt or PowerShell.**

2.  **Start the File Watcher:**
    ```cmd
    start pythonw.exe watcher.py
    ```

3.  **Start the Scheduler:**
    ```cmd
    start pythonw.exe scheduler.py
    ```

4.  **To Stop the Services:**
    You will need to use the Task Manager.
    *   Open Task Manager (Ctrl+Shift+Esc).
    *   Go to the "Details" tab.
    *   Find the `pythonw.exe` processes. You may need to check the "Command Line" column to identify which one is running `watcher.py` vs. `scheduler.py`.
    *   Select the process and click "End task".