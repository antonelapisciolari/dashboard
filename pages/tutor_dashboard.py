from navigation import make_sidebar_tutor, make_sidebar
import streamlit as st
from pagesUtils import apply_page_config
apply_page_config(st)
if st.session_state.role == 'tutor':
    make_sidebar_tutor()
if st.session_state.role == 'superadmin':
    make_sidebar()


st.write(
    """
# Tutor Dashboard

Todo lo del dashboard tutor

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

