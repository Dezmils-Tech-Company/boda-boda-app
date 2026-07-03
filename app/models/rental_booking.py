from beanie import Document, Link
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List

class BookingItem(BaseModel):
    item_id: str
    quantity: int

class RentalBooking(Document):
    member: Link["User"]
    items: List[BookingItem]
    start_date: datetime
    end_date: datetime
    total_amount: float
    deposit_paid: float = 0.0
    status: str = "Pending"
    condition_before: dict = Field(default_factory=dict)
    condition_after: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "rental_bookings"