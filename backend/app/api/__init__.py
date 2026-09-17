from app.api import auth, universities, programmes, comparison, eligibility, chat, search, admin
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/api")
api_router.include_router(universities.router, prefix="/api")
api_router.include_router(programmes.router, prefix="/api")
api_router.include_router(comparison.router, prefix="/api")
api_router.include_router(eligibility.router, prefix="/api")
api_router.include_router(chat.router, prefix="/api")
api_router.include_router(search.router, prefix="/api")
api_router.include_router(admin.router, prefix="/api")