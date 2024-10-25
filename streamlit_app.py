import streamlit as st
from variables import title, page_icon
st.set_page_config(
    page_title=title,
    page_icon=page_icon,  # You can use an emoji or a URL to an icon image
    layout="centered"  # Optional: You can set the layout as "centered" or "wide"
)
from time import sleep
import json
import requests
from navigation import make_sidebar
if 'language' not in st.session_state:
    st.session_state.language = "es"  # Default to English
def set_user_language():
    try:
        response = requests.get("https://ipapi.co/json/")
        data = response.json()
        user_country = data.get("country") 
        st.session_state.language = "es" if user_country == "ES" else "en"
    except:
        st.session_state.language = "es" 
if 'language' not in st.session_state:
    set_user_language()
    
with open("cred.json") as f:
    credentials = json.load(f)
make_sidebar()

st.title("Welcome to FP Dual - Iberostar")

st.write("Please log in to continue")

user_dict = {user['username']: user for user in credentials['users']}
username = st.text_input("Email")
password = st.text_input("Password", type="password")



if st.button("Log in", type="primary"):
    if username in user_dict and user_dict[username]['password'] == password:
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        st.session_state.role = user_dict[username]['role']
        sleep(0.5)
        if st.session_state.role == 'admin':
            st.switch_page("pages/admin_tutor_dashboard.py")
        if st.session_state.role == 'superadmin':
            st.switch_page("pages/admin_tutor_dashboard.py")    
        if st.session_state.role == 'tutor':
            st.switch_page("pages/tutor_recursos_dashboard.py")
    else:
        st.error("Incorrect username or password")