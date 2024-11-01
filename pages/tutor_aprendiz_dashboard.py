from navigation import make_sidebar_tutor, make_sidebar
import streamlit as st
import plotly.express as px
from page_utils import apply_page_config
from data_utils import filter_dataframe, getColumns
from sheet_connection import get_google_sheet, get_sheets
import pandas as pd
import matplotlib.pyplot as plt
from variables import registroAprendices, azul, amarillo, aquamarine, connectionGeneral, connectionFeedbacks,orange, celeste,teal, gris
from datetime import datetime
from streamlit_carousel import carousel

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
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
topFilters = ['FECHA INICIO', 'CANDIDATOS', 'HOTEL', 'FPDUAL / FCT', 'FECHA FIN']

def getInfo():
    sheet_id = registroAprendices
    filters = {topFilters[3]: ['FP DUAL', 'FCT'], "CORREO TUTOR": [st.session_state.username]}
    df = get_google_sheet(connectionGeneral,sheet_id)
    dfiltered = filter_dataframe(df, filters)
    return dfiltered

df = getInfo()

df[topFilters[0]] = pd.to_datetime(df[topFilters[0]], format='%d/%m/%Y')
df[topFilters[4]] = pd.to_datetime(df[topFilters[4]], format='%d/%m/%Y')

def getCandidatosActivos():
     today = pd.to_datetime(datetime.today().date())
     active_candidates = df[(df[topFilters[0]] <= today) & (df[topFilters[4]] >= today)]
     return active_candidates[topFilters[1]].nunique(), active_candidates
active_count, active_candidates = getCandidatosActivos()

#filter containers
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with st.container():
        candidato = col1.selectbox("**APRENDIZ**", options=["Todos"] + df[topFilters[1]].unique().tolist())
    with st.container():
        hotel = col2.selectbox("**HOTEL**", options=["Todos"] + df[topFilters[2]].unique().tolist())
    with st.container():
        fecha_inicio = col3.date_input("**FECHA INICIO**", value=pd.to_datetime('01/01/2024'))
    with st.container():
        programa = col4.selectbox("**TIPO DE PROGRAMA**", options=["Todos"] + df[topFilters[3]].unique().tolist())

# Filter DataFrame based on selected values
filtered_df = df[
    ((df[topFilters[1]] == candidato) | (candidato == "Todos")) &
    ((df[topFilters[2]] == hotel) | (hotel == "Todos")) &
    (df[topFilters[0]] >= pd.to_datetime(fecha_inicio)) &  
    ((df[topFilters[3]] == programa) | (programa == "Todos"))
]

#pie chart container and aprendiz data
graficos = ['POSICIÓN/DPT','HOTEL','ESTUDIOS']
with st.container():
    st.write('**¿Cómo se distribuyen mis aprendices?**')
    custom_colors = [aquamarine, amarillo, azul, '#ffcc99'] 
    chartDepto, chartHotel, chartEstudio, statusAprendiz  = st.columns(4)
    with chartDepto:
        fig1, ax1 = plt.subplots()
        filtered_df[graficos[0]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, colors=custom_colors)
        ax1.set_ylabel('')
        ax1.set_title(graficos[0])
        st.pyplot(fig1)
    with chartHotel:
        fig2, ax2 = plt.subplots()
        filtered_df[graficos[1]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2, colors=custom_colors)
        ax2.set_ylabel('')
        ax2.set_title(graficos[1])
        st.pyplot(fig2)
    with chartEstudio:
        fig3, ax3 = plt.subplots()
        filtered_df[graficos[2]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax3, colors=custom_colors)
        ax3.set_ylabel('')
        ax3.set_title(graficos[2])
        st.pyplot(fig3)

    with statusAprendiz:
            st.markdown(
                f"""
                <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                    <span style="color: white; font-size: 16px;">Aprendices Activos</span><br>
                    <span style="color: white; font-size: 20px; font-weight: bold;">{active_count}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                    <span style="color: white; font-size: 16px;">% Bajas</span><br>
                    <span style="color: white; font-size: 20px; font-weight: bold;">25%</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                    <span style="color: white; font-size: 16px;">Tasa de Finalización</span><br>
                    <span style="color: white; font-size: 20px; font-weight: bold;">50%</span>
                </div>
                """,
                unsafe_allow_html=True
            )

#Container Feedback
def getFeebackDetails():
    feedbacks = get_sheets(connectionFeedbacks, ['formularioPulse1Semana','formAprendiz'])
    return feedbacks

#feedback details 

with st.container():
    st.write('**¿Cómo se están sintiendo en cada etapa del proceso?**')
    feedbackPulse, feedbackCambioArea, feedback, spacer, costeContainer = st.columns([0.8,0.8, 0.8, 0.2, 1])
    with feedbackPulse:
     with st.container():
        with st.container(key="feedback1"):
            st.markdown(
                f"""
                    <span style="color: gray; font-size: 16px;">Pulse</span><br>
                    <span style="color: black; font-size: 20px; font-weight: bold;">9.6</span>
                """,
                unsafe_allow_html=True
            )

    # Second container (inside col2)
    with feedbackCambioArea:
        with st.container(key="feedback2"):
            st.markdown(
                f"""
                    <span style="color: gray; font-size: 16px;">Cambio de Area</span><br>
                    <span style="color: black; font-size: 20px; font-weight: bold;">5.5</span>
                """,
                unsafe_allow_html=True
            )

    # Third container (inside col3)
    with feedback:
        with st.container(key="feedback3"):
            st.markdown(
                f"""
                    <span style="color: gray; font-size: 16px;">3er Feedback</span><br>
                    <span style="color: black; font-size: 20px; font-weight: bold;">4.2</span>
                """,
                unsafe_allow_html=True
            )

    # Fourth container (inside col4)
    with costeContainer:
        with st.container(key="costeContainer"):
            st.markdown(
                f"""
                    <span style="color: gray; font-size: 16px;">Coste Salario Mensual</span><br>
                    <span style="color: black; font-size: 20px; font-weight: bold;">€ 1000,00</span>
                """,
                unsafe_allow_html=True
            )
feedbacks= getFeebackDetails()
feedbackPulse= feedbacks[0][feedbacks[0]['Email'].isin(df['CORREO DE CONTACTO'])]

feedbackAprendiz= feedbacks[1][feedbacks[1]['Email'].isin(df['CORREO DE CONTACTO'])]
with st.expander("Detalle de Feedbacks"):
    with st.container():
        tabs = st.tabs(['Pulse', 'Cambio Area', '3rd Feedback'])
        with tabs[0]:
            if feedbackPulse is not None:
                st.dataframe(feedbackPulse)
        with tabs[1]:
            if feedbackAprendiz is not None:
                st.dataframe(feedbackAprendiz)

#donde estan mis aprendices
with st.container():
    st.write('**¿En dónde se encuentran hoy mis aprendices?**')
    graficoHotel, deptoAprendiz, tablaAprendicesHoy  = st.columns([1.2,0.8,1])
    with graficoHotel:
        # Define custom colors for each position
        color_map = {
            "ESTRUCTURA": azul,  # Blue for ESTRUCTURA
            "RECEPCIÓN": amarillo,  # Orange for CHEF
            "COCINA": aquamarine,  # Green for RECEPCIONISTA
            "B&R": orange,  # Green for RECEPCIONISTA
            "PISOS": gris,  # Green for RECEPCIONISTA
            "SSTT": celeste,  # Green for RECEPCIONISTA
            "ECONOMATO": teal,  # Green for RECEPCIONISTA
        }

        # Get unique hotels
        hotels = active_candidates["HOTEL"].unique()
        carousel_items = []
        for hotel in hotels:
            # Filter the data for each hotel
            hotel_df = active_candidates[active_candidates["HOTEL"] == hotel]

            # Group by position and count candidates
            position_counts = hotel_df.groupby("POSICIÓN/DPT")["CANDIDATOS"].count().reset_index()
            position_counts.columns = ["POSICIÓN/DPT", "CANTIDAD APRENDICES"]

            # Create a bar chart using Plotly
            fig = px.bar(
                position_counts,
                x="POSICIÓN/DPT",
                y="CANTIDAD APRENDICES",
                title=f"HOTEL {hotel}",
                color="POSICIÓN/DPT",
                color_discrete_map=color_map
            )
            fig.update_yaxes(dtick=1)

            # Save the figure as an image
            fig.write_image(f"{hotel}.png")

            # Add the slide to the carousel items
            carousel_items.append({
                "title": "",
                "text": "",
                "img": f"{hotel}.png"
            })

        # Display the carousel
        carousel(items=carousel_items)

    columns_to_extract = ['CANDIDATOS','FECHA INICIO','FECHA FIN','POSICIÓN/DPT']
    actualCandidatos = getColumns(active_candidates, columns_to_extract)
    actualCandidatos[columns_to_extract[1]] = actualCandidatos[columns_to_extract[1]].dt.strftime('%d/%m/%Y')
    actualCandidatos[columns_to_extract[2]] = actualCandidatos[columns_to_extract[2]].dt.strftime('%d/%m/%Y')
    with deptoAprendiz:
        fig1, ax1 = plt.subplots()
        actualCandidatos[graficos[0]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, colors=custom_colors)
        ax1.set_ylabel('')
        ax1.set_title(graficos[0])
        st.pyplot(fig1)
    with tablaAprendicesHoy:
        #show only name and dates
        st.dataframe(actualCandidatos.iloc[:,:-1])