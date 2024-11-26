import os
import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'client.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID = '1t1_tscscOjolf5xrIZe15ElsPpzaZezUgut9g_fVpBE'
RANGE_NAME = 'Sheet1!A1:D10'  # Adjust the range as needed

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()
def query_data():

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values')
    return list(values)

query_data()