from pydantic import BaseModel
from datetime import datetime
from typing import List

class BookingItem(BaseModel):
    item_id: str
    quantity: int

class RentalBookingCreate(BaseModel):
    items: List[BookingItem]
    start_date: datetime
    end_date: datetime

class RentalBookingResponse(BaseModel):
    id: str
    status: str
    total_amount: float
    start_date: datetime
    end_date: datetime