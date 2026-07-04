from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.schemas.base import DocumentResponse

class WelfareEventCreate(BaseModel):
    event_type: str
    title: str
    description: Optional[str] = None
    affected_member_id: str
    amount_per_member: float = Field(gt=0)
    deadline: datetime

class WelfareEventProposalCreate(BaseModel):
    event_type: str
    title: str
    description: Optional[str] = None
    proof_images: Optional[List[str]] = Field(default_factory=list)

class WelfareEventResponse(DocumentResponse):
    event_type: str
    title: str
    description: Optional[str] = None
    amount_per_member: Optional[float] = None
    deadline: Optional[datetime] = None
    proof_images: List[str] = Field(default_factory=list)
    status: str
    created_at: datetime

class EventContributionResponse(BaseModel):
    id: str
    amount_due: float
    amount_paid: float
    status: str
    payment_date: Optional[datetime] = None