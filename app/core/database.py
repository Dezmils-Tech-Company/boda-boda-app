from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.group_settings import GroupSettings
from app.models.welfare_event import WelfareEvent
from app.models.event_contribution import EventContribution
from app.models.inventory_item import InventoryItem
from app.models.rental_booking import RentalBooking
from app.models.subscription_payment import SubscriptionPayment
from app.models.loan import Loan
from app.models.transaction import Transaction
from app.models.audit_log import AuditLog

async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[
            User, GroupSettings, WelfareEvent, EventContribution,
            InventoryItem, RentalBooking, SubscriptionPayment,
            Loan, Transaction, AuditLog
        ]
    )
    return client