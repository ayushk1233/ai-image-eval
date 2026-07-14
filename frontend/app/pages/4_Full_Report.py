import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import get_export_csv

st.set_page_config(page_title="Deep Dive Report", page_icon="📜", layout="wide")

# Custom CSS for the blog style
st.markdown("""
    <style>
    .blog-header {
        font-family: 'Georgia', serif;
        font-size: 3rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .blog-meta {
        color: #a0a0a0;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .blog-text {
        font-size: 1.15rem;
        line-height: 1.6;
        color: #d0d0d0;
        margin-bottom: 1.5rem;
    }
    .highlight-box {
        background-color: rgba(255, 107, 107, 0.1);
        border-left: 4px solid #FF6B6B;
        padding: 1rem 1.5rem;
        margin: 2rem 0;
        font-style: italic;
        color: #f0f0f0;
    }
    .img-caption {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="blog-header">Large-Scale Image Eval: GPT-5 Mini vs Gemini Flash for Indian E-commerce</div>', unsafe_allow_html=True)
st.markdown('<div class="blog-meta">Josh Talks Research &nbsp;&nbsp;|&nbsp;&nbsp; Independent Evaluation</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. Fetch Data
# -----------------------------------------------------------------------------
@st.cache_data(ttl=60)
def load_data():
    try:
        csv_bytes = get_export_csv()
        df = pd.read_csv(io.BytesIO(csv_bytes))
        # Clean model names for display
        df['Model'] = df['Model Name'].str.split('/').str[-1].str.replace('-image-preview', '').str.replace('-image', '')
        return df
    except Exception as e:
        return None

df = load_data()

if df is None or df.empty:
    st.error("Could not load evaluation data. Ensure the backend is running and ratings exist.")
    st.stop()

total_votes = len(df)
total_raters = df['Participant Email'].nunique()
total_prompts = df['Prompt Text'].nunique()

st.markdown(f"""
<div class="blog-text">
<b>1. Abstract</b><br>
We conducted an independent study of text-to-image quality for Indian e-commerce, analyzing <b>{total_votes} human preference ratings</b> from <b>{total_raters} evaluators</b> across <b>{total_prompts} complex product prompts</b>. We evaluated three leading commercial models (GPT-5-Mini, Gemini 2.5 Flash, Gemini 3.1 Flash) on high-fidelity, culturally specific use-cases.
<br><br>
We report on a deep dive into two critical axes that dictate real-world usability: <b>Visual/Fabric Realism</b> and <b>Product Focus</b>. Our findings highlight a stark "Commercial Gap" between artistic generation and catalog-ready product photography.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Overall Performance
# -----------------------------------------------------------------------------
st.markdown("### 2. Overall Score (The Baseline)")
st.markdown("""
<div class="blog-text">
First, we look at the aggregate "Overall Score" across all metrics. This is the baseline equivalent to a standard "Full Band" studio benchmark.
</div>
""", unsafe_allow_html=True)

avg_overall = df.groupby('Model')['Overall Score'].mean().reset_index().sort_values('Overall Score', ascending=False)
fig_overall = px.bar(avg_overall, x='Overall Score', y='Model', orientation='h', 
                     color='Model', text='Overall Score',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
fig_overall.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig_overall.update_layout(xaxis_range=[1, 5], showlegend=False, height=300, 
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_overall, use_container_width=True)

st.markdown("""
<div class="highlight-box">
"While the models appear highly competitive in aggregate (all scoring roughly ~4.0/5), the overall score masks massive underlying differences in HOW they achieve that score. The baseline does not tell the full story."
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. The Commercial Gap
# -----------------------------------------------------------------------------
st.markdown("### 3. The Commercial Gap: Focus vs. Realism")
st.markdown("""
<div class="blog-text">
For an e-commerce brand, a generated image must do two things: 1) Look incredibly real (Fabric Realism, Anatomical Correctness), and 2) Actually showcase the product clearly (Product Focus, Commercial Viability). We analyzed how model rankings completely flip depending on which of these axes you optimize for.
</div>
""", unsafe_allow_html=True)

# Calculate averages for specific metrics
metrics_of_interest = ['Product Focus', 'Commercial Viability', 'Fabric Realism', 'Anatomical Correctness']
metrics_avg = df.groupby('Model')[metrics_of_interest].mean().reset_index()

# Melt for grouped bar chart
melted = metrics_avg.melt(id_vars=['Model'], value_vars=metrics_of_interest, var_name='Metric', value_name='Average Score')

fig_gap = px.bar(melted, x='Metric', y='Average Score', color='Model', barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Set2)
fig_gap.update_layout(yaxis_range=[1, 5], height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_gap, use_container_width=True)

st.markdown("""
<div class="blog-text">
<b>The Performance Reversal 🔄</b><br>
Notice how <b>GPT-5-Mini</b> performs strongly on <i>Product Focus</i> and <i>Commercial Viability</i>, framing the subject cleanly. However, it severely drops on <i>Fabric Realism</i> and <i>Anatomical Correctness</i>, giving it an "uncanny AI" feel.<br><br>
Conversely, <b>Gemini 3.1 Flash</b> dominates on <i>Fabric Realism</i> (textures, silk, zari work look flawless) but struggles significantly with <i>Product Focus</i>, often generating cinematic, distracting backgrounds that swallow the product.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Use-Case Specific Patterns
# -----------------------------------------------------------------------------
st.markdown("### 4. Category-Specific Patterns")
st.markdown("""
<div class="blog-text">
Does model performance shift depending on the type of clothing? We broke down the <b>Overall Score</b> by the specific E-commerce Use Case.
</div>
""", unsafe_allow_html=True)

use_case_avg = df.groupby(['Use Case', 'Model'])['Overall Score'].mean().reset_index()
fig_heatmap = px.density_heatmap(use_case_avg, x='Model', y='Use Case', z='Overall Score', 
                                 histfunc='avg', color_continuous_scale='Viridis',
                                 text_auto='.1f')
fig_heatmap.update_layout(height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_heatmap, use_container_width=True)

# -----------------------------------------------------------------------------
# 5. Visual Examples (The Reality Check)
# -----------------------------------------------------------------------------
st.markdown("### 5. Actual Examples from the Evals")
st.markdown("""
<div class="blog-text">
See the difference for yourself. Below are representative images from the exact same prompt, highlighting the "Focus vs Realism" trade-off we identified in the data.
</div>
""", unsafe_allow_html=True)

st.markdown("#### Prompt: Bridal Lehenga Showcase")
st.caption('"Close-up of a modern Indian bride wearing a pastel lehenga with intricate zari work, soft glowing wedding decor in the background, studio lighting, highly detailed"')

col1, col2, col3 = st.columns(3)
# These paths are relative to the Streamlit app execution context, assuming they exist in the repo
with col1:
    try:
        st.image("../../docs/showcase/bridal_gpt5mini.png", use_container_width=True)
    except:
        st.info("Image not found: GPT-5 Mini Bridal")
    st.markdown("<p class='img-caption'><b>GPT-5-Mini</b><br>High Focus, Lower Fabric Realism</p>", unsafe_allow_html=True)

with col2:
    try:
        st.image("../../docs/showcase/bridal_gemini25.png", use_container_width=True)
    except:
        st.info("Image not found: Gemini 2.5 Bridal")
    st.markdown("<p class='img-caption'><b>Gemini 2.5 Flash</b><br>Balanced</p>", unsafe_allow_html=True)

with col3:
    try:
        st.image("../../docs/showcase/bridal_gemini31.png", use_container_width=True)
    except:
        st.info("Image not found: Gemini 3.1 Bridal")
    st.markdown("<p class='img-caption'><b>Gemini 3.1 Flash</b><br>High Realism, Distracting Background</p>", unsafe_allow_html=True)

st.markdown("""
<div class="blog-text" style="margin-top: 2rem;">
<b>Conclusion:</b><br>
This large-scale blind evaluation proves that there is no "perfect" model for Indian E-commerce right out of the box. The choice of model must be dictated by your post-production workflow. If you have editors to fix textures, use GPT for its framing. If you want pristine photorealism and are willing to aggressively prompt against busy backgrounds, use Gemini.
</div>
""", unsafe_allow_html=True)
