import streamlit as st
import os
import sys

# Ensure api_client is available
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import register_participant, login_participant, get_participant_generations

def render_sidebar():
    """Renders the sidebar showing the user's generated images."""
    with st.sidebar:
        if "participant_id" in st.session_state and st.session_state.participant_id is not None:
            st.header("👤 Your Profile")
            st.success(f"Logged in as Participant #{st.session_state.participant_id}")
            
            st.markdown("---")
            st.page_link("pages/3_History.py", label="View Your Generated Images", icon="🖼️")
