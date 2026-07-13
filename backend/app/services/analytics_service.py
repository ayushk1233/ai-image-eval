import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

def get_ratings_df(db: Session) -> pd.DataFrame:
    """Load ratings joined with image_generations and prompts into a pandas DataFrame."""
    query = """
    SELECT 
        r.id as rating_id,
        r.participant_id,
        r.overall,
        r.prompt_adherence,
        r.visual_quality,
        r.indian_relevance,
        ig.model_name,
        p.id as prompt_id,
        p.prompt_text,
        p.category,
        p.use_case
    FROM ratings r
    JOIN image_generations ig ON r.image_generation_id = ig.id
    JOIN prompts p ON ig.prompt_id = p.id
    """
    df = pd.read_sql(text(query), db.connection())
    return df

def calculate_leaderboard(db: Session) -> List[Dict[str, Any]]:
    df = get_ratings_df(db)
    if df.empty:
        return []

    # 1. Calculate averages per model
    avg_df = df.groupby('model_name')[
        ['overall', 'prompt_adherence', 'visual_quality', 'indian_relevance']
    ].mean().reset_index()

    # 2. Calculate Win Rate
    # A "trial" is a specific (participant_id, prompt_id).
    # We find the max overall score in that trial, and any model achieving that max score gets a win.
    
    # max overall per (participant, prompt)
    max_scores = df.groupby(['participant_id', 'prompt_id'])['overall'].max().reset_index()
    max_scores = max_scores.rename(columns={'overall': 'max_overall'})
    
    # merge back to find winners
    merged = pd.merge(df, max_scores, on=['participant_id', 'prompt_id'])
    merged['is_winner'] = merged['overall'] == merged['max_overall']
    
    # Win rate = total wins / total times the model was rated
    wins = merged.groupby('model_name')['is_winner'].sum().reset_index()
    total_ratings = merged.groupby('model_name').size().reset_index(name='total')
    
    win_rate_df = pd.merge(wins, total_ratings, on='model_name')
    win_rate_df['win_rate'] = (win_rate_df['is_winner'] / win_rate_df['total']) * 100
    
    # combine
    final_df = pd.merge(avg_df, win_rate_df[['model_name', 'win_rate']], on='model_name')
    
    # sort by overall descending
    final_df = final_df.sort_values('overall', ascending=False)
    
    # convert to list of dicts
    result = []
    for _, row in final_df.iterrows():
        result.append({
            "model_name": row["model_name"],
            "win_rate": round(float(row["win_rate"]), 1),
            "avg_overall": round(float(row["overall"]), 2),
            "avg_prompt_adherence": round(float(row["prompt_adherence"]), 2),
            "avg_visual_quality": round(float(row["visual_quality"]), 2),
            "avg_indian_relevance": round(float(row["indian_relevance"]), 2)
        })
    return result

def calculate_statistics(db: Session) -> Dict[str, Any]:
    # Need total_images generated
    query_images = "SELECT count(*) FROM image_generations WHERE generation_status = 'COMPLETED'"
    total_images = db.execute(text(query_images)).scalar() or 0
    
    query_participants = "SELECT count(*) FROM participants"
    total_participants = db.execute(text(query_participants)).scalar() or 0
    
    df = get_ratings_df(db)
    avg_overall = 0.0
    leading_model = None
    
    if not df.empty:
        avg_overall = round(float(df['overall'].mean()), 2)
        leaderboard = calculate_leaderboard(db)
        if leaderboard:
            leading_model = leaderboard[0]["model_name"]
            
    return {
        "total_images": total_images,
        "total_participants": total_participants,
        "avg_overall": avg_overall,
        "current_leading_model": leading_model
    }

def get_prompt_results(db: Session) -> List[Dict[str, Any]]:
    df = get_ratings_df(db)
    if df.empty:
        return []
        
    # max overall per (participant, prompt)
    max_scores = df.groupby(['participant_id', 'prompt_id'])['overall'].max().reset_index()
    max_scores = max_scores.rename(columns={'overall': 'max_overall'})
    merged = pd.merge(df, max_scores, on=['participant_id', 'prompt_id'])
    merged['is_winner'] = merged['overall'] == merged['max_overall']

    result = []
    # group by prompt
    for (prompt_id, prompt_text, category, use_case), group in merged.groupby(['prompt_id', 'prompt_text', 'category', 'use_case']):
        models = []
        for model_name, m_group in group.groupby('model_name'):
            wins = m_group['is_winner'].sum()
            total = len(m_group)
            win_rate = (wins / total * 100) if total > 0 else 0
            avg_overall = m_group['overall'].mean()
            
            models.append({
                "model_name": model_name,
                "avg_overall": round(float(avg_overall), 2),
                "win_rate": round(float(win_rate), 1)
            })
            
        result.append({
            "prompt_id": int(prompt_id),
            "prompt_text": prompt_text,
            "category": category,
            "use_case": use_case,
            "models": models
        })
        
    return result
