import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://chuoai:chuoai@localhost:5433/chuoai"
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    JWT_SECRET: str = "your-jwt-secret-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-3.5-turbo"
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    MAX_UPLOAD_SIZE: int = 10485760
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".csv"]
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    TOP_K_RETRIEVAL: int = 5
    APP_NAME: str = "ChuoAI API"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()