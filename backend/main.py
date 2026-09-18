import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# 1. Initialize FastAPI instance directly in backend/main.py
app = FastAPI(title="ChuoAI API")

# 2. Allow all host headers to fix Render 400 errors
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# 3. Configure CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Root & Health Check Endpoints
@app.get("/")
@app.head("/")
def read_root():
    return {"message": "ChuoAI API is live and running!"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    from app.core.config import settings
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)