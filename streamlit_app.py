import streamlit as st
st.set_page_config(
    page_title="FP Dual Dashboard",
    page_icon="https://assets4.cdn.iberostar.com/assets/favicon-aed60cf99a80a69e437a1476d22eea0d083d788070b7f4ac4c6c53595cf0687c.ico",  # You can use an emoji or a URL to an icon image
    layout="centered"  # Optional: You can set the layout as "centered" or "wide"
)
st.markdown("""
    <script>
        function getBrowserLanguage() {
            const userLang = navigator.language || navigator.userLanguage;
            // Update the URL with the user's language preference
            window.location.search = '?lang=' + userLang;
        }
        getBrowserLanguage();
    </script>
""", unsafe_allow_html=True)
query_params = st.query_params  # This is now a dictionary-like property
st.session_state.language = query_params.get("lang", ["en"])[0] 

from navigation import make_sidebar
from time import sleep
import json

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