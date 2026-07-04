from beanie import Document, Link
from datetime import datetime
from typing import List, Optional

class WelfareEvent(Document):
    event_type: str
    title: str
    description: Optional[str] = None
    affected_member: Link["User"]
    amount_per_member: Optional[float] = None
    deadline: Optional[datetime] = None
    proof_images: List[str] = []
    status: str = "Active"
    created_by: Link["User"]
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "welfare_events"