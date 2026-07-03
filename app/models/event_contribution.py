from beanie import Document, Link
from datetime import datetime
from typing import Optional

class EventContribution(Document):
    welfare_event: Link["WelfareEvent"]
    member: Link["User"]
    amount_due: float
    amount_paid: float = 0.0
    status: str = "Pending"
    payment_date: Optional[datetime] = None
    mpesa_receipt: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "event_contributions"