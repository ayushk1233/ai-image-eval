from sqlalchemy import Column, Integer, ForeignKey, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Rating(Base, TimestampMixin):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False, index=True)
    image_generation_id = Column(Integer, ForeignKey("image_generations.id"), nullable=False, index=True)
    
    prompt_adherence = Column(Integer, nullable=False)
    visual_quality = Column(Integer, nullable=False)
    indian_relevance = Column(Integer, nullable=False)
    overall = Column(Integer, nullable=False)
    commercial_viability = Column(Integer, nullable=False, default=3)
    product_focus = Column(Integer, nullable=False, default=3)
    anatomical_correctness = Column(Integer, nullable=False, default=3)
    lighting_consistency = Column(Integer, nullable=False, default=3)
    fabric_realism = Column(Integer, nullable=False, default=3)
    demographic_authenticity = Column(Integer, nullable=False, default=3)
    
    comments = Column(Text, nullable=True)

    participant = relationship("Participant", back_populates="ratings")
    image_generation = relationship("ImageGeneration", back_populates="ratings")

    __table_args__ = (
        CheckConstraint('prompt_adherence BETWEEN 1 AND 5', name='check_prompt_adherence_range'),
        CheckConstraint('visual_quality BETWEEN 1 AND 5', name='check_visual_quality_range'),
        CheckConstraint('indian_relevance BETWEEN 1 AND 5', name='check_indian_relevance_range'),
        CheckConstraint('overall BETWEEN 1 AND 5', name='check_overall_range'),
        UniqueConstraint('participant_id', 'image_generation_id', name='uq_participant_image_rating'),
    )
