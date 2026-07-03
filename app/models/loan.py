from beanie import Document, Link
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class RepaymentItem(BaseModel):
    due_date: datetime
    amount: float
    paid: bool = False
    payment_date: Optional[datetime] = None

class Loan(Document):
    member: Link["User"]
    amount: float
    interest_rate: float
    tenure_months: int
    monthly_installment: float
    purpose: str
    guarantors: List[Link["User"]] = Field(default_factory=list)
    status: str = "Pending"
    disbursement_date: Optional[datetime] = None
    repayment_schedule: List[RepaymentItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "loans"