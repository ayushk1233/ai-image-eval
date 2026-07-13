from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from .prompt import PromptResponse

class ImageGenerationCreate(BaseModel):
    prompt_id: int
    model_name: str

class ImageGenerationResponse(BaseModel):
    id: int
    prompt_id: int
    model_provider: str
    model_name: str
    image_path: Optional[str]
    settings: Optional[Any]
    generation_status: str
    error_message: Optional[str]
    created_at: datetime
    
    prompt: Optional[PromptResponse] = None

    class Config:
        from_attributes = True
