# filepath: app/schemas/item_update.py
"""ItemUpdate DTO for PATCH /items/{id}."""

from typing import Optional

from sqlmodel import Field, SQLModel


class ItemUpdate(SQLModel):
    """Partial-update payload. None means 'do not change'."""

    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    is_available: Optional[bool] = Field(default=None)