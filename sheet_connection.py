import logging
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
logging.basicConfig(level=logging.DEBUG)

@st.cache_data  # Cache the result to avoid reloading each time
def get_google_sheet(sheet_id, sheet_number):
    """
    Connects to a Google Sheet using service account credentials and returns the sheet.
    """
    try:
        url=f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit?usp=sharing"
        print(url)
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=url)  
        if df is not None and not df.empty:
             return df 
        else:
            st.error("No data found.")
            return None

    except FileNotFoundError as e:
        logging.error(f"Service account file not found: {e}")
        return None
    except gspread.exceptions.APIError as e:
        logging.error(f"Google Sheets API error: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
