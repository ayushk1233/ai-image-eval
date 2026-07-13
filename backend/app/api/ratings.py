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
