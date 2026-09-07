# filepath: app/models/item.py
"""Item SQLModel table definition."""

from typing import Optional

from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    """Shared fields for Item DTOs."""

    name: str = Field(index=True)
    description: Optional[str] = None
    price: float
    is_available: bool = True


class Item(ItemBase, table=True):
    """Item table model."""

    id: Optional[int] = Field(default=None, primary_key=True)