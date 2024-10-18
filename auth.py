import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def load_authenticator():
# Load configuration from YAML
    with open('credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize the authenticator with the loaded config
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    return authenticator, config
