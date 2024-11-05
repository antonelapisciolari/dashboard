from navigation import make_sidebar_admin
import streamlit as st
from page_utils import apply_page_config
from streamlit_extras.stylable_container import stylable_container
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd
from sheet_connection import get_google_sheet
from data_utils import filter_dataframe, getColumns
from variables import connectionGeneral
import base64
from variables import amarillo, aquamarine, registroAprendices, recursosUtiles,documentacionTitle, tabPreOnboarding, tabCierre,tabOnboarding,tabSeguimiento, preOnboardingLinks, onboardingLinks,seguimientoLinks,cierreLinks
apply_page_config(st)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Sesion expirada. Redirigiendo a login...")
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'admin':
        make_sidebar_admin()


#get events
columns_to_extract = ['CANDIDATOS','FECHA INICIO', 'FECHA FIN']
def getInfo():
    # Use the actual Google Sheets ID here
    sheet_id = registroAprendices
    df = get_google_sheet(connectionGeneral,sheet_id)
    return df

def getEventsByTutor(df):
    filters = {"CORREO TUTOR": [st.session_state.username]}
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
        st.write(f"[{preOnboardingLinks[0]}]({preOnboardingLinks[1]})")
    # Onboarding Tab
    with tabs[1]:
        st.write("Links relevantes para Onboarding:")
        st.write(f"[{onboardingLinks[0]}]({onboardingLinks[1]})")

    # Seguimiento Tab
    with tabs[2]:
        st.write("Links relevantes para Seguimiento:")
        st.write(f"[{seguimientoLinks[0]}]({seguimientoLinks[1]})")

    # Cierre Tab
    with tabs[3]:
        st.write("Links relevantes para Cierre:")
        st.write(f"[{cierreLinks[0]}]({cierreLinks[1]})")
with nextStep:
    st.subheader("Información Importante")
    rolAprendiz = open("./images/rol-aprendiz.gif", "rb")
    contents = rolAprendiz.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    rolAprendiz.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="rol aprendiz" style="padding-bottom: 10px">',
        unsafe_allow_html=True,
)
    rolTutor = open("./images/rol-tutor.gif", "rb")
    contents = rolTutor.read()
    data_url_tutor = base64.b64encode(contents).decode("utf-8")
    rolTutor.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url_tutor}" alt="rol tutor">',
        unsafe_allow_html=True,
)
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


