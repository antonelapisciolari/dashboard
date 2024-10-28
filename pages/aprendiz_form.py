import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection
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


default_values = {
    'current_page': 0,
    'responses': {}
}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data
with open('content/form_aprendiz.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

# Define pages and their questions
pageOneQuestions = range(0, 3)  # Questions for page 1
pageTwoQuestions = range(3, 7)  # Questions for page 2
pages = [pageOneQuestions, pageTwoQuestions]

# Total number of questions
total_questions = len(quiz_data["text_form"]["questions"])

def submit_answer(question_id, response):
    st.session_state.responses[question_id] = response
def next_question():
    st.session_state.current_page += 1
    print('next pregunta')

def create_gsheets_connection():
    try:
        conn = st.connection("gsheets_feedback", type=GSheetsConnection)
        return conn
    except Exception as e:
        st.error(f"Unable to connect to storage: {e}")
        logging.error(e, stack_info=True, exc_info=True)
        return None
    
def save_to_google_sheet(data):
        logging.info(f"Submitting records")
        responses_only = list(data.values())
        conn = create_gsheets_connection()
        existing_data = conn.read()
        new_row = pd.DataFrame([responses_only], columns=existing_data.columns)  # Ensure column names match
        
        # Step 4: Concatenate the new row with existing data
        updated_data = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(
                data=updated_data,
                )
        logging.info(f"Submitting successfully")
def all_questions_answered():
    current_page_questions = pages[st.session_state.current_page]
    for idx in current_page_questions:
        question_id = quiz_data["text_form"]["questions"][idx]["id"]
        if question_id not in st.session_state.responses or not st.session_state.responses[question_id]:
            return False
    return True
# Title and description
st.title(quiz_data["text_form"]["title"])
st.write(quiz_data["text_form"]["description"])
# Progress calculation
current_question_index = sum(len(pages[i]) for i in range(st.session_state.current_page))
progress_bar_value = current_question_index / total_questions
st.progress(progress_bar_value)

# Display questions for the current page
current_page_questions = pages[st.session_state.current_page]
for idx in current_page_questions:
    question_item = quiz_data["text_form"]["questions"][idx]
    st.subheader(question_item['question'])
    response = st.text_input(f"Respuesta", key=f"response_{idx}")

    if response:
        submit_answer(question_item["id"], response)

col1, col2 = st.columns(2)
with col1:
    if st.session_state.current_page > 0:
        st.button("Anterior", on_click=lambda: setattr(st.session_state, 'current_page', st.session_state.current_page - 1))

with col2:
    if st.session_state.current_page < len(pages) - 1:
        if st.button("Continuar", on_click=next_question):
            if all_questions_answered():
                st.session_state.current_page += 1
            else:
                st.warning("Por favor responde todas las preguntas en esta página antes de continuar.")
    else:
        if st.button("Completar"):
            if all_questions_answered():
                save_to_google_sheet(st.session_state.responses)
                st.success("Las respuestas se guardaron exitosamente!")
                st.write(quiz_data["text_form"]["cierre"])
            else:
                st.warning("Por favor responde todas las preguntas antes de completar.")