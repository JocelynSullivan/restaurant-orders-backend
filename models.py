from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class OrderLinkingTable(SQLModel, table=True):
    orderitem_id: int | None = Field(foreign_key="orderitem.id", primary_key=True)
    order_id: int | None = Field(foreign_key="order.id", primary_key=True)

class MenuItems(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    item: str
    price: float
    calories: int

class Customer(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    orders: list["Order"] = Relationship(back_populates="customer")

class Order(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    items: list["OrderItem"] = Relationship(back_populates="orders", link_model=OrderLinkingTable)
    customer_id: int | None = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="orders")
    status: str = "pending"
    order_date: datetime = datetime.now()

class OrderItem(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    menu_item_id: int = Field(foreign_key="menuitems.id")
    menu_item: MenuItems = Relationship()
    quantity: int = 1
    orders: list["Order"] = Relationship(back_populates="items", link_model=OrderLinkingTable)
    order_id: int | None = Field(foreign_key="order.id")