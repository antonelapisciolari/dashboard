import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sheet_connection import get_google_sheet
import pandas as pd
import pandasql as psql
import logging
def run():
    st.set_page_config(
        page_title="Formulario FP Dual",
        page_icon="❓",
    )

if __name__ == "__main__":
    run()

# Custom CSS for the buttons
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
</style>
""", unsafe_allow_html=True)


# Initialize session variables if they do not exist
default_values = {'current_index': 0, 'current_question': 0,'selected_option': None, 'answer_submitted': False}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)
if 'responses' not in st.session_state:
    st.session_state.responses = {}
# Load quiz data

with open('content/form_aprendiz.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

def submit_answer(response):
    st.session_state.responses[quiz_data["text_form"]["questions"][st.session_state.current_index]["id"]] = response

def next_question():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

def save_to_google_sheet(data):
    try:    
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = psql.load_meat()
            df = conn.update(
                        worksheet="formAprendiz",
                        data=data,
                    )
            st.cache_data.clear()
            st.rerun()

            # Display our Spreadsheet as st.dataframe
            st.dataframe(df.head(10))
    except Exception as e:
            st.error("Error reading/updating existing data: " + str(e))

# Title and description
st.title(quiz_data["text_form"]["title"])
st.write(quiz_data["text_form"]["description"])
# Progress bar
st.subheader(f"Pregunta {st.session_state.current_index + 1}")
progress_bar_value = (st.session_state.current_index + 1) / len(quiz_data["text_form"]["questions"])
st.progress(progress_bar_value)

# Display the question and answer options
question_item = quiz_data["text_form"]["questions"][st.session_state.current_index]

st.title(f"{question_item['question']}")

response = st.text_input("", label_visibility = 'hidden', value="",)
st.markdown(""" ___""")
# Answer selection

if st.session_state.current_index < len(quiz_data["text_form"]["questions"]) - 1:
    # "Siguiente" button to go to the next question
    if st.button("Siguiente"):
        if response:
            submit_answer(response)
            next_question()
        else:
            st.warning("Por favor ingresa una respuesta")
else:
    # On the last question, show "Completar" button to submit all responses
    if st.button("Completar"):
        if response:
            submit_answer(response)
            save_to_google_sheet(st.session_state.responses)
            restart_quiz()  # Reset quiz after completion
            st.success("Las respuestas se guardaron exitosamente!")
            st.write(quiz_data["text_form"]["cierre"])
        else:
            st.warning("Por favor ingresa una respuesta antes de completar.")