import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import get_prompts, trigger_generation, submit_rating, register_participant, login_participant
from components.auth import init_auth, login, logout

st.set_page_config(page_title="Generate Images", page_icon="⚙️", layout="wide")

cookie_controller = init_auth()

if "generated_images" not in st.session_state:
    st.session_state.generated_images = []

st.title("⚙️ Generate & Evaluate Images")

if not st.session_state.participant_id:
    st.write("You must be logged in to generate images.")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            login_contact = st.text_input("Email or Phone Number")
            if st.form_submit_button("Log In", type="primary"):
                try:
                    p = login_participant(login_contact)
                    login(cookie_controller, p["id"])
                    st.success("Logged in successfully!")
                    st.rerun()
                except Exception as e:
                    st.error("Login failed. Participant not found.")
                    
    with tab2:
        with st.form("registration_form_gen"):
            name = st.text_input("Name")
            email = st.text_input("Email or Phone Number")
            age = st.number_input("Age", min_value=1, max_value=120, value=25)
            st.info("By clicking 'Register', I consent to my ratings being recorded.")
            if st.form_submit_button("Register"):
                if age < 18:
                    st.error("Must be 18+")
                elif not name or not email:
                    st.error("Please fill all fields")
                else:
                    try:
                        p = register_participant(name, email, age, True)
                        login(cookie_controller, p["id"])
                        st.success("Registered successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Registration failed: {str(e)}")

else:
    st.write(f"Logged in as Participant ID: `{st.session_state.participant_id}`")
    if st.button("Log out"):
        logout(cookie_controller)
        st.session_state.generated_images = []
        st.rerun()
        
    st.markdown("---")
    
    st.info("⚠️ Please delete or revoke your API key from OpenRouter after usage for safety purposes.")
    api_key = st.text_input("OpenRouter API Key (Optional for loaded prompts, required if you don't have credits)", type="password")
    
    prompt_mode = st.radio("Prompt Type", ["Use Pre-loaded Benchmark Prompt", "Write Custom Prompt"])
    
    selected_prompt_id = None
    custom_prompt_text = None
    
    if prompt_mode == "Use Pre-loaded Benchmark Prompt":
        prompts = get_prompts()
        if prompts:
            options = {f"[{p['id']}] {p['prompt_text']}": p['id'] for p in prompts}
            selected = st.selectbox("Select Prompt (Full text shown below):", list(options.keys()))
            selected_prompt_id = options[selected]
        else:
            st.warning("No seeded prompts found.")
    else:
        custom_prompt_text = st.text_area("Enter your custom prompt here:")
        
    if st.button("Generate Images (All 3 Models)", type="primary"):
        if prompt_mode == "Write Custom Prompt" and not custom_prompt_text:
            st.error("Please enter a custom prompt.")
        else:
            st.session_state.generated_images = []
            models = [
                "openai/gpt-5-image-mini",
                "google/gemini-2.5-flash-image",
                "google/gemini-3.1-flash-image-preview"
            ]
            
            with st.spinner("Generating images across all 3 models... This may take up to 30 seconds."):
                for m in models:
                    try:
                        res = trigger_generation(
                            model_name=m,
                            prompt_id=selected_prompt_id,
                            custom_prompt=custom_prompt_text,
                            api_key=api_key if api_key.strip() != "" else None,
                            participant_id=st.session_state.participant_id
                        )
                        st.session_state.generated_images.append(res)
                    except Exception as e:
                        st.error(f"Failed to generate for {m}. Ensure you provided a valid API key. Error: {str(e)}")

    if st.session_state.generated_images:
        st.markdown("---")
        st.markdown("### Generated Images")
        
        cols = st.columns(len(st.session_state.generated_images))
        for idx, img_data in enumerate(st.session_state.generated_images):
            with cols[idx]:
                st.write(f"**{img_data['model_name'].split('/')[-1]}**")
                
                if img_data["generation_status"] == "COMPLETED":
                    path = f"/app/{img_data['image_path']}"
                    if os.path.exists(path):
                        st.image(path, use_container_width=True)
                    elif os.path.exists(f"../{img_data['image_path']}"):
                         st.image(f"../{img_data['image_path']}", use_container_width=True)
                         
                    rated_key = f"rated_{img_data['id']}"
                    if st.session_state.get(rated_key):
                        st.success("Rating Submitted!")
                    else:
                        with st.form(f"rate_form_{img_data['id']}"):
                            st.write("Rate this image:")
                            adherence = st.slider("Prompt Adherence", 1, 5, 3, key=f"adh_{img_data['id']}")
                            visual = st.slider("Visual Quality", 1, 5, 3, key=f"vis_{img_data['id']}")
                            indian = st.slider("Indian Relevance", 1, 5, 3, key=f"ind_{img_data['id']}")
                            
                            st.markdown("---")
                            
                            comm = st.slider("Commercial Viability", 1, 5, 3, key=f"comm_{img_data['id']}")
                            prod = st.slider("Product Focus", 1, 5, 3, key=f"prod_{img_data['id']}")
                            anat = st.slider("Anatomical Correctness", 1, 5, 3, key=f"anat_{img_data['id']}")
                            light = st.slider("Lighting Consistency", 1, 5, 3, key=f"light_{img_data['id']}")
                            fabric = st.slider("Fabric Realism", 1, 5, 3, key=f"fabric_{img_data['id']}")
                            demo = st.slider("Demographic Auth.", 1, 5, 3, key=f"demo_{img_data['id']}")

                            st.markdown("---")
                            overall = st.slider("Overall Impression", 1, 5, 3, key=f"ov_{img_data['id']}")

                            if st.form_submit_button("Submit Rating"):
                                try:
                                    submit_rating(
                                        st.session_state.participant_id, 
                                        img_data['id'], 
                                        adherence, visual, indian, overall, 
                                        comm, prod, anat, light, fabric, demo, 
                                        ""
                                    )
                                    st.session_state[rated_key] = True
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to submit: {str(e)}")
                else:
                    st.error(f"Failed: {img_data.get('error_message')}")
