import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import get_participant_generations, submit_rating
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
                    
                    prompt_text = gen.get("custom_prompt_text")
                    if not prompt_text and gen.get("prompt"):
                        prompt_text = gen["prompt"].get("prompt_text")
                    if prompt_text:
                        st.markdown(f"<p style='font-size:0.9rem; color:#ccc; margin-top:0.5rem;'><em>\"{prompt_text}\"</em></p>", unsafe_allow_html=True)
                        
                    path = f"/app/{gen['image_path']}"
                    if os.path.exists(path):
                        st.image(path, use_container_width=True)
                    elif os.path.exists(f"../{gen['image_path']}"):
                        st.image(f"../{gen['image_path']}", use_container_width=True)
                        
                    rated_key = f"hist_rated_{gen['id']}"
                    if gen.get("ratings") or st.session_state.get(rated_key):
                        st.success("Rating submitted thanks , your score matter.")
                    else:
                        with st.form(f"hist_rate_form_{gen['id']}"):
                            st.write("Rate this image:")
                            adherence = st.slider("Prompt Adherence", 1, 5, 3, key=f"hist_adh_{gen['id']}")
                            visual = st.slider("Visual Quality", 1, 5, 3, key=f"hist_vis_{gen['id']}")
                            indian = st.slider("Indian Relevance", 1, 5, 3, key=f"hist_ind_{gen['id']}")
                            
                            st.markdown("---")
                            
                            comm = st.slider("Commercial Viability", 1, 5, 3, key=f"hist_comm_{gen['id']}")
                            prod = st.slider("Product Focus", 1, 5, 3, key=f"hist_prod_{gen['id']}")
                            anat = st.slider("Anatomical Correctness", 1, 5, 3, key=f"hist_anat_{gen['id']}")
                            light = st.slider("Lighting Consistency", 1, 5, 3, key=f"hist_light_{gen['id']}")
                            fabric = st.slider("Fabric Realism", 1, 5, 3, key=f"hist_fabric_{gen['id']}")
                            demo = st.slider("Demographic Auth.", 1, 5, 3, key=f"hist_demo_{gen['id']}")

                            st.markdown("---")
                            overall = st.slider("Overall Impression", 1, 5, 3, key=f"hist_ov_{gen['id']}")
                                
                            if st.form_submit_button("Submit Rating"):
                                try:
                                    submit_rating(
                                        st.session_state.participant_id, 
                                        gen['id'], 
                                        adherence, visual, indian, overall, 
                                        comm, prod, anat, light, fabric, demo, 
                                        ""
                                    )
                                    st.session_state[rated_key] = True
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to submit: {str(e)}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to load your images: {str(e)}")
