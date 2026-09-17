from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.services.chat_service import ChatService
from app.schemas.chat import (
    ChatRequest, ChatResponse,
    ConversationCreate, ConversationUpdate, ConversationResponse,
    MessageResponse, ConversationWithMessages
)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    return await service.send_message(current_user.id, chat_request)


@router.post("/conversations", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    return service.create_conversation(current_user.id, conversation_data)


@router.get("/conversations", response_model=dict)
async def list_conversations(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    return service.get_conversations(current_user.id, page, size, status)


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    conversation = service.get_conversation(conversation_id, current_user.id)
    messages_data = service.get_messages(conversation_id, current_user.id, page=1, size=100)
    
    return ConversationWithMessages(
        conversation=conversation,
        messages=messages_data["messages"],
    )


@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    conversation_data: ConversationUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    return service.update_conversation(conversation_id, current_user.id, conversation_data)


@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    service.delete_conversation(conversation_id, current_user.id)
    return None


@router.get("/conversations/{conversation_id}/messages", response_model=dict)
async def get_messages(
    conversation_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ChatService(db)
    return service.get_messages(conversation_id, current_user.id, page, size)