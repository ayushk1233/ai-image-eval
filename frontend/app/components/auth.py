import streamlit as st
from streamlit_cookies_controller import CookieController

def init_auth():
    controller = CookieController()
    
    # Try to read from cookie first
    cookie_id = controller.get('participant_id')
    
    if cookie_id:
        st.session_state.participant_id = int(cookie_id)
    elif "participant_id" not in st.session_state:
        st.session_state.participant_id = None
        
    return controller
    
def login(controller, participant_id):
    st.session_state.participant_id = int(participant_id)
    controller.set('participant_id', int(participant_id))
    
def logout(controller):
    st.session_state.participant_id = None
    controller.remove('participant_id')
