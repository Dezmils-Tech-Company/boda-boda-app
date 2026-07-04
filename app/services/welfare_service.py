from datetime import datetime

from loguru import logger

from app.models.audit_log import AuditLog
from app.models.event_contribution import EventContribution
from app.models.transaction import Transaction
from app.models.user import User
from app.models.welfare_event import WelfareEvent
from app.services.notification_service import send_notification
from app.services.upload_service import upload_image_to_cloudinary

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
        status="Active",
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

    notification_message = (
        f"New welfare event posted: {event.title}. "
        f"Contribution due: KES {event.amount_per_member:.2f}. "
        "Check the app for details."
    )
    for member in members:
        try:
            await send_notification(member.phone, notification_message)
        except Exception as exc:
            logger.error(
                "Failed to send welfare event notification",
                member_phone=member.phone,
                error=str(exc),
                event_id=str(event.id),
            )

    await AuditLog(
        action="create_welfare_event",
        entity_type="WelfareEvent",
        entity_id=str(event.id),
        performed_by=created_by,
        details={"title": event.title, "amount_per_member": event.amount_per_member},
    ).insert()
    return event

async def submit_welfare_proposal(event_data, submitted_by):
    affected_member = submitted_by

    proof_images = []
    for image in getattr(event_data, "proof_images", []) or []:
        if isinstance(image, str) and image.startswith(("http://", "https://")):
            proof_images.append(image)
            continue
        upload_result = await upload_image_to_cloudinary(image)
        proof_images.append(upload_result["secure_url"])

    proposal = WelfareEvent(
        event_type=event_data.event_type,
        title=event_data.title,
        description=event_data.description,
        affected_member=affected_member,
        amount_per_member=None,
        deadline=None,
        proof_images=proof_images,
        created_by=submitted_by,
        status="PendingApproval",
    )
    await proposal.insert()

    await AuditLog(
        action="submit_welfare_proposal",
        entity_type="WelfareEvent",
        entity_id=str(proposal.id),
        performed_by=submitted_by,
        details={"title": proposal.title, "proof_images": proposal.proof_images},
    ).insert()
    return proposal

async def approve_welfare_proposal(event_id: str, approved_by):
    proposal = await WelfareEvent.get(event_id)
    if proposal is None:
        raise ValueError("Welfare proposal not found")
    if proposal.status != "PendingApproval":
        raise ValueError("Only pending proposals can be approved")

    proposal.status = "Active"
    await proposal.save()

    members = await User.find(User.status == "Active").to_list()
    for member in members:
        contrib = EventContribution(
            welfare_event=proposal.id,
            member=member.id,
            amount_due=proposal.amount_per_member,
        )
        await contrib.insert()

    notification_message = (
        f"New welfare event posted: {proposal.title}. "
        f"Contribution due: KES {proposal.amount_per_member:.2f}. "
        "Check the app for details."
    )
    for member in members:
        try:
            await send_notification(member.phone, notification_message)
        except Exception as exc:
            logger.error(
                "Failed to send welfare event notification",
                member_phone=member.phone,
                error=str(exc),
                event_id=str(proposal.id),
            )

    await AuditLog(
        action="approve_welfare_proposal",
        entity_type="WelfareEvent",
        entity_id=str(proposal.id),
        performed_by=approved_by,
        details={"title": proposal.title, "status": proposal.status},
    ).insert()
    return proposal

async def get_active_events():
    return await WelfareEvent.find(WelfareEvent.status == "Active").to_list()

async def get_pending_proposals():
    proposals = await WelfareEvent.find(WelfareEvent.status == "PendingApproval").to_list()
    return [proposal for proposal in proposals if getattr(proposal, "status", None) == "PendingApproval"]

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