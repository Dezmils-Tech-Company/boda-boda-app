from datetime import datetime, timedelta
from typing import List

from loguru import logger

from app.models.audit_log import AuditLog
from app.models.loan import Loan
from app.models.subscription_payment import SubscriptionPayment
from app.models.user import User
from app.services.asset_service import create_member_asset
from app.services.notification_service import send_notification
from app.utils.eligibility_scorer import EligibilityScorer

scorer = EligibilityScorer()


async def _has_clean_loan_history(member: User) -> bool:
    loans = await Loan.find(Loan.member.id == member.id).to_list()
    return all(loan.status in ["Paid", "Closed"] for loan in loans)


async def calculate_eligibility(member: User):
    """Calculate loan eligibility using enhanced scorer"""
    try:
        # Get score from enhanced scorer
        score = scorer.calculate(member)
        breakdown = scorer.get_breakdown(member)

        max_loan_amount = breakdown["max_loan_suggestion"]
        eligible = score >= 60  # Minimum score threshold

        return {
            "score": score,
            "max_loan_amount": max_loan_amount,
            "eligible": eligible,
            "breakdown": breakdown,
        }
    except Exception as e:
        logger.error(f"Error calculating eligibility for member {getattr(member, 'id', 'unknown')}: {e}")
        # Fallback to original logic if new system fails
        return await _calculate_eligibility_fallback(member)


async def _calculate_eligibility_fallback(member: User):
    """Fallback to original eligibility calculation"""
    paid_subscriptions = await SubscriptionPayment.find(
        SubscriptionPayment.member.id == member.id,
        SubscriptionPayment.status == "Paid",
    ).to_list()

    paid_months = len(paid_subscriptions)
    base_score = scorer.calculate(member)  # This will use enhanced scorer but with placeholder values
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
    if loan_data.collateral_assets:
        for asset_data in loan_data.collateral_assets:
            await create_member_asset(member, asset_data)

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
        **loan_data.dict(exclude={"guarantor_ids", "collateral_assets"}),
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


async def approve_loan(loan_id: str, approver: User):
    loan = await Loan.get(loan_id)
    if loan is None:
        raise ValueError("Loan not found")

    if loan.status != "Pending":
        raise ValueError("Only pending loans can be approved")

    if approver.role == "Treasurer":
        loan.treasurer_approved = True
    elif approver.role == "Secretary":
        loan.secretary_approved = True
    elif approver.role == "Chairperson":
        loan.chairperson_approved = True
    else:
        raise ValueError("Only Treasurer, Secretary, or Chairperson can approve loans")

    await loan.save()
    await AuditLog(
        action="approve_loan",
        entity_type="Loan",
        entity_id=str(loan.id),
        performed_by=approver,
        details={
            "treasurer_approved": loan.treasurer_approved,
            "secretary_approved": loan.secretary_approved,
            "chairperson_approved": loan.chairperson_approved,
        },
    ).insert()

    if loan.treasurer_approved and loan.secretary_approved and loan.chairperson_approved:
        loan.status = "Approved"
        loan.disbursement_date = datetime.utcnow()
        await loan.save()
        try:
            await send_notification(
                phone=loan.member.phone,
                message=(
                    f"Your loan application for KES {loan.amount:.2f} has been approved by the treasurer, secretary, and chairperson."
                ),
            )
        except Exception as exc:
            logger.error("Failed to send loan approval notification", error=str(exc), loan_id=str(loan.id))

    return loan