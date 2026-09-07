# filepath: app/models/base.py
"""Shared SQLModel base utilities."""

from sqlmodel import SQLModel


class TimestampMixin(SQLModel):
    """Optional mixin for created_at/updated_at. Not used by Item v1."""

    pass