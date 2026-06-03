from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://aiops:aiops@localhost:5432/aiops"
    REDIS_URL: str = "redis://localhost:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672//"
    SECRET_KEY: str = "super-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    GOOGLE_AI_STUDIO_API_KEY: str = ""
    GOOGLE_AI_STUDIO_MODEL: str = "gemini-1.5-flash"

    # Backward-compat (optional): keep old field but do not use it by default.
    OPENAI_API_KEY: str = ""

    CORS_ORIGINS: List[str] = ["*"]
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()