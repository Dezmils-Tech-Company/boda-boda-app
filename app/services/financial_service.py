from app.models.transaction import Transaction
from app.models.user import User

async def get_group_summary():
    total_transactions = await Transaction.all().to_list()
    total_income = sum(t.amount for t in total_transactions if t.amount > 0)
    return {"total_income": total_income}

async def get_member_financials(member_id):
    transactions = await Transaction.find(Transaction.member.id == member_id).to_list()
    return {"transactions": transactions}