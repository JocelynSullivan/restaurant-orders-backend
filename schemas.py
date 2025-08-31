from pydantic import BaseModel


class GetMenuItemsResponse(BaseModel):
    item: str
    price: float

class GetRevenuePerDay(BaseModel):
    date: str
    total_revenue: float

class GetBestSellingItem(BaseModel):
    menu_item_id: int
    item: str
    quantity: int

class GetOrdersPerCustomer(BaseModel):
    customer_id: int
    name: str
    quantity: int

class CreateMenuItemRequest(BaseModel):
    item: str
    price: float
    calories: int

class CreateCustomerRequest(BaseModel):
    name: str

class CreateOrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int = 1

class CreateOrderRequest(BaseModel):
    customer_id: int
    items: list[CreateOrderItemRequest]

class UpdateMenuItemRequest(BaseModel):
    item: str
    price: float
    calories: int

class UpdateStatusRequest(BaseModel):
    status: str