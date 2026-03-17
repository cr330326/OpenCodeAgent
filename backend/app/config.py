from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Multi-Agent Visualization Platform"
    APP_VERSION: str = "0.1.0"

    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/agent_viz"
    REDIS_URL: str = "redis://localhost:6379/0"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    CORS_ORIGINS: list = ["http://localhost:3000"]

    TRACE_RETENTION_DAYS: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
