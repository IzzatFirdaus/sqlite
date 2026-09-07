# filepath: tests/conftest.py
"""Pytest fixtures: ephemeral SQLite, TestClient."""

import pytest


@pytest.fixture
def test_engine():
    """Yield an in-memory SQLite engine for tests."""
    raise NotImplementedError


@pytest.fixture
def client(test_engine):
    """Yield a FastAPI TestClient wired to the test engine."""
    raise NotImplementedError