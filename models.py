from sqlmodel import Field, Relationship, SQLModel 

class OrderLinkingTable(SQLModel, table=True):
    orderitem_id: int | None = Field(foreign_key="orderitem.id", primary_key=True)
    order_id: int | None = Field(foreign_key="order.id", primary_key=True)

class MenuItem(SQLModel, table=True):
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

class OrderItem(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    price: float
    orders: list["Order"] = Relationship(back_populates="items", link_model=OrderLinkingTable)
