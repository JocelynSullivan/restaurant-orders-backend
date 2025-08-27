from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from database import get_db
from sqlalchemy import func

from models import Order, OrderItem, MenuItem, Customer


router = APIRouter()

