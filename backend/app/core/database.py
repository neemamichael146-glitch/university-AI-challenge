from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager
from typing import Generator
import os
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.core.config import settings

logger = logging.getLogger(__name__)


def init_pgvector_extension():
    """Initialize pgvector extension in PostgreSQL database.
    
    This runs BEFORE any models or ORMs initialize to ensure
    the vector extension is available for vector columns.
    """
    database_url = os.getenv("DATABASE_URL") or settings.DATABASE_URL
    
    if not database_url:
        logger.warning("DATABASE_URL not configured, skipping pgvector initialization")
        return
    
    # Convert SQLAlchemy URL format to psycopg2 format
    # postgresql+psycopg2:// -> postgresql://
    # postgresql:// -> postgresql:// (already correct)
    if database_url.startswith("postgresql+psycopg2://"):
        database_url = database_url.replace("postgresql+psycopg2://", "postgresql://", 1)
    elif database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    try:
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        conn.close()
        logger.info("pgvector extension initialized successfully")
        
    except psycopg2.OperationalError as e:
        logger.error(f"Failed to connect to database for pgvector initialization: {e}")
    except psycopg2.Error as e:
        logger.error(f"Failed to create pgvector extension: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during pgvector initialization: {e}")


# Initialize pgvector extension before creating engine
init_pgvector_extension()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=40,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()