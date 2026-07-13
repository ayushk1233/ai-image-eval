from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from backend.app.database.session import get_db
from backend.app.schemas.analytics import LeaderboardItem, Statistics, PromptResult
from backend.app.services.analytics_service import (
    calculate_leaderboard,
    calculate_statistics,
    get_prompt_results
)
from backend.app.services.export_service import generate_ratings_csv
import io

router = APIRouter()

@router.get("/leaderboard", response_model=List[LeaderboardItem])
def get_leaderboard(db: Session = Depends(get_db)):
    """Get aggregated leaderboard by model."""
    return calculate_leaderboard(db)

@router.get("/statistics", response_model=Statistics)
def get_statistics(db: Session = Depends(get_db)):
    """Get high level statistics for the dashboard."""
    return calculate_statistics(db)

@router.get("/results", response_model=List[PromptResult])
def get_results(db: Session = Depends(get_db)):
    """Get detailed results broken down by prompt."""
    return get_prompt_results(db)

@router.get("/export")
def export_ratings_csv(db: Session = Depends(get_db)):
    """Export all ratings as a CSV file."""
    csv_string = generate_ratings_csv(db)
    response = StreamingResponse(io.StringIO(csv_string), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=ratings_export.csv"
    return response
