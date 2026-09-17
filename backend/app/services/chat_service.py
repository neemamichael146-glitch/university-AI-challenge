from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.exceptions import NotFoundException
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.schemas.chat import ConversationCreate, ConversationUpdate, ChatRequest, ChatResponse
from app.ai.router import AIModelRouter


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_router = AIModelRouter()

    def create_conversation(self, user_id: str, conversation_data: ConversationCreate) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            title=conversation_data.title,
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: str, user_id: str) -> Conversation:
        conversation = (
            self.db.query(Conversation)
            .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
            .first()
        )
        if not conversation:
            raise NotFoundException("Conversation", conversation_id)
        return conversation

    def get_conversations(
        self,
        user_id: str,
        page: int = 1,
        size: int = 20,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        query = self.db.query(Conversation).filter(Conversation.user_id == user_id)

        if status:
            query = query.filter(Conversation.status == status)

        total = query.count()
        conversations = query.order_by(Conversation.updated_at.desc()).offset((page - 1) * size).limit(size).all()

        return {
            "conversations": conversations,
            "total": total,
            "page": page,
            "size": size,
        }

    def update_conversation(
        self,
        conversation_id: str,
        user_id: str,
        conversation_data: ConversationUpdate,
    ) -> Conversation:
        conversation = self.get_conversation(conversation_id, user_id)

        update_data = conversation_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)

        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        conversation = self.get_conversation(conversation_id, user_id)
        self.db.delete(conversation)
        self.db.commit()
        return True

    async def send_message(self, user_id: str, chat_request: ChatRequest) -> ChatResponse:
        if chat_request.conversation_id:
            conversation = self.get_conversation(chat_request.conversation_id, user_id)
        else:
            conversation = self.create_conversation(user_id, ConversationCreate())

        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=chat_request.message,
        )
        self.db.add(user_message)
        self.db.commit()

        messages = self.db.query(Message).filter(Message.conversation_id == conversation.id).order_by(Message.created_at).all()
        message_history = [{"role": m.role.value, "content": m.content} for m in messages]

        ai_response = await self.ai_router.generate_response(
            messages=message_history,
            context=chat_request.context,
        )

        assistant_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=ai_response["message"],
            tokens_used=ai_response.get("tokens_used"),
            model_used=ai_response.get("model"),
            metadata=str(ai_response.get("sources", [])),
        )
        self.db.add(assistant_message)

        conversation.updated_at = func.now()
        self.db.commit()

        return ChatResponse(
            message=ai_response["message"],
            conversation_id=conversation.id,
            tokens_used=ai_response.get("tokens_used"),
            model_used=ai_response.get("model"),
            sources=ai_response.get("sources"),
        )

    def get_messages(
        self,
        conversation_id: str,
        user_id: str,
        page: int = 1,
        size: int = 50,
    ) -> Dict[str, Any]:
        conversation = self.get_conversation(conversation_id, user_id)

        query = self.db.query(Message).filter(Message.conversation_id == conversation.id)
        total = query.count()
        messages = query.order_by(Message.created_at).offset((page - 1) * size).limit(size).all()

        return {
            "messages": messages,
            "total": total,
            "page": page,
            "size": size,
        }