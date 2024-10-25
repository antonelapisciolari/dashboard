from navigation import make_sidebar_tutor, make_sidebar
import streamlit as st
from page_utils import apply_page_config
from sheet_connection import get_google_sheet
from variables import registroAprendices
apply_page_config(st)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Session expired. Redirecting to login page...")
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'tutor':
        make_sidebar_tutor()
    if st.session_state.role == 'superadmin':
        make_sidebar()
st.write(
    """
# Aprendiz Dashboard

Dashboard de aprendiz

"""
)



def getInfo():
    # Use the actual Google Sheets ID here
    sheet_id = registroAprendices
    df = get_google_sheet(sheet_id, 0)
    st.dataframe(df)  # For an interactive table
# Call the function to show data
getInfo()
