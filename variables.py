# variables.py


import streamlit as st
if 'language' not in st.session_state:
    st.session_state.language = "en"  # Default to English
if st.session_state.language == "es":
    import location.es as vars
else:
    import location.en as vars


page_icon="https://assets4.cdn.iberostar.com/assets/favicon-aed60cf99a80a69e437a1476d22eea0d083d788070b7f4ac4c6c53595cf0687c.ico"
companyIcon="./images/logoCreciendoJuntos.png"
title= vars.title
#images tutor dashboard 
preOnboardingImage="https://github.com/user-attachments/assets/7dd8d62d-b5ce-44ac-bda9-5eca1459a8b3"
onboardingImage="https://github.com/user-attachments/assets/2234162c-6c63-4ea4-9565-69206f7870fa"
seguimientoImage="https://github.com/user-attachments/assets/e55e814d-2b7c-4b7b-a8f6-e0c6927e06ca"
cierreImage="https://github.com/user-attachments/assets/c7609f53-4bb7-4b1b-8d1f-44bdbd24f379"