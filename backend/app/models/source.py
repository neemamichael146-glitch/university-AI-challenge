from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum, func, Boolean, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class SourceType(str, enum.Enum):
    TCU_OFFICIAL = "tcu_official"
    UNIVERSITY_WEBSITE = "university_website"
    GOVERNMENT_PORTAL = "government_portal"
    NEWS_ARTICLE = "news_article"
    PDF_DOCUMENT = "pdf_document"
    USER_SUBMITTED = "user_submitted"


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=True)
    source_type = Column(SQLEnum(SourceType), nullable=False)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    source_metadata = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_checked = Column(DateTime(timezone=True), nullable=True)
    check_interval_days = Column(Integer, default=30, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    added_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)