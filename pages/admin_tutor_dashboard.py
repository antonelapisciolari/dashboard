from navigation import make_sidebar_admin
import streamlit as st
import plotly.express as px
from page_utils import apply_page_config
from data_utils import filter_dataframe, getColumns,generate_color_map
from sheet_connection import get_google_sheet, get_sheets
import pandas as pd
import matplotlib.pyplot as plt
from variables import registroAprendices, azul, amarillo, aquamarine, connectionGeneral, worksheetPulse1Semana,connectionFeedbacks,connectionUsuarios, rotationSheet,orange, errorRedirection, gris, formAprendiz,noDatosDisponibles
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

#rotacion
columnaMesesActivos="Meses Activos"
columnaDeptoDestino="Departamento de Destino"
columnaDeptoOrigen="Departamento de Origen"
columnaHotelDestino="Hotel destino"
columnaNombre="Nombre"
#trae todos los datos filtrados por Tutor 
def getInfo():
    sheet_id = registroAprendices
    df = get_google_sheet(connectionGeneral,sheet_id)
    return df

df = getInfo()

#parseando las fechas
df[topFilters[0]] = pd.to_datetime(df[topFilters[0]], format='%d/%m/%Y')
df[topFilters[4]] = pd.to_datetime(df[topFilters[4]], format='%d/%m/%Y')
print(len(df))
df= df.drop_duplicates(subset=[columnaCorreoCandidato])
print(len(df))
active_candidates = df[df[topFilters[6]].str.upper() == 'ACTIVO']
def calcularPorcentajesStatus(df):
    aprendicesStatus = getColumns(df, [columnStatus])
    total_statuses = len(aprendicesStatus)
    finalizado_count = df[columnStatus].str.lower().eq('finalizado').sum()
    baja_count = df[columnStatus].str.lower().eq('baja').sum()
    activo_count = df[columnStatus].str.lower().eq('activo').sum()

    # Calcular los porcentajes
    finalizado_pct = int((finalizado_count / total_statuses) * 100)
    baja_pct = int((baja_count / total_statuses) * 100)
    return finalizado_pct, baja_pct,activo_count
#filter containers
with st.container():
    col1, col2, col3, col4,col5, col6 = st.columns(6)
    with st.container():
        tutor_options =[value for value in df[topFilters[1]].unique() if pd.notna(value) and str(value).strip() != ""]
        tutor = col1.selectbox("**TUTOR**", options=["Todos"] + df[topFilters[5]].unique().tolist())
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
finalizado, baja,active_count = calcularPorcentajesStatus(df)
with st.container():
    st.write('**¿Cómo se distribuyen los aprendices?**')
    custom_colors = [aquamarine, amarillo, azul, orange] 
    graficosContainer, estadisticas = st.columns([8,2])
    with graficosContainer:
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
    with estadisticas:
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
                    <span style="color: white; font-size: 16px;">Bajas</span><br>
                    <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{baja}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                    <span style="color: white; font-size: 16px;">Tasa de Finalización</span><br>
                    <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">{finalizado}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )

#Container Feedback
def getFeebackDetails():
    feedbacks = get_sheets(connectionFeedbacks, [worksheetPulse1Semana,formAprendiz])
    return feedbacks

#feedback details 
with st.container():
        st.write('**¿Cómo se están sintiendo en cada etapa del proceso?**')
        feedbackPulse, feedbackCambioArea, feedback = st.columns(3)
        with feedbackPulse:
            with st.container():
                with st.container():
                    st.markdown(
                        f"""
                        <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                            <span style="color: white; font-size: 16px;">Pulse</span><br>
                            <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">2</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # Second container (inside col2)
        with feedbackCambioArea:
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                        <span style="color: white; font-size: 16px;">Cambio de Area</span><br>
                        <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">2</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Third container (inside col3)
        with feedback:
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                        <span style="color: white; font-size: 16px;">3rd Feedback</span><br>
                        <span style="color: #FECA1D; font-size: 20px; font-weight: bold;">3.1</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def getRotationInfo():
    rotacion = get_sheets(connectionUsuarios, [rotationSheet])
    return rotacion[0]

#donde estan mis aprendices
with st.container():
    titulo, filtroHotel  = st.columns(2)
    with titulo:
        st.write('**¿En dónde se encuentran hoy los aprendices?**')
    with filtroHotel:
        hotelOptions = sorted(df[topFilters[2]].unique().tolist())
        hotel = filtroHotel.selectbox("HOTEL", options=["Todos"] + hotelOptions)
        columns_to_extract = [columnaCandidatos,columnaFechaInicio,columnaFechaFin,columnaPosicion, columnaHotel]
        actualCandidatos = getColumns(active_candidates, columns_to_extract)
        actualCandidatos[columns_to_extract[1]] = actualCandidatos[columns_to_extract[1]].dt.strftime('%d/%m/%Y')
        actualCandidatos[columns_to_extract[2]] = actualCandidatos[columns_to_extract[2]].dt.strftime('%d/%m/%Y')
        df_hotel = actualCandidatos[((actualCandidatos[topFilters[2]] == hotel) | (hotel == "Todos"))]
    
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
            df = rotacion[rotacion[columnaMesesActivos] >= mes_actual]
            # Crear una columna para el mes (año-mes) y agrupar
            df = df.drop_duplicates(subset=[columnaNombre, columnaDeptoOrigen, columnaDeptoDestino, columnaMesesActivos])
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


    with tablaAprendicesHoy:
        st.write('Aprendices:')
        if actualCandidatos is not None and not actualCandidatos.empty:
            st.dataframe(df_hotel,hide_index=True)
        else:
            st.write(noDatosDisponibles)
        