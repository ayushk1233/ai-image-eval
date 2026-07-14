from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RatingCreate(BaseModel):
    participant_id: int
    image_generation_id: int
    prompt_adherence: int = Field(..., ge=1, le=5)
    visual_quality: int = Field(..., ge=1, le=5)
    indian_relevance: int = Field(..., ge=1, le=5)
    overall: int = Field(..., ge=1, le=5)
    commercial_viability: int = Field(3, ge=1, le=5)
    product_focus: int = Field(3, ge=1, le=5)
    anatomical_correctness: int = Field(3, ge=1, le=5)
    lighting_consistency: int = Field(3, ge=1, le=5)
    fabric_realism: int = Field(3, ge=1, le=5)
    demographic_authenticity: int = Field(3, ge=1, le=5)
    comments: Optional[str] = None

class RatingResponse(RatingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
