from datetime import datetime

from app.models.audit_log import AuditLog
from app.models.event_contribution import EventContribution
from app.models.transaction import Transaction
from app.models.user import User
from app.models.welfare_event import WelfareEvent

async def create_welfare_event(event_data, created_by):
    affected_member = await User.get(event_data.affected_member_id)
    if affected_member is None:
        raise ValueError("Affected member not found")

    event = WelfareEvent(
        event_type=event_data.event_type,
        title=event_data.title,
        description=event_data.description,
        affected_member=affected_member,
        amount_per_member=event_data.amount_per_member,
        deadline=event_data.deadline,
        created_by=created_by,
    )
    await event.insert()

    members = await User.find(User.status == "Active").to_list()
    for member in members:
        contrib = EventContribution(
            welfare_event=event.id,
            member=member.id,
            amount_due=event.amount_per_member,
        )
        await contrib.insert()

    await AuditLog(
        action="create_welfare_event",
        entity_type="WelfareEvent",
        entity_id=str(event.id),
        performed_by=created_by,
        details={"title": event.title, "amount_per_member": event.amount_per_member},
    ).insert()
    return event

async def get_active_events():
    return await WelfareEvent.find(WelfareEvent.status == "Active").to_list()

async def get_member_contributions(member):
    return await EventContribution.find(EventContribution.member.id == member.id).to_list()

async def pay_contribution(contribution_id: str, amount: float, mpesa_receipt: str, payer):
    contribution = await EventContribution.get(contribution_id)
    if not contribution:
        raise ValueError("Contribution not found")
    if contribution.status == "Paid":
        raise ValueError("Contribution is already paid")
    if amount < contribution.amount_due:
        raise ValueError("Payment amount is less than amount due")

    contribution.amount_paid = amount
    contribution.payment_date = datetime.utcnow()
    contribution.status = "Paid"
    contribution.mpesa_receipt = mpesa_receipt
    await contribution.save()

    await Transaction(
        type="WelfareContribution",
        amount=amount,
        member=payer,
        reference_id=str(contribution.id),
        description=f"Payment for welfare contribution {contribution.id}",
        created_by=payer,
    ).insert()

    await AuditLog(
        action="pay_contribution",
        entity_type="EventContribution",
        entity_id=str(contribution.id),
        performed_by=payer,
        details={"amount": amount, "receipt": mpesa_receipt},
    ).insert()
    return contribution