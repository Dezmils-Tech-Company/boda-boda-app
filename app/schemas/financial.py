from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class TransactionResponse(BaseModel):
    id: str
    type: str
    amount: float
    description: str
    created_at: datetime

class GroupFinancialSummary(BaseModel):
    total_balance: float
    total_income: float
    total_expenses: float
    active_loans: int

class MemberFinancialSummary(BaseModel):
    current_savings: float
    total_contributed: float
    active_loans: List[dict]
    transactions: List[TransactionResponse]