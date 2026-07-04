from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.base import DocumentResponse

class WelfareEventCreate(BaseModel):
    event_type: str
    title: str
    description: Optional[str] = None
    affected_member_id: str
    amount_per_member: float
    deadline: datetime

class WelfareEventResponse(DocumentResponse):
    event_type: str
    title: str
    amount_per_member: float
    deadline: datetime
    status: str
    created_at: datetime

class EventContributionResponse(BaseModel):
    id: str
    amount_due: float
    amount_paid: float
    status: str
    payment_date: Optional[datetime] = None