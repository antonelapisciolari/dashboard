import streamlit as st
import pandas as pd
import altair as alt

# Sample data (replace with your actual DataFrame)
data = pd.DataFrame({
    "CANDIDATOS": ["PATRICIA ESTEFANIA JORDAN", "AHINADA SANDUVET", "JESUS RAMIREZ", "ADRÍA ARTIGUES GUASP", "ADAY MARRERO ESTÉVEZ", "ADRIAN DUQUE DUQUE", "FERIEL LADJALI"],
    "POSICIÓN/DPT": ["ESTRUCTURA", "ESTRUCTURA", "ESTRUCTURA", "ESTRUCTURA", "RECEPCIÓN", "RECEPCIÓN", "RECEPCIÓN"],
    "CENTRO ENSEÑANZA": ["CIFP CESAR MANRIQUE", "I.E.S HERCULES", "IES EMILI DARDER", "IES SANT JOSEP OBRER", "HECANSA", "HECANSA", "INSTITUT ESCOLA D'HOTELERIA I TURISME DE BARCELONA"]
})

# Group by position and count the number of candidates per position
position_counts = data.groupby(['CENTRO ENSEÑANZA', 'POSICIÓN/DPT']).size().reset_index(name='Candidate Count')

# Create a selection for the hotel
hotels = position_counts['CENTRO ENSEÑANZA'].unique()
selected_hotel = st.selectbox("Select a hotel", hotels)

# Filter data by selected hotel
filtered_data = position_counts[position_counts['CENTRO ENSEÑANZA'] == selected_hotel]

# Plotting
chart = alt.Chart(filtered_data).mark_bar().encode(
    x='POSICIÓN/DPT:N',
    y='Candidate Count:Q',
    color='POSICIÓN/DPT:N'
).properties(
    title=f"Number of Candidates by Position for {selected_hotel}"
)

st.altair_chart(chart, use_container_width=True)