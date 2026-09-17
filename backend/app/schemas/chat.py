from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    sources: Optional[List[Dict[str, Any]]] = None

    model_config = {"protected_namespaces": ()}


class ConversationCreate(BaseModel):
    title: Optional[str] = Field(None, max_length=500)


class ConversationUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, pattern="^(active|archived|closed)$")


class ConversationResponse(BaseModel):
    id: str
    title: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    content: str
    role: str
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    created_at: datetime

    model_config = {"protected_namespaces": (), "from_attributes": True}


class ConversationWithMessages(BaseModel):
    conversation: ConversationResponse
    messages: List[MessageResponse]