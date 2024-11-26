from navigation import make_sidebar_admin
import streamlit as st
import plotly.express as px
from page_utils import apply_page_config
from data_utils import calcularPorcentajesStatus,create_donut_chart,generate_color_map,feedbackColor,getColumns
from sheet_connection import get_google_sheet, get_sheets
import pandas as pd
import matplotlib.pyplot as plt
from variables import registroAprendices, azul, amarillo, aquamarine, connectionGeneral, worksheetPulse1Semana,connectionFeedbacks,connectionUsuarios, rotationSheet,orange, errorRedirection,noDatosDisponibles,worksheetCambioArea,noDatosDisponibles, worksheetFormulario1Mes, worksheetFormulario4Mes, worksheetFormularioAprendizCierre1Ciclo, worksheetFormularioAprendizCierre2Ciclo,feedback_types,colorPulse, colorCambioArea, colorPrimerMes, colorAprendizCierrePrimerCiclo,colorAprendizCierreSegundoCiclo,colorCuartoMes,pulse1SemanaPromedio, primerMesPromedio, cuartoMesPromedio, cambioAreaPromedio, aprendizCierrePrimerCicloPromedio, aprendizCierreSegundoCicloPromedio
from datetime import datetime, timedelta
from streamlit_carousel import carousel
from feedback_utils import getFeedbackPulse1Semana,getFeedbackPromedioCambioArea,getFeedbackPromedioPrimerMes,getFeedbackPromedioCuartoMes,getFeedbackPromedioAprendizCierrePrimerCiclo,getFeedbackPromedioAprendizCierreSegundoCiclo,calcularEstadoRespuestas

#tab icono y titulo
apply_page_config(st)
#verificar si el usuario esta logueado sino redigirlo a la login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning(errorRedirection)
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'admin':
        make_sidebar_admin()

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
columnaTutor='TUTOR'
columnaZona='ZONA'
columnStatus = 'STATUS'
filtrosTutor = ["CORREO TUTOR", "MAIL TUTOR"]

#feedback
columnaEmail='Email'
columnaCorreoCandidato='CORREO DE CONTACTO'
topFilters = [columnaFechaInicio,columnaCandidatos,columnaHotel,columnaFPDualFCT, columnaFechaFin,columnaTutor,columnStatus]
columnaEnvio1Feedback='Envío 1er Feedback'
#rotacion
columnaMesesActivos="Meses Activos"
columnaDeptoDestino="Departamento de Destino"
columnaDeptoOrigen="Departamento de Origen"
columnaHotelDestino="Hotel destino"
columnaNombre="Nombre"
columnaFechaInicioRotacion="Fecha de Inicio"
#trae todos los datos filtrados por Tutor 
def getInfo():
    sheet_id = registroAprendices
    df = get_google_sheet(connectionGeneral,sheet_id)
    return df

df = getInfo()

#parseando las fechas
df[topFilters[0]] = pd.to_datetime(df[topFilters[0]], format='%d/%m/%Y')
df[topFilters[4]] = pd.to_datetime(df[topFilters[4]], format='%d/%m/%Y')
df= df.drop_duplicates(subset=[columnaCorreoCandidato])
active_candidates = df[df[topFilters[6]].str.upper() == 'ACTIVO']
#filter containers
with st.container():
    col1, col2, col3, col4,col5, col6 = st.columns(6)
    with st.container():
        tutor_options =[value for value in df[topFilters[5]].unique() if pd.notna(value) and str(value).strip() != ""]
        tutor_options = sorted(tutor_options)
        tutor = col1.selectbox("**TUTOR**", options=["Todos"] + tutor_options)
    with st.container():
        candidato_options = sorted(df[topFilters[1]].unique().tolist())
        candidato = col2.selectbox("**APRENDIZ**", options=["Todos"] + candidato_options)
    with st.container():
        hotel_options = sorted(df[topFilters[2]].unique().tolist())
        hotel = col3.selectbox(f"**{topFilters[2]}**", options=["Todos"] + hotel_options)
    with st.container():
        fecha_inicio = col4.date_input(f"**FECHA INICIO**", value=pd.to_datetime('01/01/2024'))
    with st.container():
        programa_options = sorted(df[topFilters[3]].unique().tolist())
        programa = col5.selectbox("**TIPO DE PROGRAMA**", options=["Todos"] + programa_options)
    with st.container():
        status = col6.selectbox("**STATUS**", options=["Todos"] + df[topFilters[6]].unique().tolist())
# Filter DataFrame based on selected values
filtered_df = df[
    ((df[topFilters[5]] == tutor) | (tutor == "Todos")) &
    ((df[topFilters[1]] == candidato) | (candidato == "Todos")) &
    ((df[topFilters[2]] == hotel) | (hotel == "Todos")) &
    (df[topFilters[0]] >= pd.to_datetime(fecha_inicio)) &  
    ((df[topFilters[3]] == programa) | (programa == "Todos")) &  
    ((df[topFilters[6]] == status) | (status == "Todos"))
]
#pie chart container and aprendiz data
graficos = [columnaPosicion,columnaHotel,columnaEstudios,columnaZona]
finalizado, baja,active_count, bajaCount, finalizadoCount = calcularPorcentajesStatus(filtered_df)
with st.container():
    st.header('**¿Cómo se distribuyen los aprendices?**')

# Layout containers
containerActivos, containerBajas,containerBajasCantidad, containerFinalizados,containerFinalizadosCant = st.columns(5)

with containerActivos:
    st.markdown(
        f"<div style='text-align: center; color: {azul}; font-size: 16px;font-weight: bold;'>Aprendices Activos</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background-color: {azul}; padding: 10px; border-radius: 50%; text-align: center; margin-bottom: 10px; width: 100px; height: 100px; line-height: 80px; margin: 0 auto;">
            <span style="color: #FECA1D; font-size: 24px; font-weight: bold;">{active_count}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Bajas Card
with containerBajas:
    st.markdown(
        f"<div style='text-align: center; color: {azul}; font-size: 16px; font-weight: bold;'>Bajas %</div>",
        unsafe_allow_html=True,
    )
    baja_chart = create_donut_chart(baja, "Bajas", 'blue')
    st.altair_chart(baja_chart, use_container_width=True)
with containerBajasCantidad:
        st.markdown(
            f"<div style='text-align: center; color: {azul}; font-size: 16px;font-weight: bold;'>Cantidad</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background-color: {azul}; padding: 10px; border-radius: 50%; text-align: center; margin-bottom: 10px; width: 100px; height: 100px; line-height: 80px; margin: 0 auto;">
                <span style="color: #FECA1D; font-size: 24px; font-weight: bold;">{bajaCount}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# Finalizados Card
with containerFinalizados:
    st.markdown("<div style='text-align: center;font-weight: bold;'>Finalizados %</div>", unsafe_allow_html=True)
    # Use columns to place the donut chart and "Cantidad" side-by-side
    finalizado_chart = create_donut_chart(finalizado, "Finalizados", 'orange')
    st.altair_chart(finalizado_chart, use_container_width=True)
with containerFinalizadosCant:
    st.markdown(
        f"<div style='text-align: center; color: {azul}; font-size: 16px;font-weight: bold;'>Cantidad</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background-color: {azul}; padding: 10px; border-radius: 50%; text-align: center; margin-bottom: 10px; width: 100px; height: 100px; line-height: 80px; margin: 0 auto;">
            <span style="color: #FECA1D; font-size: 24px; font-weight: bold;">{finalizadoCount}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

custom_colors = [aquamarine, amarillo, azul, orange] 
chartDepto, chartHotel, chartEstudio, chartZona  = st.columns(4)
fig_size = (4, 4)

with chartDepto:
    # Create the figure and axis for the bar chart
    fig1, ax1 = plt.subplots(figsize=fig_size)
    
    # Plot a bar chart and apply custom colors
    value_counts = filtered_df[graficos[0]].value_counts()
    if not value_counts.empty and value_counts.sum() > 0:
        value_counts.plot.bar(ax=ax1, color=custom_colors)
        
        # Add the amounts on top of each bar
        for index, value in enumerate(value_counts):
            ax1.text(index, value, str(value), ha='center', va='bottom', fontsize=10)
        
        # Set the title and labels
        ax1.set_ylabel("Count")
        ax1.set_title(graficos[0])
        
        # Display the bar chart in Streamlit
        st.pyplot(fig1)

with chartHotel:
    fig2, ax2 = plt.subplots(figsize=fig_size)
    value_counts = filtered_df[graficos[1]].value_counts()
    if not value_counts.empty and value_counts.sum() > 0:
        value_counts.plot.bar(ax=ax2, color=custom_colors)
        
                # Add the amounts on top of each bar
        for index, value in enumerate(value_counts):
            ax2.text(index, value, str(value), ha='center', va='bottom', fontsize=10) 
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=8)
        # Set the title and labels
        ax2.set_ylabel("Count")
        ax2.set_title(graficos[1])
        st.pyplot(fig2)
    
with chartEstudio:
    fig3, ax3 = plt.subplots(figsize=fig_size)
    value_counts = filtered_df[graficos[2]].value_counts()
    if not value_counts.empty and value_counts.sum() > 0:
        value_counts.plot.bar(ax=ax3, color=custom_colors)
        
                # Add the amounts on top of each bar
        for index, value in enumerate(value_counts):
            ax3.text(index, value, str(value), ha='center', va='bottom', fontsize=10) 
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right', fontsize=8)
        # Set the title and labels
        ax3.set_ylabel("Count")
        ax3.set_title(graficos[2])
        st.pyplot(fig3)

with chartZona:
    fig4, ax4 = plt.subplots(figsize=fig_size)
    value_counts = filtered_df[graficos[3]].value_counts()
    if not value_counts.empty and value_counts.sum() > 0:
        value_counts.plot.bar(ax=ax4, color=custom_colors)
        
                # Add the amounts on top of each bar
        for index, value in enumerate(value_counts):
            ax4.text(index, value, str(value), ha='center', va='bottom', fontsize=10) 

        # Set the title and labels
        ax4.set_ylabel("Count")
        ax4.set_title(graficos[3])
        st.pyplot(fig4)


def getRotationInfo():
    rotacion = get_sheets(connectionUsuarios, [rotationSheet])
    return rotacion[0]

#donde estan mis aprendices
with st.container():
    st.header('**¿En dónde se encuentran hoy los aprendices?**')
    graficoHotel, tablaAprendicesHoy  = st.columns([1.6,1.6])
    with graficoHotel:
        if active_candidates is not None and not active_candidates.empty:
            rotacion= getRotationInfo()
            rotacion[columnaMesesActivos] = pd.to_datetime(rotacion[columnaMesesActivos], format='%d/%m/%Y')
            # Filtrar datos para el próximo mes en adelante y agrupar por hotel, mes y departamento
            hoy = datetime.today()
            mes_actual = hoy.replace(day=1)
            prox_mes = hoy.replace(day=1) + timedelta(days=31)
            prox_mes = prox_mes.replace(day=1)  # Primer día del próximo mes
            dfRotacion = rotacion[rotacion[columnaMesesActivos] >= mes_actual]
            # Crear una columna para el mes (año-mes) y agrupar
            dfRotacion = dfRotacion.drop_duplicates(subset=[columnaNombre, columnaDeptoOrigen, columnaDeptoDestino, columnaMesesActivos])
            dfRotacion["Mes"] = dfRotacion[columnaMesesActivos].dt.to_period("M").astype(str)
            dfRotacion[columnaDeptoDestino] = dfRotacion[columnaDeptoDestino].str.strip().str.title()
            # Agrupar por hotel, mes y departamento destino
            df_grouped = dfRotacion.groupby([columnaHotelDestino, "Mes", columnaDeptoDestino]).size().reset_index(name="Cantidad")

            # Obtener los próximos 12 meses como períodos
            meses_futuros = pd.date_range(prox_mes, periods=12, freq="MS").strftime("%Y-%m").tolist()
            color_map = generate_color_map(dfRotacion, columnaDeptoDestino)
            # Crear gráficos individuales para cada hotel
            hoteles = dfRotacion[columnaHotelDestino].unique()
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
    desired_position = 3  # Assuming 0-based indexing
    column_to_move = result_df.pop("Meses Activos")  # Remove 'Meses Activos' temporarily
    result_df.insert(desired_position, "Meses Activos", column_to_move) 
    result_df= result_df.sort_values(by=columnaFechaInicioRotacion,ascending=[False])
    with tablaAprendicesHoy:
        st.write('Mis Aprendices:')
        if result_df is not None and not result_df.empty:
            st.dataframe(result_df, hide_index="true")
        else:
            st.write(noDatosDisponibles)
        

#Container Feedback
def getFeebackDetails():
    feedbacks = get_sheets(connectionFeedbacks, [worksheetPulse1Semana,worksheetCambioArea,worksheetFormulario1Mes,worksheetFormulario4Mes, worksheetFormularioAprendizCierre1Ciclo, worksheetFormularioAprendizCierre2Ciclo])
    return feedbacks

feedbacks= getFeebackDetails()

#feedback details 
with st.container():
    st.header('**¿Cómo se están sintiendo en cada etapa del proceso?**')
    tutorFilter, spaceFilte = st.columns([2,5])
    with tutorFilter:
        tutor_options_feedback =[value for value in df[topFilters[5]].unique() if pd.notna(value) and str(value).strip() != ""]
        tutor_options_feedback = sorted(tutor_options_feedback)
        tutor = tutorFilter.selectbox("**TUTOR**", options=["Todos"] + tutor_options_feedback,key='select_tutor_feed')
        df = df[
        ((df[topFilters[5]] == tutor) | (tutor == "Todos"))]
active_candidates_feed = df[df[topFilters[6]].str.upper() == 'ACTIVO']
feedbackPulseDf = feedbacks[0][feedbacks[0][columnaEmail].apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
        df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else x)
    )]
feedbackPulseDf = feedbackPulseDf.drop_duplicates(subset=[columnaEmail])
if feedbackPulseDf is not None and not feedbackPulseDf.empty:
    pulse1SemanaPromedio = getFeedbackPulse1Semana(feedbackPulseDf)
    colorPulse= feedbackColor(pulse1SemanaPromedio)

feedbackCambioAreaDf= feedbacks[1][feedbacks[1][columnaEmail].apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
    df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else x)
)]
feedbackCambioAreaDf = feedbackCambioAreaDf.drop_duplicates(subset=[columnaEmail])
if feedbackCambioAreaDf is not None and not feedbackCambioAreaDf.empty:
    cambioAreaPromedio = getFeedbackPromedioCambioArea(feedbackCambioAreaDf)
    colorCambioArea= feedbackColor(cambioAreaPromedio)

feedback1MesDf= feedbacks[2][feedbacks[2][columnaEmail].apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
    df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else x)
)]
feedback1MesDf = feedback1MesDf.drop_duplicates(subset=[columnaEmail])
if feedback1MesDf is not None and not feedback1MesDf.empty:
    primerMesPromedio = getFeedbackPromedioPrimerMes(feedback1MesDf)
    colorPrimerMes= feedbackColor(primerMesPromedio)

feedback4MesDf= feedbacks[3][feedbacks[3][columnaEmail].apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
    df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else x)
)]
feedback4MesDf = feedback4MesDf.drop_duplicates(subset=[columnaEmail])
if feedback4MesDf is not None and not feedback4MesDf.empty:
    cuartoMesPromedio = getFeedbackPromedioCuartoMes(feedback4MesDf)
    colorCuartoMes= feedbackColor(cuartoMesPromedio)

feedbackAprendizPrimerCierreDf= feedbacks[4][feedbacks[4][columnaEmail].apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
    df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else x)
)]
feedbackAprendizPrimerCierreDf = feedbackAprendizPrimerCierreDf.drop_duplicates(subset=[columnaEmail])
if feedbackAprendizPrimerCierreDf is not None and not feedbackAprendizPrimerCierreDf.empty:
    aprendizCierrePrimerCicloPromedio = getFeedbackPromedioAprendizCierrePrimerCiclo(feedbackAprendizPrimerCierreDf)
    colorAprendizCierrePrimerCiclo= feedbackColor(aprendizCierrePrimerCicloPromedio)

feedbackAprendizSegundoCierreDf= feedbacks[5][feedbacks[5][columnaEmail].apply(lambda x: x.lower() if isinstance(x, str) else x).isin(
    df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else x)
)]
feedbackAprendizSegundoCierreDf = feedbackAprendizSegundoCierreDf.drop_duplicates(subset=[columnaEmail])
if feedbackAprendizSegundoCierreDf is not None and not feedbackAprendizSegundoCierreDf.empty:
    aprendizCierreSegundoCicloPromedio = getFeedbackPromedioAprendizCierreSegundoCiclo(feedbackAprendizSegundoCierreDf)
    colorAprendizCierreSegundoCiclo= feedbackColor(aprendizCierreSegundoCicloPromedio)

metricaPulse, metricaCambioArea, metrica1Mes, metrica4Mes, metrica1Cierre, metrica2Cierrre = st.columns(6)
with metricaPulse:
    with st.container():
        st.markdown(
            f"""
                <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorPulse};">
                    <span style="color: black; font-size: 16px;font-weight: bold;">Pulse</span><br>
                    <span style="font-size: 20px; font-weight: bold;">{pulse1SemanaPromedio}</span>
                </div>
            """,
            unsafe_allow_html=True
        )
with metricaCambioArea:
    with st.container():
        st.markdown(
            f"""
                <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorCambioArea};">
                    <span style="color: black; font-size: 16px;font-weight: bold;">Cambio Area</span><br>
                    <span style="font-size: 20px; font-weight: bold;">{cambioAreaPromedio}</span>
                </div>
            """,
            unsafe_allow_html=True
        )
with metrica1Mes:
    with st.container():
        st.markdown(
            f"""
                <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorPrimerMes};">
                    <span style="color: black; font-size: 16px;font-weight: bold;">1° Mes</span><br>
                    <span style="font-size: 20px; font-weight: bold;">{primerMesPromedio}</span>
                </div>
            """,
            unsafe_allow_html=True
        )
with metrica4Mes:
    with st.container():
        st.markdown(
            f"""
                <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorCuartoMes};">
                    <span style="color: black; font-size: 16px;font-weight: bold;">4° Mes</span><br>
                    <span style="font-size: 20px; font-weight: bold;">{cuartoMesPromedio}</span>
                </div>
            """,
            unsafe_allow_html=True
        )
with metrica1Cierre:
    with st.container():
        st.markdown(
            f"""
                <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorAprendizCierrePrimerCiclo};">
                    <span style="color: black; font-size: 16px;font-weight: bold;">1° Cierre</span><br>
                    <span style="font-size: 20px; font-weight: bold;">{aprendizCierrePrimerCicloPromedio}</span>
                </div>
            """,
            unsafe_allow_html=True
        )
with metrica2Cierrre:
    with st.container():
        st.markdown(
            f"""
                <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorAprendizCierreSegundoCiclo};">
                    <span style="color: black; font-size: 16px;font-weight: bold;">2° Cierre</span><br>
                    <span style="font-size: 20px; font-weight: bold;">{aprendizCierreSegundoCicloPromedio}</span>
                </div>
            """,
            unsafe_allow_html=True
        )


with st.expander("Detalle de Feedbacks"):
    with st.container():
        tabs = st.tabs(feedback_types)
        with tabs[0]:
            if feedbackPulseDf is not None and not feedbackPulseDf.empty:
                st.dataframe(feedbackPulseDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)

        with tabs[1]:
            if feedbackCambioAreaDf is not None and not feedbackCambioAreaDf.empty:
                st.dataframe(feedbackCambioAreaDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[2]:
            if feedback1MesDf is not None and not feedback1MesDf.empty:
                st.dataframe(feedback1MesDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[3]:
            if feedback4MesDf is not None and not feedback4MesDf.empty:
                st.dataframe(feedback4MesDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[4]:
            if feedbackAprendizPrimerCierreDf is not None and not feedbackAprendizPrimerCierreDf.empty:
                st.dataframe(feedbackAprendizPrimerCierreDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[5]:
            if feedbackAprendizSegundoCierreDf is not None and not feedbackAprendizSegundoCierreDf.empty:
                st.dataframe(feedbackAprendizSegundoCierreDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)


with st.container():
    st.subheader('**Estado Respuestas**')
    tabs = st.tabs(feedback_types)
    for i, feedback in enumerate(feedback_types[:4]):
        with tabs[i]:
            st.write('')
            graficosRespuestas, respuestasRecibidas, respuestasPendientes, respuestasSinResponder, = st.columns([1,2,2,2])
            if i == 0:
                response_data, candidatos_feedback_inprogress = calcularEstadoRespuestas(active_candidates_feed, columnaEnvio1Feedback, hoy, feedbackPulseDf, columnaCorreoCandidato)
            if i == 1:
                response_data , candidatos_feedback_inprogress= calcularEstadoRespuestas(active_candidates_feed, columnaEnvio1Feedback, hoy, feedbackCambioAreaDf, columnaCorreoCandidato)
            if i == 2:
                response_data , candidatos_feedback_inprogress= calcularEstadoRespuestas(active_candidates_feed, columnaEnvio1Feedback, hoy, feedback1MesDf, columnaCorreoCandidato)
            if i == 3:
                response_data , candidatos_feedback_inprogress= calcularEstadoRespuestas(active_candidates_feed, columnaEnvio1Feedback, hoy, feedback4MesDf, columnaCorreoCandidato)
            if i == 4:
                response_data, candidatos_feedback_inprogress = calcularEstadoRespuestas(active_candidates_feed, columnaEnvio1Feedback, hoy, feedbackAprendizPrimerCierreDf, columnaCorreoCandidato)
            if i == 5:
                response_data , candidatos_feedback_inprogress= calcularEstadoRespuestas(active_candidates_feed, columnaEnvio1Feedback, hoy, feedbackAprendizSegundoCierreDf, columnaCorreoCandidato)
            with graficosRespuestas:
                chart = create_donut_chart(response_data['% Respuestas'], "Respuestas", 'orange')
                st.altair_chart(chart, use_container_width=True)
            with respuestasPendientes: 
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                        <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Feedback Enviado']}</span>
                        <span style="color: black; font-size: 24px; font-weight: bold;">Feedback Enviados</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with respuestasRecibidas: 
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                        <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Respuestas Recibidas']}</span>
                        <span style="color: black; font-size: 24px; font-weight: bold;">Respuestas Recibidas</span>
                        
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with respuestasSinResponder: 
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                        <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Feedback Sin responder']}</span>
                        <span style="color: black; font-size: 24px; font-weight: bold;">Feedback Sin responder</span>
                        
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.dataframe(getColumns(candidatos_feedback_inprogress,[columnaCandidatos, columnaCorreoCandidato, 'Feedback Respondido']))
  
