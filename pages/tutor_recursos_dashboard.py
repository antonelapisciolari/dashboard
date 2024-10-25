from navigation import make_sidebar_tutor, make_sidebar
import streamlit as st
from page_utils import apply_page_config
from streamlit_extras.stylable_container import stylable_container
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd
from sheet_connection import get_google_sheet
from data_utils import filter_dataframe, getColumns
from variables import amarillo, aquamarine, registroAprendices, recursosUtiles,documentacionTitle, tabPreOnboarding, tabCierre,tabOnboarding,tabSeguimiento, linkPreonboarding, linkPreonboarding1,linkPreonboarding2
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


preOnboardingLinks = [linkPreonboarding2, linkPreonboarding1, linkPreonboarding]
onboardingLinks = ["https://example.com/link3", "https://example.com/link4"]
seguimientoLinks = ["https://example.com/link5", "https://example.com/link6"]
cierreLinks = ["https://example.com/link7", "https://example.com/link8"]

#get events
columns_to_extract = ['CANDIDATOS','FECHA INICIO', 'FECHA FIN']
def getInfo():
    # Use the actual Google Sheets ID here
    sheet_id = registroAprendices
    df = get_google_sheet(sheet_id, 0)
    return df

def getEventsByTutor(df):
    print(st.session_state.username)
    filters = {"CORREO TUTOR": st.session_state.username}
    filtered_df = filter_dataframe(df, filters)
    selected_columns_df = getColumns(filtered_df, columns_to_extract)
    return selected_columns_df

def create_events(df):
    events = []
    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        # Parse dates
        start_date = pd.to_datetime(row[columns_to_extract[1]], dayfirst=True).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(row[columns_to_extract[2]], dayfirst=True).strftime('%Y-%m-%d')
        
        # Create start event
        start_event = {
            "start": start_date,
            "title": f"Inicio {row[columns_to_extract[0]]}",
            "backgroundColor": amarillo
        }
        
        # Create end event
        end_event = {
            "start": end_date,
            "title": f"Fin {row[columns_to_extract[0]]}",
            "backgroundColor": aquamarine
        }
        
        # Add both events to the list
        events.append(start_event)
        events.append(end_event)
    return events

candidatosByTutor = getInfo()
eventsCandidatos = getEventsByTutor(candidatosByTutor)
events = create_events(eventsCandidatos)

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
    st.subheader(recursosUtiles)
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
        st.subheader(documentacionTitle)
        tabs = st.tabs([tabPreOnboarding, tabOnboarding, tabSeguimiento, tabCierre])

    # Pre-Onboarding Tab
    with tabs[0]:
        st.write("Links relevantes para Pre-Onboarding:")
        st.write(f"[Checklist Aprendiz]({preOnboardingLinks[0]})")
        st.write(f"[Datos Aprendiz]({preOnboardingLinks[0]})")
        st.write(f"[Datos Importantes]({preOnboardingLinks[0]})")
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
with nextStep:
    st.subheader("Información Importante")
    st.image("./images/rolTutor.png",  use_column_width=True)
    st.image("./images/rolAprendiz.png", use_column_width=True)
with st.container():
    st.subheader("Próximos pasos")

    # Set up events (date format: "YYYY-MM-DD")
    #consumir desde el sheet
    events = events
    today = datetime.today().strftime('%Y-%m-%d')
    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "initialDate": today,
        "initialView": "dayGridMonth",
        "locale":"ES"
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


