import gspread
from google.oauth2.service_account import Credentials
import logging
import streamlit as st
logging.basicConfig(level=logging.DEBUG)

@st.cache_data  # Cache the result to avoid reloading each time
def get_google_sheet(sheet_id):
    """
    Connects to a Google Sheet using service account credentials and returns the sheet.
    """
    try:
        # Define the scope for accessing Google Sheets and Google Drive
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        # Load the service account credentials file (update the path to your service account JSON)
        credentials = Credentials.from_service_account_file(
            'fpdual-app-e81a53220858.json', scopes=scope
        )

        # Authorize the client using the credentials
        gc = gspread.authorize(credentials)

        # Open the sheet using the sheet ID
        sheet = gc.open_by_key(sheet_id).sheet1
        return sheet
    except FileNotFoundError as e:
        logging.error(f"Service account file not found: {e}")
        return None
    except gspread.exceptions.APIError as e:
        logging.error(f"Google Sheets API error: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
