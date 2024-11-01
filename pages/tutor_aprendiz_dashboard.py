from navigation import make_sidebar_tutor
import streamlit as st
import plotly.express as px
from page_utils import apply_page_config
from data_utils import filter_dataframe, getColumns,generate_color_map
from sheet_connection import get_google_sheet, get_sheets
import pandas as pd
import matplotlib.pyplot as plt
from variables import registroAprendices, azul, amarillo, aquamarine, connectionGeneral, connectionFeedbacks,connectionUsuarios, rotationSheet,orange, errorRedirection,teal, gris, formularioPulse1Semana, formAprendiz,noDatosDisponibles
from datetime import datetime, timedelta
from streamlit_carousel import carousel

#tab icono y titulo
apply_page_config(st)
#verificar si el usuario esta logueado sino redigirlo a la login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning(errorRedirection)
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'tutor':
        make_sidebar_tutor()

#leer el style.css 
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#filtros de arriba
columnaCandidatos='CANDIDATOS'
columnaFechaInicio='FECHA INICIO'
columnaFechaFin='FECHA FIN'
columnaHotel='HOTEL'
columnaFPDualFCT='FPDUAL / FCT'
columnaPosicion='POSICIÓN/DPT'
columnaEstudios='ESTUDIOS'

filtrosTutor = ["CORREO TUTOR", "MAIL TUTOR"]

#feedback
columnaEmail='Email'
columnaCorreoCandidato='CORREO DE CONTACTO'
topFilters = [columnaFechaInicio,columnaCandidatos,columnaHotel,columnaFPDualFCT, columnaFechaFin]

#rotacion
columnaMesesActivos="Meses Activos"
columnaDeptoDestino="Departamento de Destino"
columnaHotelDestino="Hotel destino"
#trae todos los datos filtrados por Tutor 
def getInfo():
    sheet_id = registroAprendices
    filters = {filtrosTutor[0]: [st.session_state.username]}
    df = get_google_sheet(connectionGeneral,sheet_id)
    dfiltered = filter_dataframe(df, filters)
    return dfiltered

df = getInfo()

#parseando las fechas
df[topFilters[0]] = pd.to_datetime(df[topFilters[0]], format='%d/%m/%Y')
df[topFilters[4]] = pd.to_datetime(df[topFilters[4]], format='%d/%m/%Y')

#filtrar candidatos activos
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
        hotel = col2.selectbox(f"**{topFilters[2]}**", options=["Todos"] + df[topFilters[2]].unique().tolist())
    with st.container():
        fecha_inicio = col3.date_input(f"**{topFilters[0]}**", value=pd.to_datetime('01/01/2024'))
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
graficos = [columnaPosicion,columnaHotel,columnaEstudios]
with st.container():
    st.write('**¿Cómo se distribuyen mis aprendices?**')
    custom_colors = [aquamarine, amarillo, azul, orange] 
    chartDepto, chartHotel, chartEstudio, statusAprendiz  = st.columns(4)
    fig_size = (4, 4)
    with chartDepto:
        fig1, ax1 = plt.subplots(figsize=fig_size)
        filtered_df[graficos[0]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, colors=custom_colors,startangle=90)
        ax1.set_ylabel('')
        ax1.set_title(graficos[0])
        ax1.set_aspect('equal')
        st.pyplot(fig1)
    with chartHotel:
        fig2, ax2 = plt.subplots(figsize=fig_size)
        filtered_df[graficos[1]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2, colors=custom_colors,startangle=90)
        ax2.set_ylabel('')
        ax2.set_title(graficos[1])
        ax2.set_aspect('equal')
        st.pyplot(fig2)
    with chartEstudio:
        fig3, ax3 = plt.subplots(figsize=fig_size)
        filtered_df[graficos[2]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax3, colors=custom_colors,startangle=90)
        ax3.set_ylabel('')
        ax3.set_title(graficos[2])
        ax3.set_aspect('equal')
        st.pyplot(fig3)

    with statusAprendiz:
            st.markdown(
                f"""
                <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                    <span style="color: white; font-size: 16px;">Aprendices Activos</span><br>
                    <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{active_count}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                    <span style="color: white; font-size: 16px;">% Bajas</span><br>
                    <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">25%</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                    <span style="color: white; font-size: 16px;">Tasa de Finalización</span><br>
                    <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">50%</span>
                </div>
                """,
                unsafe_allow_html=True
            )

#Container Feedback
def getFeebackDetails():
    feedbacks = get_sheets(connectionFeedbacks, [formularioPulse1Semana,formAprendiz])
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
feedbackPulse= feedbacks[0][feedbacks[0][columnaEmail].isin(df[columnaCorreoCandidato])]

feedbackAprendiz= feedbacks[1][feedbacks[1][columnaEmail].isin(df[columnaCorreoCandidato])]
with st.expander("Detalle de Feedbacks"):
    with st.container():
        tabs = st.tabs(['Pulse', 'Cambio Area', '3rd Feedback'])
        with tabs[0]:
            if feedbackPulse is not None and not feedbackPulse.empty:
                st.dataframe(feedbackPulse)
            else:
                st.write(noDatosDisponibles)

        with tabs[1]:
            if feedbackAprendiz is not None and not feedbackAprendiz.empty:
                st.dataframe(feedbackAprendiz)
            else:
                st.write(noDatosDisponibles)


with st.container():
    st.write('**Status de Respuestas**')
    respuestasRecibidas, respuestasPendientes, respuestas, = st.columns(3)
    with respuestasRecibidas:
     with st.container():
        with st.container(key="respuestas1"):
            st.markdown(
                f"""
                    <span style="color: white; font-size: 16px;">Respuestas Recibidas</span><br>
                    <span style="color:#FECA1D; font-size: 20px; font-weight: bold;">2</span>
                """,
                unsafe_allow_html=True
            )

    # Second container (inside col2)
    with respuestasPendientes:
        with st.container(key="respuestas2"):
            st.markdown(
                f"""
                    <span style="color: white; font-size: 16px;">Respuestas Pendientes</span><br>
                    <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">3</span>
                """,
                unsafe_allow_html=True
            )

    # Third container (inside col3)
    with respuestas:
        with st.container(key="respuestas3"):
            st.markdown(
                f"""
                    <span style="color: white; font-size: 16px;">% RESPUESTA</span><br>
                    <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">25%</span>
                """,
                unsafe_allow_html=True
            )

def getRotationInfo():
    rotacion = get_sheets(connectionUsuarios, [rotationSheet])
    filters = {filtrosTutor[1]: [st.session_state.username]}
    rotacionDelTutor = filter_dataframe(rotacion[0], filters)
    return rotacionDelTutor

#donde estan mis aprendices
with st.container():
    st.write('**¿En dónde se encuentran hoy mis aprendices?**')
    graficoHotel, deptoAprendiz, tablaAprendicesHoy  = st.columns([1.2,0.8,1])
    with graficoHotel:
        if active_candidates is not None and not active_candidates.empty:
            rotacion= getRotationInfo()
            rotacion[columnaMesesActivos] = pd.to_datetime(rotacion[columnaMesesActivos], format='%d/%m/%Y')
            # Filtrar datos para el próximo mes en adelante y agrupar por hotel, mes y departamento
            hoy = datetime.today()
            prox_mes = hoy.replace(day=1) + timedelta(days=31)
            prox_mes = prox_mes.replace(day=1)  # Primer día del próximo mes
            df = rotacion[rotacion[columnaMesesActivos] >= prox_mes]

            # Crear una columna para el mes (año-mes) y agrupar
            df["Mes"] = df[columnaMesesActivos].dt.to_period("M").astype(str)
            df[columnaDeptoDestino] = df[columnaDeptoDestino].str.strip().str.title()

            # Agrupar por hotel, mes y departamento destino
            df_grouped = df.groupby([columnaHotelDestino, "Mes", columnaDeptoDestino]).size().reset_index(name="Cantidad")
            # Obtener los próximos 12 meses como períodos
            meses_futuros = pd.date_range(prox_mes, periods=12, freq="MS").strftime("%Y-%m").tolist()
            color_map = generate_color_map(df, columnaDeptoDestino)
            # Crear gráficos individuales para cada hotel
            hoteles = df[columnaHotelDestino].unique()
            carousel_items = []
            for hotel in hoteles:
                # Filtrar los datos del hotel específico
                hotel_data = df_grouped[df_grouped[columnaHotelDestino] == hotel]
                
                # Crear gráfico de barras
                fig = px.bar(
                    hotel_data,
                    x="Mes",
                    y="Cantidad",
                    color=columnaDeptoDestino,
                    color_discrete_map=color_map,
                    category_orders={"Mes": meses_futuros},  # Ordenar los meses en el gráfico
                    title=f"Aprendices por Departamento en {hotel} (Próximos 12 meses)",
                    labels={"Cantidad": "Número de Candidatos", "Mes": "Mes", "Departamento de Destino": "Departamento"}
                )
                
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

        else:
            st.write(noDatosDisponibles)

    columns_to_extract = [columnaCandidatos,columnaFechaInicio,columnaFechaFin,columnaPosicion]
    actualCandidatos = getColumns(active_candidates, columns_to_extract)
    actualCandidatos[columns_to_extract[1]] = actualCandidatos[columns_to_extract[1]].dt.strftime('%d/%m/%Y')
    actualCandidatos[columns_to_extract[2]] = actualCandidatos[columns_to_extract[2]].dt.strftime('%d/%m/%Y')
    with deptoAprendiz:
        if actualCandidatos is not None and not actualCandidatos.empty:
            fig1, ax1 = plt.subplots()
            actualCandidatos[graficos[0]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, colors=custom_colors)
            ax1.set_ylabel('')
            ax1.set_title(graficos[0])
            st.pyplot(fig1)
        else:
            st.write(noDatosDisponibles)
    with tablaAprendicesHoy:
        st.write('Mis Aprendices:')
        if actualCandidatos is not None and not actualCandidatos.empty:
            st.dataframe(actualCandidatos,hide_index=True)
        else:
            st.write(noDatosDisponibles)

        