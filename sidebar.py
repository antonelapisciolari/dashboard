import streamlit as st

def showSuperAdmins():
    st.sidebar.page_link('pages/admin_dashboard.py', label='General Dashboard')
    st.sidebar.page_link('pages/progression_dashboard.py', label='Progress Dashboard')
    st.sidebar.page_link('pages/tutor_dashboard.py', label='Tutor Dashboard')
    st.sidebar.page_link('pages/aprendiz_dashboard.py', label='Aprendices Dashboard')
def showAdmins():
    st.sidebar.page_link('pages/admin_dashboard.py', label='General Dashboard')
    st.sidebar.page_link('pages/progression_dashboard.py', label='Progress Dashboard')
def showTutors():
    st.sidebar.page_link('pages/tutor_dashboard.py', label='Tutor Dashboard')
    st.sidebar.page_link('pages/aprendiz_dashboard.py', label='Aprendices Dashboard')