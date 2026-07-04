from pydantic import BaseModel
from typing import Optional
from app.core.permissions import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    role: UserRole

class TokenData(BaseModel):
    phone: str
    role: UserRole