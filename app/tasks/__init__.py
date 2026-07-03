from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "chama_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.subscription_redeemer",
        "app.tasks.loan_reminders",
        "app.tasks.subscription_reminders"
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Nairobi",
    enable_utc=True,
)