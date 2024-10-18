import streamlit as st
import sidebar as sd

st.title("Admin Dashboard")

if 'role' in st.session_state and st.session_state['role'] == 'admin':
        sd.showAdmins()
if 'role' in st.session_state and st.session_state['role'] == 'superadmin':
        sd.showSuperAdmins()