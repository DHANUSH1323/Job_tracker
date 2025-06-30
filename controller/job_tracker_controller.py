# controller/job_tracker_controller.py

from models.email_model import get_job_application_emails
from models.extractor import extract_job_info
from models.sheet_model import append_to_sheet
from config import SHEET_ID
from view.console_view import (
    print_fetching_emails,
    print_no_emails_found,
    print_processing_email,
    print_extracted_info,
    print_written_to_sheet,
    print_success,
    print_error,
)

def run_job_tracker(sheet_name="sheet31"):
    try:
        print_fetching_emails()
        emails = get_job_application_emails()

        if not emails:
            print_no_emails_found()
            return

        for email in emails:
            print_processing_email(email['date_received'])
            info = extract_job_info(email['email_text'])
            info['date_received'] = email['date_received']
            print_extracted_info(info)
            append_to_sheet(SHEET_ID, info, sheet_name=sheet_name)
            print_written_to_sheet()
            print_success()
    except Exception as e:
        print_error(str(e))

if __name__ == "__main__":
    run_job_tracker()