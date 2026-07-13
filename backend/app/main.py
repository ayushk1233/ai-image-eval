from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.app.core.logging import setup_logging
from backend.app.api.health import router as health_router
from backend.app.api.participants import router as participants_router
from backend.app.api.prompts import router as prompts_router
from backend.app.api.generations import router as generations_router
from backend.app.api.ratings import router as ratings_router
from backend.app.api.analytics import router as analytics_router
import os

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Evaluation Platform")

# Configure CORS
cors_origins_str = os.environ.get("CORS_ORIGINS", "http://localhost:8501")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["Health"])
app.include_router(participants_router, prefix="/api/participants", tags=["Participants"])
app.include_router(prompts_router, prefix="/api/prompts", tags=["Prompts"])
app.include_router(generations_router, prefix="/api/generations", tags=["Generations"])
app.include_router(ratings_router, prefix="/api/ratings", tags=["Ratings"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up AI Evaluation Platform backend...")
