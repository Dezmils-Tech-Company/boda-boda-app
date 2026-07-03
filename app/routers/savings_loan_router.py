from fastapi import APIRouter, Depends, HTTPException
from app.schemas.loan import LoanApplication, EligibilityResponse, LoanResponse
from app.services.loan_service import calculate_eligibility, create_loan
from app.core.security import get_current_user

router = APIRouter()

@router.get("/eligibility", response_model=EligibilityResponse)
async def get_eligibility(current_user=Depends(get_current_user)):
    return await calculate_eligibility(current_user)

@router.post("/apply", response_model=LoanResponse)
async def apply_for_loan(loan_data: LoanApplication, current_user=Depends(get_current_user)):
    return await create_loan(loan_data, current_user)