from sqlalchemy.orm import Session
from backend.app.models.prompt import Prompt
from backend.app.models.image_generation import ImageGeneration
from backend.app.services.image_provider import OpenRouterImageProvider
from backend.app.core.config import settings

def generate_image_for_prompt(db: Session, model_name: str, prompt_id: int = None, custom_prompt_text: str = None, api_key: str = None, participant_id: int = None) -> ImageGeneration:
    """
    Creates a PENDING ImageGeneration row, calls the provider, downloads the image,
    and updates the row with COMPLETED or FAILED status.
    """
    prompt = None
    if prompt_id:
        prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not prompt:
            raise ValueError(f"Prompt with ID {prompt_id} not found.")
    elif not custom_prompt_text:
        raise ValueError("Must provide either prompt_id or custom_prompt_text.")

    # Create initial PENDING row
    generation = ImageGeneration(
        prompt_id=prompt.id if prompt else None,
        participant_id=participant_id,
        custom_prompt_text=custom_prompt_text,
        model_provider=settings.DEFAULT_PROVIDER,
        model_name=model_name,
        generation_status="PENDING"
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)

    # Instantiate provider (could be dynamic based on DEFAULT_PROVIDER in the future)
    provider = OpenRouterImageProvider(api_key=api_key)
    
    # Call provider
    prompt_to_use = prompt.prompt_text if prompt else custom_prompt_text
    result = provider.generate_image(prompt_to_use, model_name)
    
    # Update row based on result
    generation.generation_status = result["status"]
    generation.image_path = result.get("image_path")
    generation.error_message = result.get("error_message")
    
    db.commit()
    db.refresh(generation)
    
    return generation
