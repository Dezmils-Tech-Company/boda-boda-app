from datetime import datetime
from typing import List, Optional

from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionResponse


async def record_savings_deposit(amount: float, description: str, member: User, created_by: User) -> Transaction:
    """
    Record a savings deposit transaction.

    Args:
        amount: The amount to deposit (should be positive)
        description: Description of the deposit
        member: The member making the deposit
        created_by: The user creating the transaction record

    Returns:
        The created Transaction object
    """
    if amount <= 0:
        raise ValueError("Savings deposit amount must be positive")

    savings_transaction = Transaction(
        type="savings",
        amount=amount,
        description=description,
        member=member,
        created_by=created_by,
        created_at=datetime.utcnow()
    )

    await savings_transaction.insert()
    return savings_transaction


async def get_member_savings_balance(member_id: str) -> dict:
    """
    Calculate and return a member's savings balance.

    Args:
        member_id: The ID of the member

    Returns:
        Dictionary containing savings balance information
    """
    # Get all savings transactions for the member
    savings_transactions = await Transaction.find(
        {"member.$id": member_id, "type": "savings"}
    ).to_list()

    # Calculate total savings (sum of all savings transactions)
    total_savings = sum(t.amount for t in savings_transactions)

    return {
        "total_savings": total_savings,
        "savings_transactions_count": len(savings_transactions),
        "savings_transactions": [
            {
                "id": str(t.id),
                "amount": t.amount,
                "description": t.description,
                "created_at": t.created_at
            }
            for t in savings_transactions
        ]
    }


async def get_member_savings_transactions(member_id: str, limit: int = 100) -> List[TransactionResponse]:
    """
    Get a member's savings transactions.

    Args:
        member_id: The ID of the member
        limit: Maximum number of transactions to return

    Returns:
        List of savings transactions
    """
    transactions = await Transaction.find(
        {"member.$id": member_id, "type": "savings"}
    ).sort(-Transaction.created_at).limit(limit).to_list()

    return [TransactionResponse.from_mongo(t) for t in transactions]