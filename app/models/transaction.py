from beanie import Document, Link
from datetime import datetime
from typing import Optional

class Transaction(Document):
    type: str
    amount: float
    member: Optional[Link["User"]] = None
    reference_id: Optional[str] = None
    description: str
    created_by: Link["User"]
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "transactions"