from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.app.database.session import get_db
from backend.app.models.rating import Rating
from backend.app.schemas.rating import RatingCreate, RatingResponse

router = APIRouter()

@router.post("/", response_model=RatingResponse)
def submit_rating(rating_data: RatingCreate, db: Session = Depends(get_db)):
    """Submit a rating for an image generation by a participant."""
    new_rating = Rating(
        participant_id=rating_data.participant_id,
        image_generation_id=rating_data.image_generation_id,
        prompt_adherence=rating_data.prompt_adherence,
        visual_quality=rating_data.visual_quality,
        indian_relevance=rating_data.indian_relevance,
        overall=rating_data.overall,
        commercial_viability=rating_data.commercial_viability,
        product_focus=rating_data.product_focus,
        anatomical_correctness=rating_data.anatomical_correctness,
        lighting_consistency=rating_data.lighting_consistency,
        fabric_realism=rating_data.fabric_realism,
        demographic_authenticity=rating_data.demographic_authenticity,
        comments=rating_data.comments
    )
    db.add(new_rating)
    try:
        db.commit()
        db.refresh(new_rating)
        return new_rating
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Rating already exists for this participant and image, or invalid ID")
