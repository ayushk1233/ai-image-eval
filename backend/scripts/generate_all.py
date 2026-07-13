import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database.session import SessionLocal
from backend.app.models import Prompt
from backend.app.services.generation import generate_image_for_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODELS_TO_TEST = [
    "openai/gpt-5-image-mini",
    "google/gemini-2.5-flash-image",
    "google/gemini-3.1-flash-image-preview"
]

def run_collection(limit_prompts: int = 5):
    """
    Simulate the Phase 12 Data Collection run.
    This fetches prompts and fires generation requests to OpenRouter.
    """
    db = SessionLocal()
    try:
        prompts = db.query(Prompt).limit(limit_prompts).all()
        logger.info(f"Found {len(prompts)} prompts. Starting generation run...")
        
        for p in prompts:
            logger.info(f"--- Prompt [{p.id}]: {p.prompt_text[:50]}... ---")
            for model_name in MODELS_TO_TEST:
                logger.info(f"Generating with {model_name}...")
                try:
                    generation = generate_image_for_prompt(db, p.id, model_name)
                    logger.info(f"Result: {generation.generation_status} -> {generation.image_path or generation.error_message}")
                except Exception as e:
                    logger.error(f"Failed completely: {str(e)}")
                    
    finally:
        db.close()
        logger.info("Run completed.")

if __name__ == "__main__":
    # Ensure OPENROUTER_API_KEY is available
    if not os.environ.get("OPENROUTER_API_KEY"):
        logger.warning("OPENROUTER_API_KEY not found in environment. The API calls will likely fail.")
    run_collection(limit_prompts=1)  # Limiting to 1 to save time/credits for MVP demonstration
