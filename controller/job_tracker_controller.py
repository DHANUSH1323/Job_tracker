# controller/job_tracker_controller.py

from models.email_model import get_job_application_emails
from models.extractor import extract_job_info
from models.sheet_model import append_to_sheet
from models.agent_brain import should_run_now, log_run
from view.console_view import print_agent_decision

from view.console_view import (
    print_fetching_emails,
    print_no_emails_found,
    print_processing_email,
    print_extracted_info,
    print_written_to_sheet,
    print_success,
    print_error,
)

def run_job_tracker(sheet_id, tab_name, creds):
    should_run, reason = should_run_now()
    print_agent_decision(reason)
    if not should_run:
        return

    print_fetching_emails()
    emails = get_job_application_emails()
    if not emails:
        print_no_emails_found()
        log_run(0, 0, 0)
        return

    rejections = 0
    offers = 0
    for email in emails:
        print_processing_email(email['date_received'])
        info = extract_job_info(email['email_text'])
        info['date_received'] = email['date_received']
        print_extracted_info(info)
        
        # Print a visible red flag alert if detected by AI
        if info.get("is_red_flag", False):
            print("\n⚠️  AI RED FLAG DETECTED: {}".format(info.get("red_flag_reason", "")))

        append_to_sheet(sheet_id, info, tab_name, creds)
        print_written_to_sheet()
        if info["status"].lower() == "rejected":
            rejections += 1
        if info["status"].lower() == "offer":
            offers += 1
    print_success()
    log_run(len(emails), rejections, offers)

# if __name__ == "__main__":
#     run_job_tracker("your_sheet_id_here", "your_tab_name_here", None)