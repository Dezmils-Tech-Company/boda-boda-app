from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class LoanApplication(BaseModel):
    amount: float
    tenure_months: int
    purpose: str
    guarantor_ids: List[str]

class EligibilityResponse(BaseModel):
    score: int
    max_loan_amount: float
    eligible: bool
    breakdown: dict

class LoanResponse(BaseModel):
    id: str
    amount: float
    status: str
    monthly_installment: float
    disbursement_date: Optional[datetime] = None