# filepath: tests/test_items_validation.py
"""Validation-focused tests for Item endpoints."""


def test_missing_name_returns_422(client) -> None:
    """POST without name should be rejected with 422."""
    raise NotImplementedError


def test_negative_price_returns_422(client) -> None:
    """POST with negative price should be rejected with 422."""
    raise NotImplementedError


def test_invalid_limit_returns_422(client) -> None:
    """GET with limit > 100 should be rejected with 422."""
    raise NotImplementedError