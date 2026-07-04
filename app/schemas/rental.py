from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from app.schemas.base import DocumentResponse

class BookingItem(BaseModel):
    item_id: str
    quantity: int

class BookingItemResponse(BaseModel):
    item_id: str
    quantity: int

class InventoryItemCreate(BaseModel):
    name: str
    category: str
    total_quantity: int
    available_quantity: int
    daily_rate: float
    deposit_rate: float
    photos: Optional[List[str]] = []
    condition: Optional[str] = "Good"
    location: Optional[str] = None

class InventoryItemResponse(DocumentResponse):
    name: str
    category: str
    total_quantity: int
    available_quantity: int
    daily_rate: float
    deposit_rate: float
    photos: List[str] = []
    condition: str
    location: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class RentalBookingCreate(BaseModel):
    items: List[BookingItem]
    start_date: datetime
    end_date: datetime

class RentalBookingResponse(DocumentResponse):
    status: str
    total_amount: float
    items: List[BookingItemResponse]
    start_date: datetime
    end_date: datetime
    deposit_paid: float
    created_at: datetime

    class Config:
        from_attributes = True