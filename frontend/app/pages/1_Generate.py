import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import get_prompts, trigger_generation

st.set_page_config(page_title="Generate Images", page_icon="⚙️")

st.markdown("""
    <style>
    .stButton button { width: 100%; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚙️ Operations: Generate Images")
st.write("Trigger the background pipeline to generate images for seeded prompts.")

try:
    prompts = get_prompts()
    if not prompts:
        st.warning("No prompts found in the database. Please run the seed script.")
    else:
        st.write(f"Found **{len(prompts)}** prompts in the database.")
        
        prompt_options = {f"[{p['id']}] {p['prompt_text'][:50]}...": p['id'] for p in prompts}
        selected_prompt = st.selectbox("Select Prompt to Generate", options=list(prompt_options.keys()))
        
        # Hardcoding the 3 required models for the dropdown
        model_options = [
            "openai/gpt-5-image-mini",
            "google/gemini-2.5-flash-image",
            "google/gemini-3.1-flash-image-preview"
        ]
        selected_model = st.selectbox("Select Model", options=model_options)
        
        if st.button("Trigger Generation", type="primary"):
            with st.spinner("Generating image... This may take 10-30 seconds."):
                try:
                    result = trigger_generation(prompt_options[selected_prompt], selected_model)
                    if result.get("generation_status") == "COMPLETED":
                        st.success(f"Success! Image saved to `{result.get('image_path')}`")
                    else:
                        st.error(f"Generation failed: {result.get('error_message')}")
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
                    
except Exception as e:
    st.error("Could not connect to the backend API. Is it running?")
