from app.models.loan import Loan
from app.models.transaction import Transaction
from app.models.user import User

async def get_group_summary():
    total_transactions = await Transaction.all().to_list()
    total_income = sum(t.amount for t in total_transactions if t.amount > 0)
    total_expenses = sum(-t.amount for t in total_transactions if t.amount < 0)
    total_balance = total_income - total_expenses

    members = await User.all().to_list()
    members_savings_total = 0.0
    for member in members:
        member_transactions = [
            t for t in total_transactions if str(getattr(t.member, "id", None)) == str(member.id)
        ]
        member_contributed = sum(t.amount for t in member_transactions if t.amount > 0)
        member_withdrawn = sum(-t.amount for t in member_transactions if t.amount < 0)
        members_savings_total += max(member_contributed - member_withdrawn, 0.0)

    active_loans = await Loan.find({"status": {"$in": ["Pending", "Approved"]}}).to_list()
    return {
        "total_balance": total_balance,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "members_savings_total": members_savings_total,
        "active_loans": len(active_loans),
    }

async def get_member_financials(member_id):
    transactions = await Transaction.find({"member.$id": member_id}).to_list()
    active_loans = await Loan.find({"member.$id": member_id, "status": {"$in": ["Pending", "Approved"]}}).to_list()
    total_contributed = sum(t.amount for t in transactions if t.amount > 0)
    current_savings = total_contributed - sum(-t.amount for t in transactions if t.amount < 0)
    return {
        "current_savings": current_savings,
        "total_contributed": total_contributed,
        "active_loans": active_loans,
        "transactions": transactions,
    }