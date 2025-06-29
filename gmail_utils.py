# gmail_utils.py

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import email
import datetime

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]
CREDENTIALS_FILE = 'credentials.json'

def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def search_job_application_emails(service, max_results=10, query='application'):
    # You can customize the query. E.g.: 'subject:application' or label, etc.
    results = service.users().messages().list(userId='me', maxResults=max_results, q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_email_text(service, msg_id):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg.get('payload', {})
    parts = payload.get('parts', [])
    # Try to extract the body from multipart or singlepart emails
    data = None

    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                break
        if not data and parts:
            # Fallback to first part
            data = parts[0]['body'].get('data')
    else:
        data = payload.get('body', {}).get('data')

    if data:
        decoded_bytes = base64.urlsafe_b64decode(data)
        text = decoded_bytes.decode('utf-8', errors='ignore')
        return text
    return ""



def get_job_application_emails():
    service = authenticate_gmail()
    messages = search_job_application_emails(service)
    emails = []
    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        email_text = get_email_text(service, msg['id'])
        # Get internalDate and convert to readable format
        internal_date = msg_detail.get('internalDate')
        if internal_date:
            # Convert from ms to seconds, then to datetime
            dt = datetime.datetime.fromtimestamp(int(internal_date) / 1000)
            date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_str = 'Unknown'
        emails.append({'email_text': email_text, 'date_received': date_str})
    return emails

if __name__ == "__main__":
    emails = get_job_application_emails()
    for i, email in enumerate(emails, 1):
        print(f"\n----- Email #{i} -----")
        print(f"Received: {email['date_received']}")
        print(email['email_text'])