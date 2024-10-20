import streamlit as st
from auth import load_authenticator
# Load authenticator and config
authenticator = load_authenticator()
def showSuperAdmins():
    st.sidebar.page_link('pages/admin_dashboard.py', label='General Dashboard')
    st.sidebar.page_link('pages/progression_dashboard.py', label='Progress Dashboard')
    st.sidebar.page_link('pages/tutor_dashboard.py', label='Tutor Dashboard')
    st.sidebar.page_link('pages/aprendiz_dashboard.py', label='Aprendices Dashboard')
    with st.sidebar:
        authenticator.logout("Logout", "sidebar") 
def showAdmins():
    st.sidebar.page_link('pages/admin_dashboard.py', label='General Dashboard')
    st.sidebar.page_link('pages/progression_dashboard.py', label='Progress Dashboard')
    with st.sidebar:
            authenticator.logout("Logout", "sidebar") 
def showTutors():
    st.sidebar.page_link('pages/tutor_dashboard.py', label='Tutor Dashboard')
    st.sidebar.page_link('pages/aprendiz_dashboard.py', label='Aprendices Dashboard')
    with st.sidebar:
            authenticator.logout("Logout", "sidebar")     