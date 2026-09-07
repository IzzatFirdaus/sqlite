# filepath: app/api/v1/endpoints/items.py
"""HTTP routes for Item CRUD."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status

router = APIRouter()


@router.post("/", response_model=object, status_code=status.HTTP_201_CREATED)
def create_item(payload, service=Depends()):
    """Create a new item."""
    raise NotImplementedError


@router.get("/", response_model=List[object])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    is_available: Optional[bool] = None,
    service=Depends(),
):
    """List items with pagination and optional filter."""
    raise NotImplementedError


@router.get("/{item_id}", response_model=object)
def get_item(item_id: int, service=Depends()):
    """Read a single item."""
    raise NotImplementedError


@router.put("/{item_id}", response_model=object)
def replace_item(item_id: int, payload, service=Depends()):
    """Replace an item fully."""
    raise NotImplementedError


@router.patch("/{item_id}", response_model=object)
def patch_item(item_id: int, payload, service=Depends()):
    """Patch an item partially."""
    raise NotImplementedError


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service=Depends()):
    """Delete an item."""
    raise NotImplementedError