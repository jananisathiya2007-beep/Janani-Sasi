from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import router

settings = get_settings()

app = FastAPI(
    title="LegalEase API",
    version="1.0.0",
    description="AI-powered legal document template generator.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "LegalEase API", "status": "ok", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "gemini_configured": bool(settings.gemini_api_key)}

app.include_router(router)
