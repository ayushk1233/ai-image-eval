import streamlit as st

st.set_page_config(
    page_title="AI Image Evaluation Platform",
    page_icon="📸",
    layout="wide",
)

st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    .hero {
        text-align: center;
        padding: 4rem 1rem;
        background: linear-gradient(135deg, #FF6B6B 0%, #845EC2 100%);
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
    }
    .hero h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .hero p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        max-width: 600px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>AI Evaluation Platform</h1>
    <p>Help us determine the best foundational models for E-commerce Fashion Product Photography in India.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Participant Flow")
    st.info("Are you here to rate images? Please proceed to the **Evaluate** section from the sidebar.")
    if st.button("Go to Evaluate →", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Evaluate.py")

with col2:
    st.markdown("### Admin Flow")
    st.info("Are you an administrator checking stats or triggering generation? Check the **Dashboard**.")
    if st.button("Go to Dashboard →", use_container_width=True):
        st.switch_page("pages/3_Dashboard.py")

st.markdown("---")
st.markdown("#### About this study")
st.write("""
We are evaluating how different cutting-edge models (OpenAI, Gemini) interpret prompts targeting Indian traditional and festive fashion.
Your ratings will directly contribute to identifying which models have the highest visual quality and the most authentic Indian cultural relevance.
""")
