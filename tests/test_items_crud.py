# filepath: tests/test_items_crud.py
"""End-to-end CRUD tests for the Item resource."""


def test_create_item_returns_201(client) -> None:
    """POST /items/ creates and persists an item."""
    raise NotImplementedError


def test_list_items_returns_array(client) -> None:
    """GET /items/ returns the persisted items."""
    raise NotImplementedError


def test_get_item_returns_200(client) -> None:
    """GET /items/{id} returns the requested item."""
    raise NotImplementedError


def test_get_missing_item_returns_404(client) -> None:
    """GET /items/{id} returns 404 when not found."""
    raise NotImplementedError


def test_patch_item_updates_fields(client) -> None:
    """PATCH /items/{id} updates only provided fields."""
    raise NotImplementedError


def test_put_item_replaces_fields(client) -> None:
    """PUT /items/{id} fully replaces the item."""
    raise NotImplementedError


def test_delete_item_returns_204(client) -> None:
    """DELETE /items/{id} removes the item."""
    raise NotImplementedError