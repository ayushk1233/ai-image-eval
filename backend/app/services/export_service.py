import csv
import io
from sqlalchemy.orm import Session
from sqlalchemy import text

def generate_ratings_csv(db: Session) -> str:
    """Generate a CSV string of all ratings and associated metadata."""
    query = """
    SELECT 
        COALESCE(p.prompt_text, ig.custom_prompt_text, 'Custom Prompt') as prompt_text,
        COALESCE(p.category, 'Custom') as category,
        COALESCE(p.use_case, 'User Defined') as use_case,
        ig.model_name,
        r.prompt_adherence,
        r.visual_quality,
        r.indian_relevance,
        r.overall,
        r.commercial_viability,
        r.product_focus,
        r.anatomical_correctness,
        r.lighting_consistency,
        r.fabric_realism,
        r.demographic_authenticity,
        r.comments,
        r.created_at as rating_timestamp
    FROM ratings r
    JOIN image_generations ig ON r.image_generation_id = ig.id
    LEFT JOIN prompts p ON ig.prompt_id = p.id
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
        "Commercial Viability",
        "Product Focus",
        "Anatomical Correctness",
        "Lighting Consistency",
        "Fabric Realism",
        "Demographic Authenticity",
        "Comments", 
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
            row.commercial_viability,
            row.product_focus,
            row.anatomical_correctness,
            row.lighting_consistency,
            row.fabric_realism,
            row.demographic_authenticity,
            row.comments,
            row.rating_timestamp
        ])
        
    return output.getvalue()
