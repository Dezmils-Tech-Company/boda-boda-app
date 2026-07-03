from beanie import Document, Link
from datetime import datetime

class AuditLog(Document):
    action: str
    entity_type: str
    entity_id: str
    performed_by: Link["User"]
    details: dict
    timestamp: datetime = datetime.utcnow()

    class Settings:
        name = "audit_logs"