import streamlit as st
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api_client import get_statistics, get_leaderboard, get_results, get_export_csv
from components.charts import render_leaderboard_chart, render_criteria_radar_chart

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stat-card {
        background: #1E2128;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #333;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FF6B6B;
        margin: 0.5rem 0;
    }
    .stat-label {
        color: #999;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Analytics Dashboard")
st.write("Real-time results and leaderboards across all participants.")

try:
    stats = get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-label">Total Images</div><div class="stat-value">{stats["total_images"]}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-label">Participants</div><div class="stat-value">{stats["total_participants"]}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-label">Avg Rating</div><div class="stat-value">{stats["avg_overall"]}</div></div>', unsafe_allow_html=True)
    with col4:
        winner = stats["current_leading_model"] or "N/A"
        if winner.startswith("openai"):
            winner = "GPT-5-Mini"
        elif winner.startswith("google"):
            winner = "Gemini"
        st.markdown(f'<div class="stat-card"><div class="stat-label">Leading Model</div><div class="stat-value" style="font-size:1.5rem; padding: 0.5rem 0;">{winner}</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    leaderboard = get_leaderboard()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        render_leaderboard_chart(leaderboard)
    with col2:
        render_criteria_radar_chart(leaderboard)
        
    st.markdown("---")
    st.markdown("### Raw Export")
    st.write("Download the complete CSV payload with all ratings, prompt metadata, and participant data.")
    
    csv_data = get_export_csv()
    st.download_button(
        label="📥 Download CSV Export",
        data=csv_data,
        file_name="ai_image_eval_results.csv",
        mime="text/csv",
        type="primary"
    )
        
except Exception as e:
    st.error(f"Failed to load dashboard data: {str(e)}")
