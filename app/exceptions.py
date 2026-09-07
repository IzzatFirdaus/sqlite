# filepath: app/exceptions.py
"""Domain exceptions and FastAPI handlers."""


class ItemNotFoundError(Exception):
    """Raised when an Item cannot be located by id."""

    def __init__(self, item_id: int) -> None:
        self.item_id = item_id
        super().__init__(f"Item {item_id} not found")


def register_exception_handlers(app) -> None:
    """Attach exception handlers to a FastAPI app. Placeholder."""
    raise NotImplementedError