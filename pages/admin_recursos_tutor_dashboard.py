from navigation import make_sidebar_admin, make_sidebar
from page_utils import apply_page_config
import streamlit as st
from sheet_connection import get_google_sheet
import pandas as pd
apply_page_config(st)
if st.session_state.role == 'admin':
    make_sidebar_admin()
if st.session_state.role == 'superadmin':
    make_sidebar()


st.write(
    """
# Recursos Tutores Dashboard


"""
)

def show_data():
    # Use the actual Google Sheets ID here
    sheet_id = "1su5Lczuv6By0zr9HtvX82v9ExIotBGUBSsi0ha9lhpQ"
    df = get_google_sheet(sheet_id, 0)
    if not df.empty:
            # Display the table in Streamlit
        st.dataframe(df)  # For an interactive table
    else:
        st.write("No data found.")
# Call the function to show data
show_data()
