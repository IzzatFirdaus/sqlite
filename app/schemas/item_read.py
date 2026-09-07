# filepath: app/schemas/item_read.py
"""ItemRead DTO returned by all item endpoints."""

from app.models.item import ItemBase


class ItemRead(ItemBase):
    """Response shape for Item."""

    id: int