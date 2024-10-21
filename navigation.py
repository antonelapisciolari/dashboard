import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("Menu")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/admin_dashboard.py", label="Admin Dashboard")
            st.page_link("pages/progression_dashboard.py", label="Progression Dashboard")
            st.page_link("pages/tutor_dashboard.py", label="Tutor Dashboard")
            st.page_link("pages/aprendiz_dashboard.py", label="Aprendiz Dashboard")

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")



def make_sidebar_admin():
    with st.sidebar:
        st.title("Menu")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/admin_dashboard.py", label="Admin Dashboard")
            st.page_link("pages/progression_dashboard.py", label="Progression Dashboard")

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")
def make_sidebar_tutor():
    with st.sidebar:
        st.title("Menu")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/tutor_dashboard.py", label="Tutor Dashboard")
            st.page_link("pages/aprendiz_dashboard.py", label="Aprendiz Dashboard")

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")         
def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("streamlit_app.py")
