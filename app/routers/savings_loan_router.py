from fastapi import APIRouter, Depends, HTTPException
from app.schemas.loan import CollateralAssetCreate, LoanApplication, EligibilityResponse, LoanResponse
from app.services.asset_service import create_member_asset
from app.services.loan_service import calculate_eligibility, create_loan, approve_loan
from app.services.savings_service import record_savings_deposit, get_member_savings_balance, get_member_savings_transactions
from app.models.user import User
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
    try:
        return await create_loan(loan_data, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.post("/{loan_id}/approve", response_model=LoanResponse)
async def approve_loan_application(loan_id: str, current_user=Depends(require_loan_official)):
    try:
        return await approve_loan(loan_id, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/savings/deposit")
async def deposit_savings(
    amount: float,
    description: str,
    current_user: User = Depends(get_current_user)
):
    """
    Record a savings deposit for the current user.

    Args:
        amount: The amount to deposit (must be positive)
        description: Description of the deposit
        current_user: The authenticated user making the deposit

    Returns:
        Success message with transaction details
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Savings deposit amount must be positive")

    try:
        transaction = await record_savings_deposit(
            amount=amount,
            description=description,
            member=current_user,
            created_by=current_user
        )

        return {
            "status": "success",
            "message": "Savings deposit recorded successfully",
            "data": {
                "id": str(transaction.id),
                "amount": transaction.amount,
                "description": transaction.description,
                "created_at": transaction.created_at
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record savings deposit: {str(e)}")


@router.get("/savings/balance")
async def get_savings_balance(current_user: User = Depends(get_current_user)):
    """
    Get the current savings balance for the authenticated user.

    Args:
        current_user: The authenticated user

    Returns:
        Savings balance information
    """
    try:
        balance_info = await get_member_savings_balance(str(current_user.id))
        return {
            "status": "success",
            "message": "Savings balance retrieved successfully",
            "data": balance_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve savings balance: {str(e)}")


@router.get("/savings/transactions")
async def get_savings_transactions(
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """
    Get savings transaction history for the authenticated user.

    Args:
        limit: Maximum number of transactions to return (default: 100)
        current_user: The authenticated user

    Returns:
        List of savings transactions
    """
    try:
        transactions = await get_member_savings_transactions(
            member_id=str(current_user.id),
            limit=limit
        )

        return {
            "status": "success",
            "message": "Savings transactions retrieved successfully",
            "data": {
                "transactions": transactions,
                "count": len(transactions)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve savings transactions: {str(e)}")