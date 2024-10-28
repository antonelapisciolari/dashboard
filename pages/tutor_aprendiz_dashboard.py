from navigation import make_sidebar_tutor, make_sidebar
import streamlit as st
from page_utils import apply_page_config
from data_utils import filter_dataframe
from sheet_connection import get_google_sheet
import pandas as pd
import matplotlib.pyplot as plt
from variables import registroAprendices, azul
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

topFilters = ['FECHA INICIO', 'CANDIDATOS', 'HOTEL', 'FPDUAL / FCT']
def getInfo():
    sheet_id = registroAprendices
    filters = {topFilters[3]: ['Fp Dual', 'FCT'], "CORREO TUTOR": [st.session_state.username]}
    df = get_google_sheet(sheet_id, 0)
    dfiltered = filter_dataframe(df, filters)
    return dfiltered

df = getInfo()

df[topFilters[0]] = pd.to_datetime(df[topFilters[0]], format='%d/%m/%Y')
#filter containers
with st.container():
    
    col1, col2, col3, col4 = st.columns(4)
    with st.container():
        candidato = col1.selectbox("APRENDIZ", options=["Todos"] + df[topFilters[1]].unique().tolist())
    with st.container():
        hotel = col2.selectbox("HOTEL", options=["Todos"] + df[topFilters[2]].unique().tolist())
    with st.container():
        fecha_inicio = col3.date_input("FECHA INICIO", value=pd.to_datetime('01/01/2024'))
    with st.container():
        programa = col4.selectbox("TIPO DE PROGRAMA", options=["Todos"] + df[topFilters[3]].unique().tolist())

# Filter DataFrame based on selected values
filtered_df = df[
    ((df[topFilters[1]] == candidato) | (candidato == "Todos")) &
    ((df[topFilters[2]] == hotel) | (hotel == "Todos")) &
    (df[topFilters[0]] >= pd.to_datetime(fecha_inicio)) &  
    ((df[topFilters[3]] == programa) | (programa == "Todos"))
]

#pie chart container
graficos = ['POSICIÓN/DPT','HOTEL','ESTUDIOS']
with st.container():
    st.write('¿Cómo se distribuyen mis aprendices?')
    chartDepto, chartHotel, chartEstudio, statusAprendiz  = st.columns(4)
    with chartDepto:
        fig1, ax1 = plt.subplots()
        filtered_df[graficos[0]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1)
        ax1.set_ylabel('')
        ax1.set_title(graficos[0])
        st.pyplot(fig1)
    with chartHotel:
            fig2, ax2 = plt.subplots()
            filtered_df[graficos[1]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2)
            ax2.set_ylabel('')
            ax2.set_title(graficos[1])
            st.pyplot(fig2)
    with chartEstudio:
        fig3, ax3 = plt.subplots()
        filtered_df[graficos[2]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax3)
        ax3.set_ylabel('')
        ax3.set_title(graficos[2])
        st.pyplot(fig3)
    with statusAprendiz:
            st.markdown(
                f"""
                <div style="background-color: {azul}; padding: 10px; border-radius: 5px;text-align: center;margin-bottom: 10px;"">
                    <span style="color: white; font-size: 16px;">Aprendices Activos</span><br>
                    <span style="color: white; font-size: 20px; font-weight: bold;">{filtered_df['CANDIDATOS'].nunique()}</span>
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
# Display filtered data
    st.dataframe(filtered_df)
