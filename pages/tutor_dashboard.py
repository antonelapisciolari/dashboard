import pandas as pd
import streamlit as st

def show_tutor_dashboardsss():
    st.title("Tutor Dashboard")
    st.write("Tutor view with access to aprendiz dashboard.")
    #show_data()

import pandas as pd
import streamlit as st
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

