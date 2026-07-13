import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import get_participant_generations
from components.sidebar import render_sidebar
from components.auth import init_auth

st.set_page_config(page_title="Your Generated Images", page_icon="🖼️", layout="wide")

st.markdown("""
    <style>
    .image-container { 
        padding: 1rem; 
        border-radius: 12px; 
        background: #1E2128; 
        border: 1px solid #333;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

cookie_controller = init_auth()
render_sidebar()

st.title("🖼️ Your Generated Images")

if not st.session_state.participant_id:
    st.warning("Please log in on the Generate page to view your history.")
    st.stop()

try:
    with st.spinner("Loading your generated images..."):
        generations = get_participant_generations(st.session_state.participant_id)
        
    if not generations:
        st.info("You haven't generated any images yet.")
    else:
        st.write(f"Found {len(generations)} images.")
        
        # Display images in a grid
        cols = st.columns(3)
        for idx, gen in enumerate(generations):
            if gen.get("image_path"):
                with cols[idx % 3]:
                    st.markdown('<div class="image-container">', unsafe_allow_html=True)
                    st.markdown(f"**Model:** `{gen['model_name']}`")
                    path = f"/app/{gen['image_path']}"
                    if os.path.exists(path):
                        st.image(path, use_container_width=True)
                    elif os.path.exists(f"../{gen['image_path']}"):
                        st.image(f"../{gen['image_path']}", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to load your images: {str(e)}")
