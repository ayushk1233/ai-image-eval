from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class ImageGeneration(Base, TimestampMixin):
    __tablename__ = "image_generations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=True, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=True, index=True)
    model_provider = Column(String(50), nullable=False)
    model_name = Column(String(80), nullable=False)
    image_path = Column(String(255), nullable=True)
    settings = Column(JSON, nullable=True)
    generation_status = Column(String(20), nullable=False)
    error_message = Column(Text, nullable=True)
    custom_prompt_text = Column(Text, nullable=True)

    prompt = relationship("Prompt", back_populates="image_generations")
    participant = relationship("Participant", back_populates="image_generations")
    ratings = relationship("Rating", back_populates="image_generation", cascade="all, delete-orphan")
