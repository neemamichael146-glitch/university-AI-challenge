from sqlalchemy import func, Column, String, Boolean, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base
import uuid
from datetime import datetime, timezone


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    COUNSELOR = "counselor"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")