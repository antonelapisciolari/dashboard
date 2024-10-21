import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import streamlit as st

logging.basicConfig(level=logging.DEBUG)

@st.cache_data  # Cache the result to avoid reloading each time
def get_google_sheet(sheet_id, sheet_number):
    """
    Connects to a Google Sheet using service account credentials and returns the sheet.
    """
    try:
        # Set up Google Sheets API credentials
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)

        # Open the Google Sheets file by its ID, not by name
        spreadsheet = client.open_by_key(sheet_id)

        # Get the first worksheet
        worksheet = spreadsheet.get_worksheet(sheet_number)

        # Get all values and display them with Streamlit
        data = worksheet.get_all_values()

        return data
    except FileNotFoundError as e:
        logging.error(f"Service account file not found: {e}")
        return None
    except gspread.exceptions.APIError as e:
        logging.error(f"Google Sheets API error: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
