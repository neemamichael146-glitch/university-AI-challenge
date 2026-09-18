import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Import your FastAPI instance directly from app/main.py
from app.main import app

# 1. Allow all host headers to fix 400 Bad Request on Render health checks
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]
)

# 2. Allow CORS requests from your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    from app.core.config import settings
    # Point Uvicorn to 'app.main:app' so it matches the directory structure
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)