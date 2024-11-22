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
    df_mapped = dfiltered.applymap(lambda x: feedback_mapping.get(x, 0))

    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)


