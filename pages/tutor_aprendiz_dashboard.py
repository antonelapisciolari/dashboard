from navigation import make_sidebar_tutor
import streamlit as st
import plotly.express as px
from page_utils import apply_page_config
from data_utils import filter_dataframe, getColumns,generate_color_map,calcularPorcentajesStatus
from sheet_connection import get_google_sheet, get_sheets
from feedback_utils import getFeedbackPulse1Semana
import pandas as pd
import matplotlib.pyplot as plt
from variables import registroAprendices, azul, amarillo, aquamarine,worksheetPulse1Semana, connectionGeneral, connectionFeedbacks,connectionUsuarios, rotationSheet,orange, errorRedirection, formAprendiz,noDatosDisponibles
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
columnaFechaInicio='FECHA INICIO real'
columnaFechaFin='FECHA FIN real'
columnaHotel='HOTEL'
columnaFPDualFCT='FPDUAL / FCT'
columnaPosicion='POSICIÓN/DPT'
columnaEstudios='ESTUDIOS'

filtrosTutor = ["CORREO TUTOR", "MAIL TUTOR"]

#feedback
columnaEmail='Email'
columnaCorreoCandidato='CORREO DE CONTACTO'
topFilters = [columnaFechaInicio,columnaCandidatos,columnaHotel,columnaFPDualFCT, columnaFechaFin]
columnStatus = 'STATUS'

#trae todos los datos filtrados por Tutor 
def getInfo():
    sheet_id = registroAprendices
    filters = {filtrosTutor[0]: [st.session_state.username]}
    df = get_google_sheet(connectionGeneral,sheet_id)
    dfiltered = filter_dataframe(df, filters)
    dfiltered =dfiltered.drop_duplicates(subset=[columnaCandidatos])
    return dfiltered

df = getInfo()

#parseando las fechas
df[topFilters[0]] = pd.to_datetime(df[topFilters[0]], format='%d/%m/%Y')
df[topFilters[4]] = pd.to_datetime(df[topFilters[4]], format='%d/%m/%Y')
active_candidates = df[df[columnStatus].str.upper() == 'ACTIVO']



#filter containers
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with st.container():
        candidato = col1.selectbox("**APRENDIZ**", options=["Todos"] + df[topFilters[1]].unique().tolist())
    with st.container():
        hotel = col2.selectbox(f"**{topFilters[2]}**", options=["Todos"] + df[topFilters[2]].unique().tolist())
    with st.container():
        fecha_inicio = col3.date_input(f"**FECHA INICIO**", value=pd.to_datetime('01/01/2024'))
    with st.container():
        programa = col4.selectbox("**TIPO DE PROGRAMA**", options=["Todos"] + df[topFilters[3]].unique().tolist())

# Filter DataFrame based on selected values
filtered_df = df[
    ((df[topFilters[1]] == candidato) | (candidato == "Todos")) &
    ((df[topFilters[2]] == hotel) | (hotel == "Todos")) &
    (df[topFilters[0]] >= pd.to_datetime(fecha_inicio)) &  
    ((df[topFilters[3]] == programa) | (programa == "Todos"))
]
finalizado, baja,active_count, bajaCount, finalizadoCount = calcularPorcentajesStatus(filtered_df)
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
                <div style="display: flex; justify-content: space-between; gap: 10px; margin-bottom: 10px;">
                    <!-- First div -->
                    <div style="background-color: {azul}; padding: 10px; border-radius: 5px; text-align: center; flex: 1;">
                        <span style="color: white; font-size: 16px;">Bajas</span><br>
                        <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{baja}%</span>
                    </div>
                    <div style="background-color: {azul}; padding: 10px; border-radius: 5px; text-align: center; flex: 1;">
                        <span style="color: white; font-size: 14px;">Cantidad</span><br>
                        <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{bajaCount}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; gap: 10px; margin-bottom: 10px;">
                    <!-- First div -->
                    <div style="background-color: {azul}; padding: 10px; border-radius: 5px; text-align: center; flex: 1;">
                        <span style="color: white; font-size: 16px;">Finalizados</span><br>
                        <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{finalizado}%</span>
                    </div>
                    <div style="background-color: {azul}; padding: 10px; border-radius: 5px; text-align: center; flex: 1;">
                        <span style="color: white; font-size: 14px;">Cantidad</span><br>
                        <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{finalizadoCount}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

#Container Feedback
def getFeebackDetails():
    feedbacks = get_sheets(connectionFeedbacks, [worksheetPulse1Semana,formAprendiz])
    return feedbacks

feedbacks= getFeebackDetails()
feedbackPulseDf = feedbacks[0][feedbacks[0][columnaEmail].apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
    df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else x)
)]
feedbackPulseDf = feedbackPulseDf.drop_duplicates(subset=[columnaEmail])
feedbackAprendiz= feedbacks[1][feedbacks[1][columnaEmail].apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
    df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else x)
)]

pulse1SemanaPromedio = getFeedbackPulse1Semana(feedbackPulseDf)
#feedback details 
with st.container():
    st.write('**¿Cómo se están sintiendo en cada etapa del proceso?**')
    feedbackPulse, feedbackCambioArea, feedback = st.columns(3)
    with feedbackPulse:
     with st.container():
        with st.container(key="feedback1"):
            st.markdown(
                f"""
                    <span style="color: gray; font-size: 16px;">Pulse</span><br>
                    <span style="color: black; font-size: 20px; font-weight: bold;">{pulse1SemanaPromedio}</span>
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


feedbackAprendiz = feedbackAprendiz.drop_duplicates(subset=[columnaEmail])

feedback_types = ['Pulse 1º Semana', 'Cambio Area', '1º Mes'] 
with st.expander("Detalle de Feedbacks"):
    with st.container():
        tabs = st.tabs(feedback_types)
        with tabs[0]:
            if feedbackPulseDf is not None and not feedbackPulseDf.empty:
                st.dataframe(feedbackPulseDf)
            else:
                st.write(noDatosDisponibles)

        with tabs[1]:
            if feedbackAprendiz is not None and not feedbackAprendiz.empty:
                st.dataframe(feedbackAprendiz)
            else:
                st.write(noDatosDisponibles)
response_data = {
    'Respuestas Recibidas': [2, 5, 3],  # Replace with actual values
    'Respuestas Pendientes': [3, 2, 4],  # Replace with actual values
    '% RESPUESTA': ['25%', '71%', '43%']  # Replace with actual values
}

with st.container():
    st.write('**Status de Respuestas**')
    tabs = st.tabs(feedback_types)
    for i, feedback in enumerate(feedback_types):
        with tabs[i]:
            respuestasRecibidas, respuestasPendientes, respuestas, = st.columns(3)
            with respuestasRecibidas:
                with st.container():
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="custom-container">
                                <span style="color: white; font-size: 16px;">Respuestas Recibidas</span><br>
                                <span style="color:#FECA1D; font-size: 20px; font-weight: bold;">{response_data['Respuestas Recibidas'][i]}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                # Second container (inside col2)
                with respuestasPendientes:
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="custom-container">
                                <span style="color: white; font-size: 16px;">Respuestas Pendientes</span><br>
                                <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{response_data['Respuestas Pendientes'][i]}</span>
                                </div>
                            """,
                            unsafe_allow_html=True
                        )

                # Third container (inside col3)
                with respuestas:
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="custom-container">
                                <span style="color: white; font-size: 16px;">% RESPUESTA</span><br>
                                <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{response_data['% RESPUESTA'][i]}</span>
                                </div>
                            """,
                            unsafe_allow_html=True
                    )

#rotacion
columnaMesesActivos="Meses Activos"
columnaDeptoDestino="Departamento de Destino"
columnaDeptoOrigen="Departamento de Origen"
columnaHotelDestino="Hotel destino"
columnaNombre="Nombre"
columnaFechaInicioRotacion="Fecha de Inicio"
columnaEmailAprendiz="MAIL APRENDIZ"

def getRotationInfo():
    rotacion = get_sheets(connectionUsuarios, [rotationSheet])
    filters = {filtrosTutor[1]: [st.session_state.username]}
    rotacionDelTutor = filter_dataframe(rotacion[0], filters)
    return rotacionDelTutor

#donde estan mis aprendices
with st.container():
    st.write('**¿En dónde se encuentran hoy mis aprendices?**')
    graficoHotel, tablaAprendicesHoy  = st.columns([1.6,1.4])
    with graficoHotel:
        if active_candidates is not None and not active_candidates.empty:
            rotacionUnfiltered= getRotationInfo()
            rotacion = rotacionUnfiltered[rotacionUnfiltered[columnaEmailAprendiz].isin(active_candidates[columnaCorreoCandidato])]
            
            rotacion[columnaMesesActivos] = pd.to_datetime(rotacion[columnaMesesActivos], format='%d/%m/%Y')
            # Filtrar datos para el próximo mes en adelante y agrupar por hotel, mes y departamento
            hoy = datetime.today()
            mes_actual = hoy.replace(day=1)
            prox_mes = hoy.replace(day=1) + timedelta(days=31)
            prox_mes = prox_mes.replace(day=1)  # Primer día del próximo mes
            df = rotacion[rotacion[columnaMesesActivos] >= mes_actual]
            # Crear una columna para el mes (año-mes) y agrupar
            df["Mes"] = df[columnaMesesActivos].dt.to_period("M").astype(str)
            df[columnaDeptoDestino] = df[columnaDeptoDestino].str.strip().str.title()
            df = df.drop_duplicates(subset=[columnaNombre, columnaDeptoOrigen, columnaDeptoDestino, columnaMesesActivos])
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
                    labels={"Cantidad": "Número de Candidatos", "Mes": "Mes", "Departamento de Destino": "Departamento"},
                    text="Cantidad"
                )
                
                fig.update_traces(textposition="outside")
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

    hoy = datetime.today()
    mes_actual = hoy.replace(day=1)
    prox_mes = hoy.replace(day=1) + timedelta(days=31)
    prox_mes = prox_mes.replace(day=1)  # Primer día del próximo mes
    rotacion = rotacion[rotacion[columnaMesesActivos] >= mes_actual]
    result_df = rotacion.groupby(
    ["Nombre", "Departamento de Destino", "Hotel destino", "Fecha de Inicio"]
        ).agg(
            {
                "Meses Activos": lambda x: ", ".join(sorted(x.astype(str).unique()))
            }
        ).reset_index()
    result_df= result_df.sort_values(by=columnaFechaInicioRotacion,ascending=[False])
    with tablaAprendicesHoy:
        st.write('Mis Aprendices:')
        if result_df is not None and not result_df.empty:
            st.dataframe(result_df, hide_index="true")
        else:
            st.write(noDatosDisponibles)

        