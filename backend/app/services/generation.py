from sqlalchemy.orm import Session
from backend.app.models.prompt import Prompt
from backend.app.models.image_generation import ImageGeneration
from backend.app.services.image_provider import OpenRouterImageProvider
from backend.app.core.config import settings

def generate_image_for_prompt(db: Session, prompt_id: int, model_name: str) -> ImageGeneration:
    """
    Creates a PENDING ImageGeneration row, calls the provider, downloads the image,
    and updates the row with COMPLETED or FAILED status.
    """
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise ValueError(f"Prompt with ID {prompt_id} not found.")

    # Create initial PENDING row
    generation = ImageGeneration(
        prompt_id=prompt.id,
        model_provider=settings.DEFAULT_PROVIDER,
        model_name=model_name,
        generation_status="PENDING"
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)

    # Instantiate provider (could be dynamic based on DEFAULT_PROVIDER in the future)
    provider = OpenRouterImageProvider()
    
    # Call provider
    result = provider.generate_image(prompt.prompt_text, model_name)
    
    # Update row based on result
    generation.generation_status = result["status"]
    generation.image_path = result.get("image_path")
    generation.error_message = result.get("error_message")
    
    db.commit()
    db.refresh(generation)
    
    return generation
