from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from database import get_db
from sqlalchemy import func

from models import Order, OrderItem, MenuItems, Customer
from schemas import GetRevenuePerDay, GetBestSellingItem, GetOrdersPerCustomer


router = APIRouter()

### Revenue Per Day ###

@router.get("/reports/revenue_per_day")
async def get_revenue_per_day(db: Session = Depends(get_db)) -> list[GetRevenuePerDay]:
    statement = (
        select(
            func.date(Order.order_date),
            func.sum(OrderItem.quantity * MenuItems.price)
        )
        .select_from(Order)
        .join(OrderItem, OrderItem.id == Order.id)
        .join(MenuItems, MenuItems.id == OrderItem.menu_item_id)
        .group_by(func.date(Order.order_date))
        .order_by(func.date(Order.order_date))
    )

    results = db.exec(statement).all()

    revenue_per_day: list[GetRevenuePerDay] = []

    for result in results:
        revenue_per_day.append(GetRevenuePerDay(date=str(result[0], total_revenue=float(result[1]))))

    return revenue_per_day

### Best Selling Menu Items ###

@router.get("/reports/best_selling_item")
async def get_best_selling_item(db: Session = Depends(get_db)) -> GetBestSellingItem:
    statement = (
        select(MenuItems, MenuItems.id, MenuItems.item, func.sum(OrderItem.quantity))
            .join(OrderItem, OrderItem.menu_item_id == MenuItems.id)
            .group_by(MenuItems.id, MenuItems.item)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(1)
    )

    result = db.exec(statement).all()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No sales data found.")
    
    return GetBestSellingItem(menu_item_id=result[0], item=result[1], quantity=result[2])


### Orders Per Customer ###

@router.get("/reports/orders_per_customer")
async def get_orders_per_customer(db: Session = Depends(get_db)):

    statement = (
        select(Customer.id, Customer.name, func.coalesce(func.sum(OrderItem.quantity), 0)
        )

        .select_from(Customer)
        .outerjoin(Order, Order.customer_id == Customer.id)
        .outerjoin(OrderItem, OrderItem.order_id == Order.id)
        .group_by(Customer.id, Customer.name)
        .order_by(func.coalesce(func.sum(OrderItem.quantity), 0).desc())
        )

    results = db.exec(statement).all()

    orders_per_customer: list[GetOrdersPerCustomer] = []

    for result in results:
        orders_per_customer.append(GetOrdersPerCustomer(customer_id=result[0], name=result[1], quantity=result[2]))

    return orders_per_customer