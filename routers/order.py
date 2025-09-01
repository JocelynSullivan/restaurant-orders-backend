from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import Order, OrderItem, MenuItems, Customer
from schemas import CreateMenuItemRequest, CreateOrderRequest, UpdateStatusRequest

router = APIRouter()

### GET ###

@router.get("/orders")
async def get_orders(db: Session = Depends(get_db)) -> list[dict]:
    statement = (
        select(Order, OrderItem, MenuItems, Customer)
        .join(OrderItem, OrderItem.id == Order.id)
        .join(MenuItems, MenuItems.id == OrderItem.menu_item_id)
        .join(Customer, Customer.id == Order.customer_id)
    )

    results = db.exec(statement).all()

    orders: dict[int, dict] = {}
    for order, item, menu, customer in results:
        if order.id not in orders:
            orders[order.id] = {
                "id": order.id,
                "customer": customer.name,
                "status": order.status,
                "order_date": order.order_date,
                "items": []
            }
        orders[order.id]["items"].append({
            "id": item.id,
            "quantity": item.quantity,
            "menu_item": {
                "id": menu.id,
                "name": customer.name,
                "price": menu.price,
            }    
        })
    return list(orders.values())


@router.get("/orders/{id}")
async def get_order(id: int, db: Session = Depends(get_db)) -> dict:
    statement = (
        select(Order, OrderItem, MenuItems, Customer)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .join(MenuItems, MenuItems.id == OrderItem.menu_item_id)
        .join(Customer, Customer.id == Order.customer_id)
        .where(Order.id == id)
    )

    results = db.exec(statement).all()
    
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} not found.")

    order_data = {
        "id": results[0][0].id,
        "customer": results[0][3].name,
        "status": results[0][0].status,
        "order_date": results[0][0].order_date,
        "items": []
    }

    for order, item, menu, customer in results:
        order_data["items"].append({
            "id": item.id,
            "quantity": item.quantity,
            "menu_item": {
                "id": menu.id,
                "name": menu.name,
                "price": menu.price
            }
        })
    return order_data

### POST ###

@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(create_order_request: CreateOrderRequest, db: Session = Depends(get_db)) -> Order:

    items: list[OrderItem] = []
    for i in create_order_request.items:
        menu: MenuItems | None = db.get(MenuItems, i.menu_item_id)
        if menu is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Menu item not found.")
        
        order_item: OrderItem = OrderItem(menu_item_id=i.menu_item_id, quantity=i.quantity)
        items.append(order_item)

    customer: Customer | None = db.get(Customer, create_order_request.customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {create_order_request.customer_id} not found.")

    order: Order = Order(customer=customer, items=items)

    db.add(order)
    db.commit()
    db.refresh(order)
    return order

### PATCH ###

@router.patch("/orders/{id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_order_status(id: int, order_status: UpdateStatusRequest, db: Session = Depends(get_db)) -> None:
    order: Order | None = db.get(Order, id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} not found.")
    
    order.status = order_status.status
    db.add(order)
    db.commit()
