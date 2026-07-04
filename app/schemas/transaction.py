from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from app.schemas.base import DocumentResponse

class TransactionResponse(DocumentResponse):
    type: str
    amount: float
    description: str
    created_at: datetime