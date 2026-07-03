from datetime import datetime, timedelta
from typing import List

from app.models.audit_log import AuditLog
from app.models.loan import Loan
from app.models.subscription_payment import SubscriptionPayment
from app.models.user import User
from app.utils.eligibility_scorer import EligibilityScorer

scorer = EligibilityScorer()

async def _has_clean_loan_history(member: User) -> bool:
    loans = await Loan.find(Loan.member.id == member.id).to_list()
    return all(loan.status in ["Paid", "Closed"] for loan in loans)

async def calculate_eligibility(member: User):
    paid_subscriptions = await SubscriptionPayment.find(
        SubscriptionPayment.member.id == member.id,
        SubscriptionPayment.status == "Paid",
    ).to_list()

    paid_months = len(paid_subscriptions)
    base_score = scorer.calculate(member)
    breakdown = {
        "subscription_history": min(paid_months, 12) * 3,
        "repayment_behavior": 25 if await _has_clean_loan_history(member) else 10,
        "boda_specific": 20 if getattr(member, "id_number", None) else 10,
        "participation": 10 if (datetime.utcnow() - member.join_date).days >= 90 else 5,
        "longevity_bonus": 5 if (datetime.utcnow() - member.join_date).days >= 365 else 0,
    }
    total = min(int(base_score + sum(breakdown.values())), 100)
    max_loan_amount = total * 700
    return {
        "score": total,
        "max_loan_amount": max_loan_amount,
        "eligible": total >= 60,
        "breakdown": breakdown,
    }

async def create_loan(loan_data, member):
    eligibility = await calculate_eligibility(member)
    if not eligibility["eligible"]:
        raise ValueError("Not eligible for loan")

    guarantors: List[User] = []
    for guarantor_id in loan_data.guarantor_ids:
        guarantor = await User.get(guarantor_id)
        if guarantor is None:
            raise ValueError(f"Guarantor {guarantor_id} not found")
        guarantors.append(guarantor)

    total_amount = loan_data.amount * (1 + loan_data.interest_rate / 100)
    monthly_installment = round(total_amount / loan_data.tenure_months, 2)
    repayment_schedule = []
    for month_index in range(1, loan_data.tenure_months + 1):
        due_date = datetime.utcnow() + timedelta(days=30 * month_index)
        repayment_schedule.append({
            "due_date": due_date,
            "amount": monthly_installment,
            "paid": False,
            "payment_date": None,
        })

    loan = Loan(
        **loan_data.dict(exclude={"guarantor_ids"}),
        member=member,
        guarantors=guarantors,
        monthly_installment=monthly_installment,
        repayment_schedule=repayment_schedule,
        status="Pending",
    )
    await loan.insert()
    await AuditLog(
        action="create_loan",
        entity_type="Loan",
        entity_id=str(loan.id),
        performed_by=member,
        details={"amount": loan.amount, "tenure_months": loan.tenure_months},
    ).insert()
    return loan