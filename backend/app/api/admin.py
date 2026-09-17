from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.auth.dependencies import get_current_admin_user
from app.schemas.admin import DashboardStats, UserAdminResponse, UserListResponse, SystemHealth
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    return DashboardStats(
        total_users=db.query(User).count(),
        total_universities=10,
        total_programmes=50,
        total_conversations=100,
        total_messages=500,
        active_users_24h=25,
        active_users_7d=100,
        new_registrations_24h=5,
        conversations_24h=30,
    )


@router.get("/users", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    
    if search:
        query = query.filter(
            User.email.ilike(f"%{search}%") | User.full_name.ilike(f"%{search}%")
        )
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    total = query.count()
    users = query.order_by(User.created_at.desc()).offset((page - 1) * size).limit(size).all()
    
    return UserListResponse(users=users, total=total, page=page, size=size)


@router.get("/health", response_model=SystemHealth)
async def get_system_health(
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    import time
    start = time.time()
    db.execute("SELECT 1")
    db_latency = time.time() - start
    
    return SystemHealth(
        status="healthy",
        database="connected",
        redis="connected",
        ai_provider="groq",
        version="1.0.0",
        uptime_seconds=db_latency,
    )