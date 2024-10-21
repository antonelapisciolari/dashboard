import streamlit as st
from time import sleep
import json
from navigation import make_sidebar

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
            st.switch_page("pages/admin_dashboard.py")
        if st.session_state.role == 'superadmin':
            st.switch_page("pages/admin_dashboard.py")    
        if st.session_state.role == 'tutor':
            st.switch_page("pages/tutor_dashboard.py")
    else:
        st.error("Incorrect username or password")