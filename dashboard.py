import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import os

# Cargar los datos
@st.cache
def load_data():
    data = pd.read_csv('Registro_EMEA.csv')  # Ruta al archivo CSV
    return data

data = load_data()

# Verificar las columnas del DataFrame
st.write("Columnas del DataFrame:", data.columns)

# Mostrar las primeras filas para verificar la carga de datos
st.write("Primeras filas del DataFrame:", data.head())

# Asegurarse de que la columna 'Nombre' existe en el DataFrame
if 'Nombre' in data.columns:
    empleado_seleccionado = st.selectbox('Selecciona un empleado para ver detalles', data['Nombre'].unique())
    empleado_data = data[data['Nombre'] == empleado_seleccionado]
    st.write(f"Empleado seleccionado: {empleado_seleccionado}")
    st.write(empleado_data)
    
    # Unificación de competencias
    competencias = [
        'Liderazgo de Equipos', 'Gestión del Negocio', 
        'Excelencia con el cliente', 'Gestión de las Relaciones', 
        'Gestión de las Emociones', 'Gestión de la Diversidad y el Cambio'
    ]
    
    # Extracción de datos para 2023 y 2024
    empleado_competencias_2023 = [
        empleado_data[f'{competencia} 2023 (N)'].values[0] for competencia in competencias
    ]
    
    empleado_competencias_2024 = [
        empleado_data[f'{competencia} (n)'].values[0] for competencia in competencias
    ]
    
    # Creación del gráfico de radar
    fig5 = go.Figure()
    
    fig5.add_trace(go.Scatterpolar(
          r=empleado_competencias_2023,
          theta=competencias,
          fill='toself',
          name=f'{empleado_seleccionado} - 2023'
    ))
    
    fig5.add_trace(go.Scatterpolar(
          r=empleado_competencias_2024,
          theta=competencias,
          fill='toself',
          name=f'{empleado_seleccionado} - 2024'
    ))
    
    fig5.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 10]  # Suponiendo que la escala es de 0 a 10
        )),
      showlegend=True,
      title=f"Desempeño de {empleado_seleccionado} por Competencias en 2023 y 2024"
    )
    
    st.plotly_chart(fig5)
    
    # Exportar imagen del gráfico de radar
    radar_image_path = f"{empleado_seleccionado}_radar.png"
    fig5.write_image(radar_image_path)

    # Funcionalidad de exportación a PDF
    st.header("Exportación de Datos a PDF")
    export_pdf = st.button("Exportar Datos Filtrados a PDF")
    
    if export_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Título
        pdf.cell(200, 10, txt=f"Informe de {empleado_seleccionado}", ln=True, align='C')
        pdf.ln(10)
        
        # Añadir los detalles del empleado
        detalles = {
            "Nombre": empleado_data['Nombre'].values[0],
            "Hotel": empleado_data['Hotel'].values[0],
            "Region": empleado_data['Region'].values[0],
            "Posicion": empleado_data['Posición '].values[0],
            "Edad": empleado_data['Edad'].values[0],
            "Movilidad": empleado_data['Movilidad'].values[0],
            "Aspiraciones": empleado_data['Aspiraciones'].values[0]
        }
        
        for key, value in detalles.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
        
        pdf.ln(10)
        
        # Añadir el gráfico de radar
        pdf.image(radar_image_path, x=10, y=pdf.get_y(), w=180)
        
        # Guardar el archivo PDF
        pdf_output = f"{empleado_seleccionado}_informe.pdf"
        pdf.output(pdf_output)
        st.success(f'Informe PDF generado exitosamente: {pdf_output}')
        
        # Mostrar enlace de descarga
        with open(pdf_output, "rb") as file:
            btn = st.download_button(
                label="Descargar PDF",
                data=file,
                file_name=pdf_output,
                mime="application/octet-stream"
            )
        
        # Eliminar el archivo de imagen temporal
        os.remove(radar_image_path)
else:
    st.error("La columna 'Nombre' no existe en el DataFrame. Verifica el archivo CSV.")
