import pandas as pd
import streamlit as st
import sidebar as sd
def show_admin_dashboard():
    st.title("Admin Dashboard")
    st.write("Admin-specific view.")
   # show_data()

if 'role' in st.session_state and st.session_state['role'] == 'admin':
        sd.showAdmins()
if 'role' in st.session_state and st.session_state['role'] == 'superadmin':
        sd.showSuperAdmins()

from google_sheets import get_google_sheet

def show_data():
    sheet_id = "1rEpToDOnYMWDnGX2V2t1ciAchEbkFbvittKcMgnbJvU"
    sheet = get_google_sheet(sheet_id)  # Public data, no authentication required
       
    if sheet:
        # Get the data from the Google Sheet
        data = pd.DataFrame(sheet.get_all_records())
        st.write(data)
    else:
        st.error("Failed to access Google Sheets.")

