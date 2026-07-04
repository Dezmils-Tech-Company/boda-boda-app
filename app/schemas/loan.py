from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import List, Optional
from app.schemas.base import DocumentResponse

class CollateralAssetCreate(BaseModel):
    asset_type: str
    description: str
    quantity: int = Field(gt=0)
    unit_value: float = Field(gt=0)
    total_value: float = 0.0

    @model_validator(mode="after")
    def compute_total_value(self):
        self.total_value = round(self.quantity * self.unit_value, 2)
        return self

class LoanApplication(BaseModel):
    amount: float = Field(gt=0)
    tenure_months: int = Field(gt=0)
    purpose: str
    guarantor_ids: List[str] = Field(default_factory=list)
    interest_rate: float = Field(default=1.5, ge=0)
    collateral_assets: List[CollateralAssetCreate] = Field(default_factory=list)

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
    treasurer_approved: bool
    secretary_approved: bool
    chairperson_approved: bool