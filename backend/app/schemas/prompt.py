from pydantic import BaseModel
from datetime import datetime

class PromptBase(BaseModel):
    prompt_text: str
    category: str
    use_case: str

class PromptResponse(PromptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
