from pydantic import BaseModel, EmailStr
from datetime import datetime

class ParticipantCreate(BaseModel):
    name: str
    email: str
    age: int
    consent: bool

class ParticipantResponse(ParticipantCreate):
    id: int
    consent_given_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
