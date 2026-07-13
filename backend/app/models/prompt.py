from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Prompt(Base, TimestampMixin):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prompt_text = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    use_case = Column(String(150), nullable=False)

    image_generations = relationship("ImageGeneration", back_populates="prompt", cascade="all, delete-orphan")
