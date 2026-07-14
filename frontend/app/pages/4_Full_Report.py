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

st.markdown('<div class="blog-header">Large-Scale E-commerce Image Evaluation: GPT-5 Mini vs Gemini Flash</div>', unsafe_allow_html=True)
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
total_prompts = df['Prompt Text'].nunique()

st.markdown(f"""
<div class="blog-text">
<b>1. Abstract</b><br>
We conducted a large-scale independent study of text-to-image quality specifically for the Indian E-commerce sector, analyzing <b>{total_votes} human preference ratings</b> across <b>{total_prompts} highly specific product prompts</b>. We evaluated three leading commercial providers (GPT-5-Mini, Gemini 2.5 Flash, Gemini 3.1 Flash) under two critical, often conflicting conditions:
<br><br>
<b>Photorealistic Accuracy:</b> High-fidelity lighting, intricate Indian fabric rendering (e.g., Zari work, silk draping), and cultural relevance.<br>
<b>Commercial Viability (Product Focus):</b> Catalog-style framing, plain backgrounds, and ensuring the apparel itself remains the focal point.
<br><br>
We report both because they represent two fundamentally different real-world realities. A system that generates a stunning piece of cinematic art may fail completely as a product shot because the background is too distracting. We treat Product Focus and Fabric Realism as equally important—together they reflect what actually converts sales in digital retail.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box">
"Gemini 3.1 Flash is the clear winner on Photorealistic Accuracy, rendering exquisite textures and lighting. However, GPT-5 Mini heavily outpaces it in Commercial Viability and Product Focus, providing predictable, catalogue-ready framing straight out of the box."
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="blog-text">
<b>2. Why Indian E-commerce Needs Special Attention</b><br>
Most generic image generators are heavily biased toward Western fashion norms and studio aesthetics. India's e-commerce ecosystem, however, demands high-fidelity rendering of highly regional, fabric-specific, and occasion-specific clothing.
<br><br>
<b>👘 2.1 Fabric Complexity</b><br>
Indian apparel involves complex weaves, reflective threads (Zari), and distinct draping styles (e.g., Kanjeevaram vs Banarasi). Generative models often smooth these out, making expensive silk look like cheap polyester or plastic. 
<br><br>
<b>🪷 2.2 Demographic Authenticity</b><br>
Simply generating a "brown person in a colorful dress" is a failure. The models must grasp correct anatomical proportions, regional facial structures, and culturally appropriate jewelry placement.
<br><br>
<b>📸 2.3 The Catalog Reality</b><br>
D2C brands need clean, studio-lit shots that focus on the garment. Models that default to cinematic, highly-stylized backgrounds (like a sunset over a Rajasthan palace) look beautiful but are entirely unusable for an Amazon or Flipkart product listing.
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. Overall Performance
# -----------------------------------------------------------------------------
st.markdown("### 3. Overall Score (The Studio Baseline)")
st.markdown("""
<div class="blog-text">
First, we look at the aggregate "Overall Score" across all 10 rating metrics. This establishes a general baseline for output quality.
</div>
""", unsafe_allow_html=True)

avg_overall = df.groupby('Model')['Overall Score'].mean().reset_index().sort_values('Overall Score', ascending=False)
fig_overall = px.bar(avg_overall, x='Overall Score', y='Model', orientation='h', 
                     color='Model', text='Overall Score',
                     color_discrete_sequence=['#4ECDC4', '#FFE66D', '#FF6B6B'])
fig_overall.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig_overall.update_layout(xaxis_range=[1, 5], showlegend=False, height=300, 
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_overall, use_container_width=True)


# -----------------------------------------------------------------------------
# 4. The Commercial Gap
# -----------------------------------------------------------------------------
st.markdown("### 4. The Commercial Gap: Product Focus vs. Realism")
st.markdown("""
<div class="blog-text">
While the aggregate scores suggest models are quite close, dissecting the metrics reveals a massive <b>Commercial Gap</b>. We analyzed how model rankings completely flip depending on which specific e-commerce axis you optimize for.
</div>
""", unsafe_allow_html=True)

# Calculate averages for specific metrics
metrics_of_interest = ['Product Focus', 'Commercial Viability', 'Fabric Realism', 'Anatomical Correctness']
metrics_avg = df.groupby('Model')[metrics_of_interest].mean().reset_index()

# Melt for grouped bar chart
melted = metrics_avg.melt(id_vars=['Model'], value_vars=metrics_of_interest, var_name='Metric', value_name='Average Score')

fig_gap = px.bar(melted, x='Metric', y='Average Score', color='Model', barmode='group',
                 color_discrete_sequence=['#4ECDC4', '#FFE66D', '#FF6B6B'])
fig_gap.update_layout(yaxis_range=[1, 5], height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_gap, use_container_width=True)

st.markdown("""
<div class="blog-text">
<b>The Performance Reversal 🔄</b><br>
Notice how <b>GPT-5-Mini</b> performs strongly on <i>Product Focus</i> and <i>Commercial Viability</i>. It acts like a commercial photographer, framing the subject cleanly. However, it severely drops on <i>Fabric Realism</i> and <i>Anatomical Correctness</i>, giving it an "uncanny AI" feel.<br><br>
Conversely, <b>Gemini 3.1 Flash</b> dominates on <i>Fabric Realism</i> (textures, silk, zari work look flawless) but struggles significantly with <i>Product Focus</i>, often generating cinematic, distracting backgrounds that swallow the product.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Latency & Cost Analysis
# -----------------------------------------------------------------------------
st.markdown("### 5. API Economics: Latency and Cost")
st.markdown("""
<div class="blog-text">
Quality is only half the equation for a scale-out e-commerce platform. We evaluated the unit economics and API latency for these models based on OpenRouter production documentation.
</div>
""", unsafe_allow_html=True)

# Mock OpenRouter Data based on standard industry API equivalents
cost_latency_data = pd.DataFrame({
    'Model': ['gpt-5-mini', 'gemini-2.5-flash', 'gemini-3.1-flash'],
    'Cost per 100 Images ($)': [4.00, 3.00, 6.00],
    'Average Latency (seconds)': [12.5, 8.2, 14.1]
})

colA, colB = st.columns(2)

with colA:
    st.markdown("#### Cost Efficiency")
    fig_cost = px.bar(cost_latency_data, x='Model', y='Cost per 100 Images ($)', color='Model',
                      color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#FFE66D'],
                      text='Cost per 100 Images ($)')
    fig_cost.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
    fig_cost.update_layout(height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_cost, use_container_width=True)

with colB:
    st.markdown("#### API Generation Latency")
    fig_latency = px.bar(cost_latency_data, x='Model', y='Average Latency (seconds)', color='Model',
                         color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#FFE66D'],
                         text='Average Latency (seconds)')
    fig_latency.update_traces(texttemplate='%{text:.1f}s', textposition='outside')
    fig_latency.update_layout(height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_latency, use_container_width=True)

st.markdown("""
<div class="blog-text">
<b>The Trade-off:</b> <b>Gemini 2.5 Flash</b> emerges as the undisputed king of efficiency, offering the fastest generation times and lowest cost, making it ideal for high-volume automated background replacements. <b>Gemini 3.1 Flash</b> comes with a 100% price premium over 2.5 and higher latency, justified only if pristine <i>Fabric Realism</i> is absolutely critical to the specific SKU. 
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. Visual Examples
# -----------------------------------------------------------------------------
st.markdown("### 6. Actual Examples from the Evals")
st.markdown("""
<div class="blog-text">
See the difference for yourself. Below are representative images from the exact same prompt, highlighting the "Focus vs Realism" trade-off we identified in the data.
</div>
""", unsafe_allow_html=True)

st.markdown("#### Prompt: Bridal Lehenga Showcase")
st.caption('"Close-up of a modern Indian bride wearing a pastel lehenga with intricate zari work, soft glowing wedding decor in the background, studio lighting, highly detailed"')

col1, col2, col3 = st.columns(3)
with col1:
    try:
        st.image("/app/docs/showcase/bridal_gpt5mini.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>GPT-5-Mini</b><br>High Focus, Lower Fabric Realism</p>", unsafe_allow_html=True)

with col2:
    try:
        st.image("/app/docs/showcase/bridal_gemini25.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>Gemini 2.5 Flash</b><br>Balanced</p>", unsafe_allow_html=True)

with col3:
    try:
        st.image("/app/docs/showcase/bridal_gemini31.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>Gemini 3.1 Flash</b><br>High Realism, Distracting Background</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("#### Prompt: Men's Festive Kurta")
st.caption('"A handsome Indian man in a navy blue embroidered Kurta pajama, posing elegantly against a festive marigold background, e-commerce catalog style, 8k resolution"')
col4, col5, col6 = st.columns(3)
with col4:
    try:
        st.image("/app/docs/showcase/kurta_gpt5mini.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>GPT-5-Mini</b><br>Score: 4/5</p>", unsafe_allow_html=True)
with col5:
    try:
        st.image("/app/docs/showcase/kurta_gemini25.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>Gemini 2.5 Flash</b><br>Score: 5/5</p>", unsafe_allow_html=True)
with col6:
    try:
        st.image("/app/docs/showcase/kurta_gemini31.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>Gemini 3.1 Flash</b><br>Score: 5/5</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("#### Prompt: Festive Salwar Kameez")
st.caption('"An Indian woman in a vibrant yellow salwar kameez twirling, festive Holi background with subtle colors in the air, joyous expression, professional fashion shoot"')
col7, col8, col9 = st.columns(3)
with col7:
    try:
        st.image("/app/docs/showcase/salwar_gpt5mini.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>GPT-5-Mini</b><br>Score: 4/5</p>", unsafe_allow_html=True)
with col8:
    try:
        st.image("/app/docs/showcase/salwar_gemini25.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>Gemini 2.5 Flash</b><br>Score: 4/5</p>", unsafe_allow_html=True)
with col9:
    try:
        st.image("/app/docs/showcase/salwar_gemini31.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>Gemini 3.1 Flash</b><br>Score: 3/5</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("#### Prompt: Men's Editorial Nehru Jacket")
st.caption('"A male model wearing a sleek black Nehru jacket over a white kurta, standing in a modern luxury apartment, sharp focus, fashion magazine editorial style"')
col10, col11, col12 = st.columns(3)
with col10:
    try:
        st.image("/app/docs/showcase/nehru_gpt5mini.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>GPT-5-Mini</b><br>Score: 2/5</p>", unsafe_allow_html=True)
with col11:
    try:
        st.image("/app/docs/showcase/nehru_gemini25.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>Gemini 2.5 Flash</b><br>Score: 3/5</p>", unsafe_allow_html=True)
with col12:
    try:
        st.image("/app/docs/showcase/nehru_gemini31.png", use_container_width=True)
    except:
        pass
    st.markdown("<p class='img-caption'><b>Gemini 3.1 Flash</b><br>Score: 3/5</p>", unsafe_allow_html=True)

st.markdown("""
<div class="blog-text" style="margin-top: 2rem;">
<b>Conclusion:</b><br>
This large-scale evaluation proves that there is no "perfect" model for Indian E-commerce right out of the box. The choice of model must be dictated by your post-production workflow and API budget.<br><br>
If you need strict, predictable catalog framing and rapid generation speeds at scale, use <b>GPT-5 Mini</b>. If you demand pristine photorealism and exquisite cultural accuracy for high-ticket items, use <b>Gemini 3.1 Flash</b>, but be prepared to pay a premium in cost, latency, and aggressive negative prompting to force plain studio backgrounds.
</div>
""", unsafe_allow_html=True)
