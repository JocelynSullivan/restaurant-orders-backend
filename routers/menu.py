
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import MenuItem
from schemas import CreateMenuItemRequest

router = APIRouter()

### GET ###

@router.get("/menu_items")
async def get_menu_items(db: Session = Depends(get_db)) -> list[MenuItem]:
    return db.exec(select(MenuItem)).all()

@router.get("/menu_items/{items_id}")
async def get_menu_item(item_id: int, db: Session = Depends(get_db)) -> MenuItem:
    item: MenuItem | None = db.get(MenuItem, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {item_id} not found.")
    return item

### POST ###

@router.post("/menu_items", status_code=status.HTTP_201_CREATED)
async def create_menu_item(create_menu_item_request: CreateMenuItemRequest, db: Session = Depends(get_db)) -> MenuItem:
    menu_item: MenuItem = MenuItem(**create_menu_item_request.model_dump())
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    return menu_item.id

### DELETE ###

@router.delete("/menu_items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(item_id: int, db: Session = Depends(get_db)) -> None:
    menu_item: MenuItem | None = db.get(MenuItem, item_id)
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item with ID {item_id} not found.")

    db.delete(menu_item)
    db.commit()