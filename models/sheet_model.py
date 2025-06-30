from googleapiclient.discovery import build
from auth_utils import get_credentials
from config import SHEET_ID

def get_sheets_service():
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    return service

def append_to_sheet(sheet_id, info_dict, sheet_name="sheet31"):
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