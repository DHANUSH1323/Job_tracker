from gmail_utils import get_job_application_emails
from sheets_utils import append_to_sheet
from extractor import extract_job_info
from config import SHEET_ID

def main():
    emails = get_job_application_emails()
    # for email_text in emails:
    #     info = extract_job_info(email_text)
    #     print("Extracted:", info)
    #     append_to_sheet(SHEET_ID, info)
    for email in emails:
        info = extract_job_info(email['email_text'])
        print("Company:", info['company'])
        print("Position:", info['position'])
        print("Status:", info['status'])
        print("Received:", email['date_received'])
        print("---")
        append_to_sheet(SHEET_ID, info, sheet_name="Job_application")

if __name__ == "__main__":
    main()