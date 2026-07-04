from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from app.schemas.base import DocumentResponse

class TransactionResponse(DocumentResponse):
    type: str
    amount: float
    description: str
    created_at: datetime

class GroupFinancialSummary(BaseModel):
    total_balance: float
    total_income: float
    total_expenses: float
    members_savings_total: float
    active_loans: int

class MemberFinancialSummary(BaseModel):
    current_savings: float
    total_contributed: float
    active_loans: List[dict]
    transactions: List[TransactionResponse]