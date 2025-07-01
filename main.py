import time
from controller.job_tracker_controller import run_job_tracker

def main():
    print("Welcome! Please log in to your Google account...")
    # You may have an explicit login step here (first run of run_job_tracker will handle token)
    print("Agentic Job Tracker started! Press Ctrl+C to stop at any time.\n")
    try:
        while True:
            run_job_tracker()
            # Sleep a short interval; agent_brain decides if any action is needed
            time.sleep(5 * 60)  # Check every 5 minutes (or adjust as desired)
    except KeyboardInterrupt:
        print("\nAgent stopped by user (Ctrl+C).")

if __name__ == "__main__":
    main()