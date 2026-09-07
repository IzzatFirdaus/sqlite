# filepath: app/config.py
"""Application configuration loaded from environment variables."""

from functools import lru_cache


@lru_cache(maxsize=1)
def get_settings() -> "Settings":
    """Return a cached Settings instance."""
    raise NotImplementedError


class Settings:
    """Placeholder settings container. Replace with pydantic-settings BaseSettings."""

    APP_NAME: str = "FastAPI + SQLite Persistence API"
    DATABASE_URL: str = "sqlite:///./database.db"
    SQL_ECHO: bool = False
    LOG_LEVEL: str = "INFO"
    CORS_ALLOW_ORIGINS: str = "*"