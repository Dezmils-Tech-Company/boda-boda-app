from beanie import Document
from datetime import datetime
from typing import List, Optional

class InventoryItem(Document):
    name: str
    category: str
    total_quantity: int
    available_quantity: int
    daily_rate: float
    deposit_rate: float
    photos: List[str] = []
    condition: str = "Good"
    location: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "inventory_items"