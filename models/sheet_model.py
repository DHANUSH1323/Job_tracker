from googleapiclient.discovery import build

def append_to_sheet(sheet_id, info_dict, tab_name, creds):
    """
    Appends a row with company, position, status, and date to the specified Google Sheet tab.
    """
    service = build('sheets', 'v4', credentials=creds)
    sheet_range = f"{tab_name}"
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