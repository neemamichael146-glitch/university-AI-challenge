from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.core.exceptions import UnauthorizedException, ConflictException, ValidationException
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, TokenResponse, RefreshTokenRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, user_data: UserCreate) -> TokenResponse:
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ConflictException("Email already registered")

        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role or "student",
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return self._create_tokens(user)

    def login(self, credentials: UserLogin) -> TokenResponse:
        user = self.db.query(User).filter(User.email == credentials.email).first()
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is deactivated")

        return self._create_tokens(user)

    def refresh_token(self, request: RefreshTokenRequest) -> TokenResponse:
        payload = verify_token(request.refresh_token, "refresh")
        if not payload:
            raise UnauthorizedException("Invalid or expired refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid token payload")

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive")

        return self._create_tokens(user)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def _create_tokens(self, user: User) -> TokenResponse:
        access_token = create_access_token(data={"sub": user.id, "email": user.email, "role": user.role})
        refresh_token = create_refresh_token(data={"sub": user.id})
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,
        )