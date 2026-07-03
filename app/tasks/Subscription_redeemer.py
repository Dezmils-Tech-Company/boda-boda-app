from celery import shared_task
from loguru import logger
from app.models.user import User
from app.models.subscription_payment import SubscriptionPayment
from datetime import datetime
from app.services.notification_service import send_notification

@shared_task
async def send_monthly_subscription_reminders():
    """Send reminders to members who haven't paid this month's subscription"""
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    # Find members who haven't paid
    paid_members = await SubscriptionPayment.find(
        SubscriptionPayment.month == current_month,
        SubscriptionPayment.year == current_year,
        SubscriptionPayment.status == "Paid"
    ).to_list()

    paid_ids = [p.member.id for p in paid_members]

    unpaid_members = await User.find(
        User.status == "Active",
        {"_id": {"$nin": paid_ids}}
    ).to_list()

    for member in unpaid_members:
        try:
            await send_notification(
                member.phone,
                f"Dear {member.full_name}, your monthly subscription of KSh {1000} is due. Please pay to avoid penalties."
            )
            logger.info(f"Reminder sent to {member.phone}")
        except Exception as e:
            logger.error(f"Failed to send reminder to {member.phone}: {e}")