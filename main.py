import time
from datetime import datetime
from controller.job_tracker_controller import run_job_tracker
from models.agent_brain import get_next_best_time

def main():
    print("Welcome! Please log in to your Google account...")
    print("Agentic Job Tracker started! Press Ctrl+C to stop at any time.\n")
    try:
        while True:
            run_job_tracker()
            next_run = get_next_best_time()
            now = datetime.now()
            sleep_seconds = (next_run - now).total_seconds()
            if sleep_seconds > 0:
                print(f"AI scheduled next run for {next_run}. Sleeping for {int(sleep_seconds)} seconds...")
                time.sleep(sleep_seconds)
            else:
                print("AI suggests running again immediately!")
    except KeyboardInterrupt:
        print("\nAgent stopped by user (Ctrl+C).")

if __name__ == "__main__":
    main()