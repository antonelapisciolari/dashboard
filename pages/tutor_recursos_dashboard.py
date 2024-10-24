from navigation import make_sidebar_tutor, make_sidebar
import streamlit as st
from page_utils import apply_page_config
from streamlit_extras.stylable_container import stylable_container
from streamlit_calendar import calendar
from datetime import datetime
apply_page_config(st)
if st.session_state.role == 'tutor':
    make_sidebar_tutor()
if st.session_state.role == 'superadmin':
    make_sidebar()


preOnboardingLinks = ["https://example.com/link1", "https://example.com/link2"]
onboardingLinks = ["https://example.com/link3", "https://example.com/link4"]
seguimientoLinks = ["https://example.com/link5", "https://example.com/link6"]
cierreLinks = ["https://example.com/link7", "https://example.com/link8"]

# Create the main container for the layout
container = st.container()

# Create two columns inside the container, one taking 60% width and the other 40%
resources, nextStep = container.columns([3, 2])  # 60% for col1, 40% for col2
st.markdown(
    """
    <style>
    .resource-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
# In the 60% container, you can place some text or content
with resources:
    st.header("Datos Útiles")
    # Create two side-by-side containers inside col1

    # Add content to the first inner column
    with stylable_container(
        key="documentation_container",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                background-color: white;
            }
            """,
    ):
        st.subheader("Documentación")
        tabs = st.tabs(["Pre-Onboarding", "Onboarding", "Seguimiento", "Cierre"])

    # Pre-Onboarding Tab
    with tabs[0]:
        st.write("Links relevantes para Pre-Onboarding:")
        for link in preOnboardingLinks:
            st.write(f"[Pre-Onboarding Link]({link})")

    # Onboarding Tab
    with tabs[1]:
        st.write("Links relevantes para Onboarding:")
        for link in onboardingLinks:
            st.write(f"[Onboarding Link]({link})")

    # Seguimiento Tab
    with tabs[2]:
        st.write("Links relevantes para Seguimiento:")
        for link in seguimientoLinks:
            st.write(f"[Seguimiento Link]({link})")

    # Cierre Tab
    with tabs[3]:
        st.write("Links relevantes para Cierre:")
        for link in cierreLinks:
            st.write(f"[Cierre Link]({link})")

with st.container():
    st.subheader("Próximos pasos")

    # Set up events (date format: "YYYY-MM-DD")
    #consumir desde el sheet
    events = [
        {"start": "2024-10-25", "end":"2024-11-02", "title": "Inicio Mauricio Spalletti", "backgroundColor": "#FF6C6C",},
        {"start": "2024-10-30", "title": "Entrega Uniforme","backgroundColor": "#4f33ff",},
        {"start": "2024-11-01", "end":"2024-11-12", "title": "Inicio Gaston Quiroga", "backgroundColor": "#ff5733",},
    ]
    today = datetime.today().strftime('%Y-%m-%d')
    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "initialDate": today,
        "initialView": "dayGridMonth",
    }
    custom_css = """
        .fc-toolbar-title {
            font-size: 1.5rem;  /* Adjust the title size */
        }
        .fc {
            width: 70%;  /* Set calendar width to 70% of the container for desktop */
            margin: 0 auto;
        }
        .fc-view {
            min-height: 300px;  /* Set a minimum height */
        }
        
        /* Responsive adjustments for smaller screens */
        @media only screen and (max-width: 768px) {
            .fc {
                width: 100%;  /* Full width for mobile */
            }
            .fc-toolbar-title {
                font-size: 1.2rem;  /* Adjust the title size for mobile */
            }
        }
    """
    # Display the subheader with the current month and year
    st.subheader(f"Calendario")

    # Create a dictionary to hold events by date
    # Display the calendar
    selected_date = calendar(
        events,  # Pass the event dictionary
        options=calendar_options,
        custom_css=custom_css
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

