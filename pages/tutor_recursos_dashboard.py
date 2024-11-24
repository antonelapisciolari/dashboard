from navigation import make_sidebar_tutor
import streamlit as st
from page_utils import apply_page_config
from streamlit_extras.stylable_container import stylable_container
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd
from sheet_connection import get_google_sheet
from data_utils import filter_dataframe, getColumns,create_events
from variables import connectionGeneral
import base64
from variables import amarillo, aquamarine, registroAprendices, recursosUtiles,documentacionTitle, tabPreOnboarding, tabCierre,tabOnboarding,tabSeguimiento, preOnboardingLinks, onboardingLinks,seguimientoLinks,cierreLinks,tabFeedback,formsLinks
apply_page_config(st)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Sesion expirada. Redirigiendo a login...")
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'tutor':
        make_sidebar_tutor()

#leer el style.css 
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#get events
columns_to_extract = ['CANDIDATOS','FECHA INICIO real', 'FECHA FIN real','Envío 1er Feedback','Envío 2do Feedback','Envío 3er Feedback']
columnaCorreoTutor= "CORREO TUTOR"
def getInfo():
    # Use the actual Google Sheets ID here
    sheet_id = registroAprendices
    df = get_google_sheet(connectionGeneral,sheet_id)
    filters = {columnaCorreoTutor: [st.session_state.username]}
    filtered_df = filter_dataframe(df, filters)
    filtered_df =filtered_df.drop_duplicates(subset=[columns_to_extract[0]])
    return filtered_df
    
def getEventsByTutor(df):
    selected_columns_df = getColumns(df, columns_to_extract)
    return selected_columns_df


candidatosByTutor = getInfo()
eventsCandidatos = getEventsByTutor(candidatosByTutor)
events = create_events(eventsCandidatos, columns_to_extract)


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
        tabs = st.tabs([tabPreOnboarding, tabOnboarding, tabSeguimiento, tabCierre,tabFeedback])

    # Pre-Onboarding Tab
    with tabs[0]:
        st.write("Links relevantes para preparación:")
        st.write(f"[{preOnboardingLinks[0]}]({preOnboardingLinks[1]})")
    # Onboarding Tab
    with tabs[1]:
        st.write("Links relevantes para primeros días:")
        st.write(f"[{onboardingLinks[0]}]({onboardingLinks[1]})")

    # Seguimiento Tab
    with tabs[2]:
        st.write("Links relevantes para Seguimiento:")
        st.write(f"[{seguimientoLinks[0]}]({seguimientoLinks[1]})")

    # Cierre Tab
    with tabs[3]:
        st.write("Links relevantes para Cierre:")
        st.write(f"[{cierreLinks[0]}]({cierreLinks[1]})")
            # Cierre Tab
    with tabs[4]:
        tutorForms, aprendizForms = st.columns(2)
        with aprendizForms:
            st.write("**Aprendiz:**")
            st.write(f"[{formsLinks[0]}]({formsLinks[1]})")
            st.write(f"[{formsLinks[2]}]({formsLinks[3]})")
            st.write(f"[{formsLinks[4]}]({formsLinks[5]})")
            st.write(f"[{formsLinks[6]}]({formsLinks[7]})")
            st.write(f"[{formsLinks[8]}]({formsLinks[9]})")
            st.write(f"[{formsLinks[10]}]({formsLinks[11]})")
        with tutorForms:
            st.write("**Tutor:**")
            st.write(f"[{formsLinks[12]}]({formsLinks[13]})")
            st.write(f"[{formsLinks[14]}]({formsLinks[15]})")
with nextStep:
    st.subheader("Información Importante")
    rolAprendiz = open("./images/carusel_tutor.gif", "rb")
    contents = rolAprendiz.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    rolAprendiz.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="rol aprendiz" style="padding-bottom: 10px">',
        unsafe_allow_html=True,
)
with st.container():
    st.subheader("Próximos pasos")
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
        "locale":"ES",
        "selectable": True,
    }
    custom_css = """
        .fc-toolbar-title {
            font-size: 1rem;  /* Adjust the title size */
        }
        .fc {
            width: 60%;  /* Set calendar width to 70% of the container for desktop */
            margin: 0 auto;
        }
        .fc-view {
            min-height: 200px;  /* Set a minimum height */
        }
        
        /* Responsive adjustments for smaller screens */
        @media only screen andter (max-width: 768px) {
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
    details_placeholder = st.empty()
    # Create a dictionary to hold events by date
    # Display the calendar
    selected_date = calendar(
        events,  # Pass the event dictionary
        options=calendar_options,
        custom_css=custom_css,
        callbacks = ["eventClick"]
    )
    
    if selected_date:
    # Find the event details
        details_placeholder.markdown(f"**Evento:** {selected_date['eventClick']['event']['title']}\n**Dia:** {selected_date['eventClick']['event']['start']}")


