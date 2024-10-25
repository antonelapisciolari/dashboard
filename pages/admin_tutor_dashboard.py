from navigation import make_sidebar_admin, make_sidebar
import streamlit as st
from page_utils import apply_page_config
apply_page_config(st)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Session expired. Redirecting to login page...")
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'admin':
        make_sidebar_admin()
    if st.session_state.role == 'superadmin':
        make_sidebar()

st.write(
    """
# Tutor Dashboard

Toda info relacionada con el tutor

"""
)


# import pandas as pd
# import streamlit as st
# from gsheets import get_google_sheet

# def show_data():
#     sheet_id = "1rEpToDOnYMWDnGX2V2t1ciAchEbkFbvittKcMgnbJvU"
#     sheet = get_google_sheet(sheet_id)  # Public data, no authentication required
       
#     if sheet:
#         # Get the data from the Google Sheet
#         data = pd.DataFrame(sheet.get_all_records())
#         st.write(data)
#     else:
#         st.error("Failed to access Google Sheets.")

