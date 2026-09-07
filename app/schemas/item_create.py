# filepath: app/schemas/item_create.py
"""ItemCreate DTO for POST /items/."""

from app.models.item import ItemBase


class ItemCreate(ItemBase):
    """Payload accepted by create endpoints."""

    pass