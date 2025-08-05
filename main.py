import time
import re
from datetime import datetime
from controller.job_tracker_controller import run_job_tracker
from models.agent_brain import get_next_best_time
from googleapiclient.discovery import build
from auth_utils import get_credentials

def interactive_sheet_setup(creds):
    sheets_service = build('sheets', 'v4', credentials=creds)
    sheet_url = input("Paste your Google Sheet URL: ")
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheet_url)
    if not match:
        print("Invalid Sheet URL.")
        return None, None
    sheet_id = match.group(1)

    # Fetch tab (worksheet) names
    sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    tab_names = [s['properties']['title'] for s in sheets]
    print("\nAvailable tabs in your sheet:")
    for i, name in enumerate(tab_names, 1):
        print(f"{i}. {name}")

    tab_name = input("\nEnter the tab name to write to (choose from above or type a new one): ")
    return sheet_id, tab_name

def main():
    print("Welcome! Please log in to your Google account...")
    creds = get_credentials()  # Your normal login/auth function

    # Step 1: Dynamic Google Sheet & Tab Selection
    sheet_id, tab_name = interactive_sheet_setup(creds)
    if not sheet_id or not tab_name:
        print("Setup failed. Exiting.")
        return

    print("\nAgentic Job Tracker started! Press Ctrl+C to stop at any time.\n")
    try:
        while True:
            run_job_tracker(sheet_id=sheet_id, tab_name=tab_name, creds=creds)
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