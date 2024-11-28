from navigation import make_sidebar_tutor
import streamlit as st
from page_utils import apply_page_config
from streamlit_carousel import carousel

apply_page_config()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Sesion expirada. Redirigiendo a login...")
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'tutor':
        make_sidebar_tutor()

#leer el style.css 
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.subheader("Agenda")

carousel_items = []  # Initialize as an empty list

# Append items to the carousel
carousel_items.append({
    "title": "",
    "text": "",
    "img": "./images/agenda_1_DH.png"
})
carousel_items.append({
    "title": "",
    "text": "",
    "img": "./images/agenda_2_DH.png"
})

# Print to ver

carousel(items=carousel_items, container_height= 1100)