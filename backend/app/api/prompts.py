from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.database.session import get_db
from backend.app.models.prompt import Prompt
from backend.app.schemas.prompt import PromptResponse

router = APIRouter()

@router.get("/", response_model=List[PromptResponse])
def get_prompts(db: Session = Depends(get_db)):
    """Fetch all prompts from the database."""
    prompts = db.query(Prompt).all()
    return prompts
