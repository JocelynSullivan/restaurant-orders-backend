from pydantic import BaseModel


class GetMenuItemsResponse(BaseModel):
    item: str
    price: float

class CreateMenuItemRequest(BaseModel):
    item: str
    price: float
    calories: int

class CreateCustomerRequest(BaseModel):
    name: str

class CreateOrderRequest(BaseModel):
    item: str
    name: str
    price: str

class UpdateMenuItemRequest(BaseModel):
    item: str
    price: float
    calories: int