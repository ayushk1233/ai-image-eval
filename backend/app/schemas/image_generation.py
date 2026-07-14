from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from .prompt import PromptResponse
from .rating import RatingResponse

class ImageGenerationCreate(BaseModel):
    prompt_id: Optional[int] = None
    custom_prompt: Optional[str] = None
    model_name: str
    api_key: Optional[str] = None
    participant_id: Optional[int] = None

class ImageGenerationResponse(BaseModel):
    id: int
    prompt_id: Optional[int] = None
    participant_id: Optional[int] = None
    model_provider: str
    model_name: str
    image_path: Optional[str]
    settings: Optional[Any]
    generation_status: str
    error_message: Optional[str]
    custom_prompt_text: Optional[str] = None
    created_at: datetime
    
    prompt: Optional[PromptResponse] = None
    ratings: Optional[list[RatingResponse]] = None

    class Config:
        from_attributes = True
