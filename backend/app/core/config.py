from pydantic_settings import BaseSettings, SettingsConfigDict

import os

class Settings(BaseSettings):
    APP_NAME: str = "AI Evaluation Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str
    
    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    DEFAULT_PROVIDER: str = "openrouter"
    OPENAI_IMAGE_MODEL: str
    GEMINI_25_MODEL: str
    GEMINI_31_MODEL: str
    
    IMAGE_STORAGE_PATH: str = "generated_images"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".env"),
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
