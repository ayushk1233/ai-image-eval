from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.database.session import get_db
from backend.app.models.participant import Participant
from backend.app.schemas.participant import ParticipantCreate, ParticipantResponse

router = APIRouter()

@router.post("/", response_model=ParticipantResponse)
def register_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    if participant.age < 18:
        raise HTTPException(status_code=400, detail="Participant must be at least 18 years old")
        
    existing = db.query(Participant).filter(Participant.email == participant.email).first()
    if existing:
        return existing
        
    new_participant = Participant(
        name=participant.name,
        email=participant.email,
        age=participant.age,
        consent=participant.consent,
        consent_given_at=datetime.utcnow() if participant.consent else None
    )
    
    db.add(new_participant)
    db.commit()
    db.refresh(new_participant)
    return new_participant

@router.get("/login", response_model=ParticipantResponse)
def login_participant(email: str, db: Session = Depends(get_db)):
    existing = db.query(Participant).filter(Participant.email == email).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Participant not found")
    return existing
