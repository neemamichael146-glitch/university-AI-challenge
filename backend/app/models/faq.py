from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum, func, Boolean, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class FAQCategory(str, enum.Enum):
    ADMISSIONS = "admissions"
    PROGRAMMES = "programmes"
    SCHOLARSHIPS = "scholarships"
    TCU = "tcu"
    GENERAL = "general"
    TECHNICAL = "technical"


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(SQLEnum(FAQCategory), default=FAQCategory.GENERAL, nullable=False)
    keywords = Column(Text, nullable=True)
    view_count = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    created_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    documents = relationship("Document", back_populates="faq", cascade="all, delete-orphan")