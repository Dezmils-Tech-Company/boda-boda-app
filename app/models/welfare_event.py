from beanie import Document, Link
from datetime import datetime
from typing import Optional

class WelfareEvent(Document):
    event_type: str
    title: str
    description: Optional[str] = None
    affected_member: Link["User"]
    amount_per_member: float
    deadline: datetime
    status: str = "Active"
    created_by: Link["User"]
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "welfare_events"