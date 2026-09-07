# filepath: app/api/deps.py
"""Reusable FastAPI dependencies."""

from typing import Iterator


def get_session_dep() -> Iterator:
    """Yield a SQLModel Session for request scope. Placeholder."""
    raise NotImplementedError


def get_item_service_dep():
    """Construct an ItemService for request scope. Placeholder."""
    raise NotImplementedError