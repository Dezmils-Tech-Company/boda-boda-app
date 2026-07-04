from beanie import Document, Link
from pydantic import Field
from datetime import datetime
from typing import Optional
from app.models.user import User

class Asset(Document):
    """Model to track member assets for collateral and wealth assessment"""
    member: Link[User]
    asset_type: str  # livestock, equipment, business, land, etc.
    description: str
    quantity: int
    unit_value: float  # Estimated market value per unit
    total_value: float  # Computed: quantity * unit_value
    acquisition_date: datetime
    status: str = "Active"  # Active, Sold, Disposed
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "assets"