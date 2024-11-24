from data_utils import getColumns
import streamlit as st
import json

with open('content/formularioPulse1Semana.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

def getFeedbackPulse1Semana(feedback):
    dfiltered = getColumns(feedback, [quiz_data["text_form"]["questions"][1]["question"], quiz_data["text_form"]["questions"][2]["question"], quiz_data["text_form"]["questions"][4]["question"]])
    feedback_mapping = {
    "Genial 😊": 4,
    "Bien 👍": 3,
    "Regular 😐": 2,
    "Me ha costado 😕": 1,
    "Sí, me sirvió bastante": 3,
    "Estuvo bien, pero podría haber sido más completa": 2,
    "Me pareció que faltaba información": 1,
    "Sí, totalmente": 3,
    "Más o menos": 2,
    "No mucho": 1,
}
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))

    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)




with open('content/formulario_cambio_area.json', 'r', encoding='utf-8') as f:
    quiz_data_cambio_area = json.load(f)

def getFeedbackPromedioCambioArea(feedback):
    dfiltered = getColumns(feedback, [quiz_data_cambio_area["text_form"]["questions"][2]["question"],quiz_data_cambio_area["text_form"]["questions"][3]["question"]])
    feedback_mapping = {
    "Súper cómodo/a 😊": 4,
    "Bien": 3,
    "Me costó adaptarme": 2,
    "No me sentí cómodo/a": 1,
    4:4,
    3:3,
    2:2,
    1:1
}
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))
    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)


with open('content/formulario_primer_mes.json', 'r', encoding='utf-8') as f:
    quiz_data_primer_mes = json.load(f)

def getFeedbackPromedioPrimerMes(feedback):
    dfiltered = getColumns(feedback,[quiz_data_primer_mes["text_form"]["questions"][1]["question"],quiz_data_primer_mes["text_form"]["questions"][2]["question"],quiz_data_primer_mes["text_form"]["questions"][3]["question"],quiz_data_primer_mes["text_form"]["questions"][4]["question"],quiz_data_primer_mes["text_form"]["questions"][5]["question"]])
    feedback_mapping = {
    "Súper bien": 4,
    "Bien": 3,
    "Un poco perdido/a": 2,
    "No me sentí cómodo/a": 1,
    4:4,
    3:3,
    2:2,
    1:1
}
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))
    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)
