# filepath: app/services/item_service.py
"""Business rules for the Item domain."""

from typing import List, Optional


class ItemService:
    """Orchestrates item operations through ItemRepository."""

    def __init__(self, repository) -> None:
        self._repo = repository

    def create_item(self, payload):
        """Validate business rules and create an item."""
        raise NotImplementedError

    def get_item(self, item_id: int):
        """Return an item or raise ItemNotFoundError."""
        raise NotImplementedError

    def list_items(self, *, skip: int = 0, limit: int = 50, is_available: Optional[bool] = None) -> List[object]:
        """List items honoring pagination and availability filters."""
        raise NotImplementedError

    def replace_item(self, item_id: int, payload):
        """Replace an item fully; raise ItemNotFoundError when missing."""
        raise NotImplementedError

    def patch_item(self, item_id: int, payload):
        """Patch an item partially; raise ItemNotFoundError when missing."""
        raise NotImplementedError

    def delete_item(self, item_id: int) -> None:
        """Delete an item; raise ItemNotFoundError when missing."""
        raise NotImplementedError