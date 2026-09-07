# filepath: app/database.py
"""SQLite engine, session dependency, and table creation."""

from typing import Iterator


def get_engine():
    """Return the SQLAlchemy engine. Placeholder."""
    raise NotImplementedError


def create_db_and_tables() -> None:
    """Create database tables if they do not exist. Placeholder."""
    raise NotImplementedError


def get_session() -> Iterator:
    """FastAPI dependency yielding a SQLModel Session. Placeholder."""
    raise NotImplementedError