# gmail_utils.py

from googleapiclient.discovery import build
from auth_utils import get_credentials
import base64
import email
import datetime
import csv
import os

EMAIL_CSV = "email_times.csv"

def log_email_received(date_received):
    file_exists = os.path.isfile(EMAIL_CSV)
    with open(EMAIL_CSV, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["received_datetime"])
        writer.writerow([date_received])

def search_job_application_emails(service, max_results=3, query='is:unread application'):
    results = service.users().messages().list(userId='me', maxResults=max_results, q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_email_text(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg.get('payload', {})
    parts = payload.get('parts', [])
    data = None

    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                break
        if not data and parts:
            data = parts[0]['body'].get('data')
    else:
        data = payload.get('body', {}).get('data')

    if data:
        decoded_bytes = base64.urlsafe_b64decode(data)
        text = decoded_bytes.decode('utf-8', errors='ignore')
        return text
    return ""

def get_job_application_emails():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    messages = search_job_application_emails(service)
    emails = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        email_text = get_email_text(service, msg['id'])
        internal_date = msg_detail.get('internalDate')
        if internal_date:
            dt = datetime.datetime.fromtimestamp(int(internal_date) / 1000)
            date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_str = 'Unknown'
        emails.append({'email_text': email_text, 'date_received': date_str})
        if date_str != 'Unknown':
            log_email_received(date_str)
    return emails

















# # gmail_utils.py

# from googleapiclient.discovery import build
# from auth_utils import get_credentials
# import base64
# import email
# import datetime
# import csv
# import os

# EMAIL_CSV = "email_times.csv"

# def log_email_received(date_received):
#     file_exists = os.path.isfile(EMAIL_CSV)
#     with open(EMAIL_CSV, "a", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         if not file_exists:
#             writer.writerow(["received_datetime"])
#         writer.writerow([date_received])

# def search_job_application_emails(service, max_results=1, query='is:unread application'):
#     results = service.users().messages().list(userId='me', maxResults=max_results, q=query).execute()
#     messages = results.get('messages', [])
#     return messages

# def get_email_text(service, msg_id):
#     msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
#     payload = msg.get('payload', {})
#     parts = payload.get('parts', [])
#     # Try to extract the body from multipart or singlepart emails
#     data = None

#     if parts:
#         for part in parts:
#             if part['mimeType'] == 'text/plain':
#                 data = part['body'].get('data')
#                 break
#         if not data and parts:
#             # Fallback to first part
#             data = parts[0]['body'].get('data')
#     else:
#         data = payload.get('body', {}).get('data')

#     if data:
#         decoded_bytes = base64.urlsafe_b64decode(data)
#         text = decoded_bytes.decode('utf-8', errors='ignore')
#         return text
#     return ""



# def get_job_application_emails():
#     creds = get_credentials()
#     service = build('gmail', 'v1', credentials=creds)
#     messages = search_job_application_emails(service)
#     emails = []
#     for msg in messages:
#         msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
#         email_text = get_email_text(service, msg['id'])
#         # Get internalDate and convert to readable format
#         internal_date = msg_detail.get('internalDate')
#         if internal_date:
#             # Convert from ms to seconds, then to datetime
#             dt = datetime.datetime.fromtimestamp(int(internal_date) / 1000)
#             date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
#         else:
#             date_str = 'Unknown'
#         emails.append({'email_text': email_text, 'date_received': date_str})
#     return emails