import csv
import io
from sqlalchemy.orm import Session
from sqlalchemy import text

def generate_ratings_csv(db: Session) -> str:
    """Generate a CSV string of all ratings and associated metadata."""
    query = """
    SELECT 
        p.prompt_text,
        p.category,
        p.use_case,
        ig.model_name,
        r.prompt_adherence,
        r.visual_quality,
        r.indian_relevance,
        r.overall,
        r.comments,
        part.name as participant_name,
        part.email as participant_email,
        part.age as participant_age,
        r.created_at as rating_timestamp
    FROM ratings r
    JOIN image_generations ig ON r.image_generation_id = ig.id
    JOIN prompts p ON ig.prompt_id = p.id
    JOIN participants part ON r.participant_id = part.id
    ORDER BY r.created_at DESC
    """
    
    result = db.execute(text(query)).fetchall()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Prompt Text", 
        "Category", 
        "Use Case", 
        "Model Name", 
        "Prompt Adherence", 
        "Visual Quality", 
        "Indian Relevance", 
        "Overall Score", 
        "Comments", 
        "Participant Name", 
        "Participant Email", 
        "Participant Age", 
        "Timestamp"
    ])
    
    # Write rows
    for row in result:
        writer.writerow([
            row.prompt_text,
            row.category,
            row.use_case,
            row.model_name,
            row.prompt_adherence,
            row.visual_quality,
            row.indian_relevance,
            row.overall,
            row.comments,
            row.participant_name,
            row.participant_email,
            row.participant_age,
            row.rating_timestamp
        ])
        
    return output.getvalue()
