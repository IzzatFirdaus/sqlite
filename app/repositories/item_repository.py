# filepath: app/repositories/item_repository.py
"""CRUD operations on the Item table. No business rules, no HTTP types."""

from typing import List, Optional


class ItemRepository:
    """Repository facade over SQLModel Session operations."""

    def __init__(self, session) -> None:
        self._session = session

    def create(self, item) -> object:
        """Insert a new Item row."""
        raise NotImplementedError

    def get(self, item_id: int):
        """Return a single Item by id or None."""
        raise NotImplementedError

    def list(self, *, skip: int = 0, limit: int = 50, is_available: Optional[bool] = None) -> List[object]:
        """Return a paginated list of Items."""
        raise NotImplementedError

    def replace(self, item_id: int, item) -> object:
        """Fully replace an Item by id. Raise if missing."""
        raise NotImplementedError

    def patch(self, item_id: int, updates: dict) -> object:
        """Partially update an Item by id. Raise if missing."""
        raise NotImplementedError

    def delete(self, item_id: int) -> None:
        """Delete an Item by id. Raise if missing."""
        raise NotImplementedError