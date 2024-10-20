import streamlit as st
st.set_page_config(
    page_title="FP Dual Dashboard",
    page_icon="https://assets4.cdn.iberostar.com/assets/favicon-aed60cf99a80a69e437a1476d22eea0d083d788070b7f4ac4c6c53595cf0687c.ico",  # You can use an emoji or a URL to an icon image
    layout="wide"  # Optional: You can set the layout as "centered" or "wide"
)
from auth import load_authenticator
import sidebar as sd
# Load authenticator and config
authenticator, config = load_authenticator()

authenticator.login()
if st.session_state['authentication_status']:
    # Retrieve the role of the logged-in user
    role = config['credentials']['usernames'][st.session_state['username']]['role']
    st.session_state['role'] = role
    # Role-based page rendering
    if role == 'superadmin':
        st.title('SuperAdmin Dashboard')
        sd.showSuperAdmins()
    elif role == 'admin':
        st.title('Admin Dashboard')
        sd.showAdmins()
    
    elif role == 'tutor':
        st.title('Tutor Dashboard')
        sd.showTutors()
    # Logout button in sidebar
    with st.sidebar:
            authenticator.logout("Logout", "sidebar") 
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')

elif st.session_state['authentication_status'] is None:
    st.info('Please enter your username and password')
