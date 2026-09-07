# filepath: app/core/pagination.py
"""Pagination helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    """Immutable pagination descriptor."""

    skip: int = 0
    limit: int = 50

    def clamp(self, *, max_limit: int = 100) -> "Page":
        """Return a Page with skip ≥ 0 and 1 ≤ limit ≤ max_limit."""
        raise NotImplementedError