from navigation import make_sidebar_admin, make_sidebar
import streamlit as st

if st.session_state.role == 'admin':
    make_sidebar_admin()
if st.session_state.role == 'superadmin':
    make_sidebar()


st.write(
    """
# 🔓 Admin Dashboard

Aca va el dashboard del admin

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

