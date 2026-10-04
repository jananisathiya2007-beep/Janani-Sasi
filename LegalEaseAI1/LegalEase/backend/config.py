from functools import lru_cache
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Settings(BaseModel):
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-3.8-flash"))
    backend_url: str = Field(default_factory=lambda: os.getenv("BACKEND_URL", "http://127.0.0.1:8000"))
    app_env: str = Field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            x.strip() for x in os.getenv(
                "CORS_ORIGINS",
                "http://localhost:8501,http://127.0.0.1:8501"
            ).split(",") if x.strip()
        ]
    )
    max_document_chars: int = Field(
        default_factory=lambda: int(os.getenv("MAX_DOCUMENT_CHARS", "30000"))
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
