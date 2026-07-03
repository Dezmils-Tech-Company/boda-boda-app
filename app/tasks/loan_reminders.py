from celery import shared_task
from loguru import logger
from app.models.loan import Loan
from datetime import datetime
from app.services.notification_service import send_notification

@shared_task
async def send_loan_due_reminders():
    """Send reminders for upcoming loan repayments"""
    today = datetime.utcnow().date()

    active_loans = await Loan.find(Loan.status == "Active").to_list()

    for loan in active_loans:
        for schedule in loan.repayment_schedule:
            if not schedule.paid and schedule.due_date.date() <= today + timedelta(days=3):
                try:
                    member = await loan.member.fetch()
                    await send_notification(
                        member.phone,
                        f"Your loan installment of KSh {schedule.amount} is due on {schedule.due_date.date()}. Please pay on time."
                    )
                except Exception as e:
                    logger.error(f"Failed to send loan reminder: {e}")