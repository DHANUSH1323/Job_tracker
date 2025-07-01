# view/console_view.py

def print_fetching_emails():
    print("Fetching unread job application emails...")

def print_no_emails_found():
    print("No unread job application emails found.")

def print_processing_email(date_received):
    print(f"\nProcessing email received at: {date_received}")

def print_extracted_info(info):
    print("Extracted Info:", info)

def print_written_to_sheet():
    print("Written to Google Sheet.")

def print_error(error_msg):
    print(f"Error: {error_msg}")

def print_success():
    print("Job application tracking completed successfully.")

def print_agent_decision(reason):
    print(f"Agent Decision: {reason}")