from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Defaults are container-friendly so docker-compose/k8s work out of the box
    DATABASE_URL: str = "postgresql+asyncpg://aiops:aiops@postgres:5432/aiops"
    REDIS_URL: str = "redis://redis:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672//"
    SECRET_KEY: str = "super-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    GOOGLE_API_KEY: str = ""                      # <-- THIS IS NEW
    CORS_ORIGINS: List[str] = ["*"]
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()