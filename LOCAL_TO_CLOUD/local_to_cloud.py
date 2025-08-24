"""

This script creates a file-watchdog. 
i.e if a new log file is created, this file uploads the new log file to the 
corresponding GitHub/AWS S3 repo. 


This script is being tested to upload log files to GitHub. 


@author : Taizun J 
@date   : 21:43:18 Aug 20 2025
"""


import os
import subprocess
import glob
import shutil
import logging
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration ---
# Load environment variables from a .env file
load_dotenv()

# Folder where your log files are saved.
SESSION_LOG_FOLDER_PATH   = os.getenv('SESSION_LOG_FOLDER_PATH')
# Path to your calculation program (log_energy_calculator.py).
CALCULATION_PROGRAM_PATH  = os.getenv('CALCULATION_PROGRAM_PATH')
# GitHub repository local path.
GITHUB_REPO_PATH          = os.getenv('GITHUB_REPO_PATH')
GITHUB_COMMIT_MESSAGE     = "New Session Log"
# File to track which logs have been processed.
PROCESSED_FILES_LOG       = os.getenv('PROCESSED_FILE_LOG')
LOG_FILE_PATH             = os.getenv('LOG_FILE_PATH')
CUSTOM_PYTHON_PATH        = os.getenv('CUSTOM_PYTHON_PATH')
print(f'LOG file : {LOG_FILE_PATH}')
# --- End of Configuration ---



log_file_path = os.path.join(os.path.dirname(__file__), os.getenv('SESSION_LOG_FILE'))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file_path,
    filemode='w'
)



def get_processed_files():
    """
    Reads the list of already processed files from the tracking file.
    Returns a set of filenames for efficient lookup.
    """
    if not os.path.exists(PROCESSED_FILES_LOG):
        return set()
    try:
        with open(PROCESSED_FILES_LOG, 'r') as f:
            # Read lines and strip any whitespace/newlines
            return set(line.strip() for line in f if line.strip())
    except IOError as e:
        logging.info(f"Error reading processed files log: {e}")
        return set()

def log_processed_file(filename):
    """
    Appends a successfully processed filename to our tracking file.
    """
    try:
        with open(PROCESSED_FILES_LOG, 'a') as f:
            f.write(filename + '\n')
    except IOError as e:
        logging.info(f"Error writing to processed files log: {e}")


def upload_to_cloud(file_path):
    """
    Copies the file to the git repo, then adds, commits, and pushes it.
    Returns True on success, False on failure.
    """
    if not GITHUB_REPO_PATH or not os.path.isdir(GITHUB_REPO_PATH):
        logging.info(f"Error: GITHUB_REPO_PATH '{GITHUB_REPO_PATH}' is not a valid directory.")
        return False
        
    filename = os.path.basename(file_path)
    destination_path = os.path.join(GITHUB_REPO_PATH, filename)

    try:
        # --- FIX: Copy the log file into the repository folder first ---
        logging.info(f"Uploading {filename} to configured repository...")
        # Commands are run in the context of the repository folder (cwd).
        subprocess.run(["git", "pull"], cwd=GITHUB_REPO_PATH, check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], cwd=GITHUB_REPO_PATH, check=True)
        
        commit_process = subprocess.run(
            ["git", "commit", "-m", f"{GITHUB_COMMIT_MESSAGE}: {filename}"],
            cwd=GITHUB_REPO_PATH, capture_output=True, text=True
        )
        
        # Git commit returns 1 if there's nothing to commit, which is not an error here.
        if commit_process.returncode > 1:
            raise subprocess.CalledProcessError(commit_process.returncode, commit_process.args, commit_process.stdout, commit_process.stderr)
        elif "nothing to commit" in commit_process.stdout:
            logging.info("No changes to commit. File may be identical to the one in the repo.")
        
        logging.info(" - Upload successful.")
        subprocess.run(["git", "push"], cwd=GITHUB_REPO_PATH, check=True)
        return True
        
    except shutil.Error as e:
        logging.info(f"Error copying file: {e}")
        return False
    except subprocess.CalledProcessError as e:
        logging.info(f"Error during git operation for {filename}.")
        logging.info(f"Command failed: {' '.join(e.cmd)}")
        logging.info(f"Stderr: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print("Error: Git command not found. Make sure Git is installed and in your system's PATH.")
        logging.info("Error: Git command not found. Make sure Git is installed and in your system's PATH.")
        return False


def run_calculation(file_path):
    """
    Runs the external calculation program on the given file.
    Returns True on success, False on failure.
    """
    if not CALCULATION_PROGRAM_PATH or not os.path.exists(CALCULATION_PROGRAM_PATH):
        print(f"Error: Calculation program not found at '{CALCULATION_PROGRAM_PATH}'")
        logging.info(f"Error: Calculation program not found at '{CALCULATION_PROGRAM_PATH}'")
        return False

    logging.info(f"Running calculation for {os.path.basename(file_path)}...")
    try:
        # Pass the file path as a command-line argument.
        # subprocess.run(["python", CALCULATION_PROGRAM_PATH, file_path], check=True)
        subprocess.run([CUSTOM_PYTHON_PATH, CALCULATION_PROGRAM_PATH, file_path],
                       cwd=os.path.dirname(CALCULATION_PROGRAM_PATH))
        logging.info(" - Calculation finished successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logging.info(f"Error running calculation program: {e}")
        return False
    except FileNotFoundError:
        logging.info(f"Error: 'python' command not found. Make sure Python is installed and in your PATH.")
        return False


def main():
    """
    Main function to find new log files, upload them, and run calculations.
    This script is designed to be run once per trigger.
    """
    print("--- Starting On-Demand Log Processor ---")
    logging.info("--- Starting On-Demand Log Processor ---")
    
    if not SESSION_LOG_FOLDER_PATH or not os.path.isdir(SESSION_LOG_FOLDER_PATH):
        logging.info(f"Error: Log folder path '{SESSION_LOG_FOLDER_PATH}' is invalid. Please check your .env file.")
        return

    # 1. Get the set of files we've already processed.
    processed_files = get_processed_files()

    # 2. Find all log files in the target directory that match the pattern.
    log_file_pattern = os.path.join(SESSION_LOG_FOLDER_PATH, 'SESSION_LOG_*.json')
    all_log_files = {os.path.basename(f) for f in glob.glob(log_file_pattern)}

    # 3. Determine which files are new by finding the difference.
    new_files_to_process = sorted(list(all_log_files - processed_files))

    if not new_files_to_process:
        logging.info("No new log files found to process.")
    else:
        logging.info(f"Found {len(new_files_to_process)} new log file(s): {', '.join(new_files_to_process)}")
        success_count = 0
        for filename in new_files_to_process:
            full_path = os.path.join(SESSION_LOG_FOLDER_PATH, filename)
            logging.info(f"\n--- Processing: {filename} ---")

            run_calculation(full_path)
            # Step A: Upload the file.
            upload_to_cloud(full_path)
            log_processed_file(filename)
            logging.info(f" - Successfully processed and logged {filename}.")
            success_count += 1

    print("\n--- Script finished. ---")
    # logging.info("--- Script finished. ---")


if __name__ == "__main__":
    main()