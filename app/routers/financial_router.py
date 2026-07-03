from fastapi import APIRouter, Depends
from app.schemas.financial import GroupFinancialSummary, MemberFinancialSummary
from app.services.financial_service import get_group_summary, get_member_financials
from app.core.security import get_current_user, require_admin

router = APIRouter()

@router.get("/group", response_model=GroupFinancialSummary)
async def group_financials(current_user=Depends(require_admin)):
    return await get_group_summary()

@router.get("/me", response_model=MemberFinancialSummary)
async def my_financials(current_user=Depends(get_current_user)):
    return await get_member_financials(current_user.id)