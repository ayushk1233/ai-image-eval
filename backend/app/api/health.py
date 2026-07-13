from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database.session import get_db

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "service": "josh-ai-image-eval-backend"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database not reachable")

