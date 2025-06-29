# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
# from config import SHEET_ID

# def get_sheets_service():
#     # Reuse the token from Gmail authentication, or set up as needed
#     creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/spreadsheets'])
#     service = build('sheets', 'v4', credentials=creds)
#     return service

# def append_to_sheet(sheet_id, info_dict, sheet_name="Job_application"):
#     """
#     Appends a row with company, position, status, and date to the specified Google Sheet tab.
#     """
#     service = get_sheets_service()
#     sheet_range = f"{sheet_name}!A1"
#     values = [[
#         info_dict.get("company", ""),
#         info_dict.get("position", ""),
#         info_dict.get("status", ""),
#         info_dict.get("date_received", "")
#     ]]
#     body = {'values': values}
#     service.spreadsheets().values().append(
#         spreadsheetId=sheet_id,
#         range=sheet_range,
#         valueInputOption='RAW',
#         body=body
#     ).execute()











from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from config import SHEET_ID

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]
CREDENTIALS_FILE = 'credentials.json'

def get_sheets_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('sheets', 'v4', credentials=creds)
    return service

def append_to_sheet(sheet_id, info_dict, sheet_name="Job_application"):
    """
    Appends a row with company, position, status, and date to the specified Google Sheet tab.
    """
    service = get_sheets_service()
    sheet_range = f"{sheet_name}"  # Best practice: just the tab name, not !A1
    values = [[
        info_dict.get("company", ""),
        info_dict.get("position", ""),
        info_dict.get("status", ""),
        info_dict.get("date_received", "")
    ]]
    body = {'values': values}
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=sheet_range,
        valueInputOption='RAW',
        body=body
    ).execute()