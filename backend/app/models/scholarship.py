from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Float, Integer, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class ScholarshipType(str, enum.Enum):
    FULL = "full"
    PARTIAL = "partial"
    TUITION_WAIVER = "tuition_waiver"
    STIPEND = "stipend"
    RESEARCH_GRANT = "research_grant"


class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    type = Column(SQLEnum(ScholarshipType), nullable=False)
    amount_tzs = Column(Float, nullable=True)
    amount_usd = Column(Float, nullable=True)
    coverage_details = Column(Text, nullable=True)
    eligibility_criteria = Column(Text, nullable=True)
    application_requirements = Column(Text, nullable=True)
    application_deadline = Column(DateTime(timezone=True), nullable=False)
    application_url = Column(String(500), nullable=True)
    contact_email = Column(String(255), nullable=True)
    number_of_awards = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    university_id = Column(String(36), ForeignKey("universities.id"), nullable=False)
    university = relationship("University", back_populates="scholarships")