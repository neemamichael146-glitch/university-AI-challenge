from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum, func, Boolean, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class DocumentType(str, enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CSV = "csv"
    HTML = "html"
    MARKDOWN = "markdown"


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(500), nullable=False)
    original_filename = Column(String(500), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_path = Column(String(1000), nullable=True)
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    doc_metadata = Column(Text, nullable=True)
    is_processed = Column(Boolean, default=False, nullable=False)
    processing_error = Column(Text, nullable=True)
    chunk_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    uploaded_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    faq_id = Column(String(36), ForeignKey("faqs.id"), nullable=True)
    faq = relationship("FAQ", back_populates="documents")