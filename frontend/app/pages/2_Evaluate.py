import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import register_participant, get_unrated_images, submit_rating, login_participant
from components.auth import init_auth, login, logout

st.set_page_config(page_title="Evaluate Images", page_icon="📝", layout="wide")

st.markdown("""
    <style>
    .stSlider > div > div > div { background-color: #845EC2; }
    .image-container { 
        padding: 1rem; 
        border-radius: 12px; 
        background: #1E2128; 
        border: 1px solid #333;
        margin-bottom: 2rem;
    }
    .prompt-box {
        font-size: 1.2rem;
        padding: 1rem;
        background: #2D323E;
        border-left: 4px solid #FF6B6B;
        margin-bottom: 1rem;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

cookie_controller = init_auth()

st.title("📝 Evaluate Images")

if not st.session_state.participant_id:
    st.write("Before we begin, please log in or register. You must be 18 or older to register.")
    
    tab1, tab2 = st.tabs(["Log In", "Register"])
    
    with tab1:
        with st.form("login_form_eval"):
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
        with st.form("registration_form_eval"):
            name = st.text_input("Name")
            email = st.text_input("Email Address")
            age = st.number_input("Age", min_value=1, max_value=120, value=25)
            
            st.markdown("#### Consent")
            st.info("By clicking 'Register & Begin', I consent to my ratings being recorded and analyzed for this AI evaluation study. I understand my email will only be used to prevent duplicate submissions.")
            
            submitted = st.form_submit_button("Register & Begin", type="primary")
            
            if submitted:
                if age < 18:
                    st.error("You must be at least 18 years old.")
                elif not name or not email:
                    st.error("Please fill out all fields.")
                else:
                    try:
                        participant = register_participant(name, email, age, True)
                        login(cookie_controller, participant["id"])
                        st.success("Registered successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Registration failed. Please make sure you entered a valid email. Error details: {str(e)}")

else:
    st.write(f"Logged in as Participant ID: `{st.session_state.participant_id}`")
    if st.button("Log out"):
        logout(cookie_controller)
        st.rerun()
        
    st.markdown("---")
    
    try:
        unrated = get_unrated_images(st.session_state.participant_id)
        if not unrated:
            st.success("🎉 Evaluation submitted! You have rated all available images in the benchmark dataset.")
        else:
            # We show one image at a time for evaluation
            current_image = unrated[0]
            
            st.markdown(f"**{len(unrated)} images left to rate.**")
            
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="prompt-box">"{current_image["prompt"]["prompt_text"]}"</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("**Model Output:**")
                if current_image.get("image_path"):
                    st.image(f"{os.environ.get('PUBLIC_API_URL', 'http://localhost:8000')}/{current_image['image_path']}", use_container_width=True)
                else:
                    st.warning("No image path provided by the backend.")
            
            with col2:
                st.write("**Rate this generation (1 = Poor, 5 = Excellent):**")
                with st.form("rating_form"):
                    adherence = st.slider("Prompt Adherence", 1, 5, 3)
                    visual = st.slider("Visual Quality", 1, 5, 3)
                    indian = st.slider("Indian Cultural Relevance", 1, 5, 3)
                    
                    st.markdown("---")
                    
                    comm = st.slider("Commercial Viability", 1, 5, 3)
                    prod = st.slider("Product Focus", 1, 5, 3)
                    anat = st.slider("Anatomical Correctness", 1, 5, 3)
                    light = st.slider("Lighting Consistency", 1, 5, 3)
                    fabric = st.slider("Fabric Realism", 1, 5, 3)
                    demo = st.slider("Demographic Auth.", 1, 5, 3)

                    st.markdown("---")
                    overall = st.slider("Overall Impression", 1, 5, 3)

                    comments = st.text_area("Optional Comments")
                    
                    submit = st.form_submit_button("Submit Rating", type="primary")
                    if submit:
                        try:
                            submit_rating(
                                st.session_state.participant_id, 
                                current_image["id"], 
                                adherence, visual, indian, overall, 
                                comm, prod, anat, light, fabric, demo, 
                                comments
                            )
                            st.success("Rating submitted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to submit rating: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
                            
    except Exception as e:
        st.error(f"Failed to load images: {str(e)}")
