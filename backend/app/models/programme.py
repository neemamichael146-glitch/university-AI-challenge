from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class ProgrammeLevel(str, enum.Enum):
    CERTIFICATE = "certificate"
    DIPLOMA = "diploma"
    BACHELOR = "bachelor"
    MASTER = "master"
    PHD = "phd"


class Programme(Base):
    __tablename__ = "programmes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    level = Column(SQLEnum(ProgrammeLevel), nullable=False)
    duration_years = Column(Integer, nullable=False)
    duration_semesters = Column(Integer, nullable=True)
    credits = Column(Integer, nullable=True)
    entry_requirements = Column(Text, nullable=True)
    tuition_fee_tzs = Column(Float, nullable=True)
    tuition_fee_usd = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    university_id = Column(String(36), ForeignKey("universities.id"), nullable=False)
    university = relationship("University", back_populates="programmes")
    admissions = relationship("Admission", back_populates="programme", cascade="all, delete-orphan")