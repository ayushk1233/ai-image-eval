from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Participant(Base, TimestampMixin):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    consent = Column(Boolean, nullable=False)
    consent_given_at = Column(DateTime, nullable=False)

    ratings = relationship("Rating", back_populates="participant", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('age >= 18', name='check_participant_age'),
    )
