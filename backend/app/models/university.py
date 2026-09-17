from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class University(Base):
    __tablename__ = "universities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), unique=True, nullable=False, index=True)
    short_name = Column(String(50), unique=True, nullable=False)
    tcu_code = Column(String(20), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    logo_url = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    established_year = Column(Integer, nullable=True)
    accreditation_status = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    programmes = relationship("Programme", back_populates="university", cascade="all, delete-orphan")
    admissions = relationship("Admission", back_populates="university", cascade="all, delete-orphan")
    scholarships = relationship("Scholarship", back_populates="university", cascade="all, delete-orphan")