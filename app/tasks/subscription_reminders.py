from celery import shared_task
from loguru import logger
from datetime import datetime
from app.models.subscription_payment import SubscriptionPayment
from app.models.user import User
from app.services.notification_service import send_notification

@shared_task
async def process_december_redemption():
    """Process annual subscription redemption in December"""
    current_month = datetime.utcnow().month
    if current_month != 12:
        return

    current_year = datetime.utcnow().year

    # Get all active members
    members = await User.find(User.status == "Active").to_list()

    for member in members:
        # Calculate total paid subscriptions for the year
        payments = await SubscriptionPayment.find(
            SubscriptionPayment.member.id == member.id,
            SubscriptionPayment.year == current_year
        ).to_list()

        total_paid = sum(p.amount for p in payments)

        if total_paid > 0:
            try:
                # Here you would create a redemption transaction
                await send_notification(
                    member.phone,
                    f"Your December redemption of KSh {total_paid} has been processed. Thank you for being a loyal member."
                )
                logger.info(f"Redemption processed for {member.full_name}")
            except Exception as e:
                logger.error(f"Redemption failed for {member.full_name}: {e}")