from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import Order, OrderItem, MenuItem, Customer
from schemas import CreateMenuItemRequest, CreateOrderRequest

router = APIRouter()

### GET ###

# @router.get("/orders")
# async def get_orders(db: Session = Depends(get_db)) -> list[dict]:


@router.get("/order_items/{order_items}")
async def get_order_items(order_items: str, db: Session = Depends(get_db)) -> list [OrderItem]:
    for item in order_items:
        if item.id == order_items.id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {order_items.id} not found.")

### POST ###

@router.post("/orders")
async def create_order(create_order_request: CreateOrderRequest) -> Order:
    order: Order = Order(**create_order_request.model_dump())
    return order

### DELETE ###