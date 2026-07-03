from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "chama_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.subscription_reminders",
        "app.tasks.loan_reminders",
        "app.tasks.december_redemption_task"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Nairobi",
    enable_utc=True,
    beat_schedule={
        "monthly-reminders": {
            "task": "app.tasks.subscription_reminders.send_monthly_subscription_reminders",
            "schedule": 86400.0,  # Every 24 hours
        },
        "loan-reminders": {
            "task": "app.tasks.loan_reminders.send_loan_due_reminders",
            "schedule": 86400.0,
        },
        "december-redemption": {
            "task": "app.tasks.december_redemption_task.process_december_redemption",
            "schedule": {"month_of_year": 12, "day_of_month": 1, "hour": 9},  # 1st Dec at 9 AM
        },
    },
)