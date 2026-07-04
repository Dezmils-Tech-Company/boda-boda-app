from beanie import Document, Link
from datetime import datetime
from typing import Optional

class SubscriptionPayment(Document):
    member: Link["User"]
    month: int
    year: int
    amount: float
    status: str = "Pending"
    mpesa_receipt: Optional[str] = None
    payment_date: Optional[datetime] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "subscription_payments"