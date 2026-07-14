import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def render_leaderboard_chart(leaderboard_data):
    if not leaderboard_data:
        st.info("No leaderboard data available yet.")
        return
        
    df = pd.DataFrame(leaderboard_data)
    
    # We want a beautiful bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    models = df['model_name']
    win_rates = df['win_rate']
    
    bars = ax.barh(models, win_rates, color=['#FF6B6B', '#4ECDC4', '#FFE66D'])
    
    # Styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#FAFAFA')
    ax.spines['left'].set_color('#FAFAFA')
    ax.tick_params(colors='#FAFAFA')
    
    ax.set_xlabel('Win Rate (%)', color='#FAFAFA', fontsize=12)
    ax.set_title('Overall Win Rate by Model', color='#FAFAFA', fontsize=16, pad=20)
    
    # Add data labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                ha='left', va='center', color='#FAFAFA', fontweight='bold')
                
    st.pyplot(fig)

def render_criteria_radar_chart(leaderboard_data):
    if not leaderboard_data:
        return
        
    df = pd.DataFrame(leaderboard_data)
    
    st.markdown("### Average Scores by Criteria")
    
    criteria = [
        'avg_overall', 'avg_prompt_adherence', 'avg_visual_quality', 'avg_indian_relevance',
        'avg_commercial_viability', 'avg_product_focus', 'avg_anatomical_correctness',
        'avg_lighting_consistency', 'avg_fabric_realism', 'avg_demographic_authenticity'
    ]
    clean_labels = [
        'Overall', 'Prompt Adh.', 'Vis. Quality', 'Indian Rel.',
        'Comm. Viab.', 'Prod. Focus', 'Anat. Correct.',
        'Light Consist.', 'Fabric Real.', 'Demo. Auth.'
    ]
    
    # We can just show a grouped bar chart for simplicity and better readability than a radar in matplotlib
    df_melted = df.melt(id_vars=['model_name'], value_vars=criteria, var_name='Criterion', value_name='Score')
    
    # Since we have streamlit, let's use its native st.bar_chart if we can, or just matplotlib
    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')
    
    pivot_df = df.set_index('model_name')[criteria].T
    pivot_df.index = clean_labels
    
    pivot_df.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF', '#D4A5A5', '#9ADCFF', '#FFB7B2'])
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#FAFAFA')
    ax.spines['left'].set_color('#FAFAFA')
    ax.tick_params(colors='#FAFAFA', rotation=45)
    
    # Align rotated labels
    for tick in ax.get_xticklabels():
        tick.set_horizontalalignment('right')
    
    ax.set_ylabel('Average Score (1-5)', color='#FAFAFA', fontsize=12)
    ax.legend(facecolor='#0E1117', labelcolor='#FAFAFA', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(1, 5)
    
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
