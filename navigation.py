import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from variables import adminRecursosTutorDashboard, adminTutorDashboard, aprendizDashboard,tutorDashboard, logoutButton, logoutMessage

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 200px;  /* Adjust the width to your preference */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        st.title("Menu")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/admin_recursos_tutor_dashboard.py", label=adminRecursosTutorDashboard)
            st.page_link("pages/admin_tutor_dashboard.py", label=adminTutorDashboard)
            st.page_link("pages/tutor_aprendiz_dashboard.py", label=aprendizDashboard)
            st.page_link("pages/tutor_recursos_dashboard.py", label=tutorDashboard)

            st.write("")
            st.write("")

            if st.button(logoutButton):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")



def make_sidebar_admin():
    with st.sidebar:
        st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 200px;  /* Adjust the width to your preference */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        st.title("Menu")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/admin_recursos_tutor_dashboard.py", label=adminRecursosTutorDashboard)
            st.page_link("pages/admin_tutor_dashboard.py", label=adminTutorDashboard)

            st.write("")
            st.write("")

            if st.button(logoutButton):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")
def make_sidebar_tutor():
    with st.sidebar:
        st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 200px;  /* Adjust the width to your preference */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        st.title("Menu")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/tutor_aprendiz_dashboard.py", label=aprendizDashboard)
            st.page_link("pages/tutor_recursos_dashboard.py", label=tutorDashboard)
            st.write("")
            st.write("")

            if st.button(logoutButton):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")         
def logout():
    st.session_state.logged_in = False
    st.info(logoutMessage)
    sleep(0.5)
    st.switch_page("streamlit_app.py")

