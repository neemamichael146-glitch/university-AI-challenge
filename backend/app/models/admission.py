from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class AdmissionStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    UPCOMING = "upcoming"
    EXTENDED = "extended"


class Admission(Base):
    __tablename__ = "admissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    academic_year = Column(String(20), nullable=False, index=True)
    intake = Column(String(50), nullable=False)
    status = Column(SQLEnum(AdmissionStatus), default=AdmissionStatus.UPCOMING, nullable=False)
    application_start = Column(DateTime(timezone=True), nullable=False)
    application_deadline = Column(DateTime(timezone=True), nullable=False)
    extended_deadline = Column(DateTime(timezone=True), nullable=True)
    requirements = Column(Text, nullable=True)
    application_url = Column(String(500), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    university_id = Column(String(36), ForeignKey("universities.id"), nullable=False)
    university = relationship("University", back_populates="admissions")

    programme_id = Column(String(36), ForeignKey("programmes.id"), nullable=True)
    programme = relationship("Programme", back_populates="admissions")