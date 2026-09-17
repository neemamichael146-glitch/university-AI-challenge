from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum, func, Boolean, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    role = Column(SQLEnum(MessageRole), nullable=False)
    message_metadata = Column(Text, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    is_error = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    conversation = relationship("Conversation", back_populates="messages")