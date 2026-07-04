from fastapi import APIRouter, Depends, HTTPException
from app.schemas.loan import CollateralAssetCreate, LoanApplication, EligibilityResponse, LoanResponse
from app.services.asset_service import create_member_asset
from app.services.loan_service import calculate_eligibility, create_loan, approve_loan
from app.core.security import get_current_user, require_loan_official

router = APIRouter()

@router.get("/eligibility", response_model=EligibilityResponse)
async def get_eligibility(current_user=Depends(get_current_user)):
    return await calculate_eligibility(current_user)

@router.post("/assets")
async def post_collateral_asset(asset_data: CollateralAssetCreate, current_user=Depends(get_current_user)):
    asset = await create_member_asset(current_user, asset_data)
    return {
        "status": "success",
        "message": "Collateral asset recorded for eligibility scoring",
        "data": {
            "id": str(asset.id),
            "asset_type": asset.asset_type,
            "description": asset.description,
            "quantity": asset.quantity,
            "unit_value": asset.unit_value,
            "total_value": asset.total_value,
            "status": asset.status,
        },
    }

@router.post("/apply", response_model=LoanResponse)
async def apply_for_loan(loan_data: LoanApplication, current_user=Depends(get_current_user)):
    return await create_loan(loan_data, current_user)

@router.post("/{loan_id}/approve", response_model=LoanResponse)
async def approve_loan_application(loan_id: str, current_user=Depends(require_loan_official)):
    try:
        return await approve_loan(loan_id, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
