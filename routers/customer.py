from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_db
from models import Customer
from schemas import CreateCustomerRequest

router = APIRouter()

### GET ###

@router.get("/customers")
async def get_customers(db: Session = Depends(get_db)) -> list[Customer]:
    return db.exec(select(Customer)).all()

@router.get("/customers/{id}")
async def get_customer(db: Session = Depends(get_db)) -> Customer:
    customer: Customer | None = db.get(Customer, id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {id} not found.")
    return customer

### POST ###

@router.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(create_customer_request: CreateCustomerRequest, db: Session = Depends(get_db)) -> Customer:
    customer: Customer = Customer(name=create_customer_request.name)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer.id

### DELETE ###

@router.delete("/customer/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
    customer: Customer | None = db.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {customer_id} not found.")

    db.delete(customer)
    db.commit()