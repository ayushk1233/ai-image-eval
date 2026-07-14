from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from backend.app.database.session import get_db
from backend.app.models.image_generation import ImageGeneration
from backend.app.models.rating import Rating
from backend.app.schemas.image_generation import ImageGenerationCreate, ImageGenerationResponse
from backend.app.services.generation import generate_image_for_prompt

router = APIRouter()

@router.post("/", response_model=ImageGenerationResponse)
def create_generation(request: ImageGenerationCreate, db: Session = Depends(get_db)):
    """Triggers image generation via the abstraction worker."""
    try:
        generation = generate_image_for_prompt(
            db=db,
            model_name=request.model_name,
            prompt_id=request.prompt_id,
            custom_prompt_text=request.custom_prompt,
            api_key=request.api_key,
            participant_id=request.participant_id
        )
        return generation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/unrated", response_model=List[ImageGenerationResponse])
def get_unrated_generations(participant_id: int = Query(...), db: Session = Depends(get_db)):
    """Returns successfully generated images that the participant hasn't rated yet."""
    # Find IDs of images already rated by this participant
    rated_image_ids = db.query(Rating.image_generation_id).filter(
        Rating.participant_id == participant_id
    ).subquery()

    # Query completed images not in the rated list, and ONLY benchmark images (participant_id is None)
    unrated = db.query(ImageGeneration).filter(
        ImageGeneration.generation_status == "COMPLETED",
        ImageGeneration.participant_id.is_(None),
        ~ImageGeneration.id.in_(rated_image_ids)
    ).all()
    
    return unrated

@router.get("/participant/{participant_id}", response_model=List[ImageGenerationResponse])
def get_participant_generations(participant_id: int, db: Session = Depends(get_db)):
    """Returns successfully generated images that the participant created themselves."""
    generations = db.query(ImageGeneration).filter(
        ImageGeneration.participant_id == participant_id,
        ImageGeneration.generation_status == "COMPLETED"
    ).all()
    
    return generations
