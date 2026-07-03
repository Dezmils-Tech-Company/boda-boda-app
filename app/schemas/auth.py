from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    phone: str
    pin: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    phone: str
    role: str