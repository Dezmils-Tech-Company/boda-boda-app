from beanie import Document
from datetime import datetime

class GroupSettings(Document):
    monthly_subscription_amount: float = 1000.0
    default_interest_rate: float = 1.5
    late_payment_penalty: float = 100.0
    redemption_month: str = "December"
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "group_settings"