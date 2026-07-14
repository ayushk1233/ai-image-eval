import os
import uuid
import requests
from abc import ABC, abstractmethod
from openai import OpenAI
from backend.app.core.config import settings

class BaseImageProvider(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, model_name: str) -> dict:
        """
        Generate an image and save it locally.
        Returns:
            dict containing:
                "status": "COMPLETED" or "FAILED"
                "image_path": str or None
                "error_message": str or None
        """
        pass

    def _download_and_save_image(self, url: str) -> str:
        """Downloads the image from URL and saves it to IMAGE_STORAGE_PATH."""
        os.makedirs(settings.IMAGE_STORAGE_PATH, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(settings.IMAGE_STORAGE_PATH, filename)
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return filepath

class OpenRouterImageProvider(BaseImageProvider):
    def __init__(self, api_key: str = None):
        key = api_key if api_key else settings.OPENROUTER_API_KEY
        if not key:
            raise ValueError("No OpenRouter API key provided.")
        self.client = OpenAI(
            api_key=key,
            base_url=settings.OPENROUTER_BASE_URL
        )

    def generate_image(self, prompt: str, model_name: str) -> dict:
        try:
            response = self.client.images.generate(
                model=model_name,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            image_url = response.data[0].url
            b64_json = response.data[0].b64_json
            
            os.makedirs(settings.IMAGE_STORAGE_PATH, exist_ok=True)
            filename = f"{uuid.uuid4().hex}.png"
            local_path = os.path.join(settings.IMAGE_STORAGE_PATH, filename)
            
            if b64_json:
                import base64
                with open(local_path, 'wb') as f:
                    f.write(base64.b64decode(b64_json))
            elif image_url:
                local_path = self._download_and_save_image(image_url)
            else:
                raise ValueError("No image URL or base64 data returned by the provider.")
            
            return {
                "status": "COMPLETED",
                "image_path": local_path,
                "error_message": None
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "image_path": None,
                "error_message": str(e)
            }
