from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.core.config import settings
from app.core.database import engine
from app.api import api_router
from app.utils.logger import setup_logging, logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting ChuoAI API...")
    # Base.metadata.create_all(bind=engine)  # Use Alembic migrations in production
    # logger.info("Database tables created")
    yield
    logger.info("Shutting down ChuoAI API...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Tanzania University & TCU AI Assistant API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["chuoai.com", "www.chuoai.com", "api.chuoai.com", "localhost", "127.0.0.1"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "ChuoAI API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)