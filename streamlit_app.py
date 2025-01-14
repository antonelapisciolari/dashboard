import streamlit as st
st.set_page_config(
    page_title="FP Dual Dashboard",
    page_icon="https://assets4.cdn.iberostar.com/assets/favicon-aed60cf99a80a69e437a1476d22eea0d083d788070b7f4ac4c6c53595cf0687c.ico",  # You can use an emoji or a URL to an icon image
    layout="centered",  # Optional: You can set the layout as "centered" or "wide"
    initial_sidebar_state="collapsed"
)
from variables import username, password, loginButton,loginMessage,IncorrectPassword, forgotPassword
from navigation import make_sidebar
from time import sleep
import json
with open("cred.json") as f:
    credentials = json.load(f)
make_sidebar()
left_co, cent_co,last_co = st.columns(3)
with cent_co:
     st.image("./images/logoCreciendoJuntos.png")


st.title("Bienvenido a FP Dual - Iberostar")

user_dict = {user['username']: user for user in credentials['users']}
username = st.text_input("Email",placeholder="Ingrese email")
password = st.text_input("Contraseña", type="password", placeholder="Ingrese contraseña")

st.markdown(
    f'<div style="text-align: right;"><a href="mailto:support@embatconsultora.com">{forgotPassword}</a></div>',
    unsafe_allow_html=True
)



if st.button(loginButton, type="primary"):
    if username in user_dict and user_dict[username]['password'] == password:
        st.session_state.logged_in = True
        st.success(loginMessage)
        st.session_state.username = username.upper()
        st.session_state.role = user_dict[username]['role']
        sleep(0.5)
        if st.session_state.role == 'admin':
            st.switch_page("pages/admin_tutor_dashboard.py")
        if st.session_state.role == 'superadmin':
            st.switch_page("pages/admin_tutor_dashboard.py")    
        if st.session_state.role == 'tutor':
            st.switch_page("pages/tutor_recursos_dashboard.py")
    else:
        st.error(IncorrectPassword)