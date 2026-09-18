from app.api import auth, universities, programmes, comparison, eligibility, chat, search, admin
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(universities.router)
api_router.include_router(programmes.router)
api_router.include_router(comparison.router)
api_router.include_router(eligibility.router)
api_router.include_router(chat.router)
api_router.include_router(search.router)
api_router.include_router(admin.router)