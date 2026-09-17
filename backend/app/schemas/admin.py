from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DashboardStats(BaseModel):
    total_users: int
    total_universities: int
    total_programmes: int
    total_conversations: int
    total_messages: int
    active_users_24h: int
    active_users_7d: int
    new_registrations_24h: int
    conversations_24h: int


class UserAdminResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: List[UserAdminResponse]
    total: int
    page: int
    size: int


class SystemHealth(BaseModel):
    status: str
    database: str
    redis: str
    ai_provider: str
    version: str
    uptime_seconds: float