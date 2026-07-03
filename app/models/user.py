from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, Field

class FamilyMember(BaseModel):
    name: str
    age: Optional[int] = None
    relationship: str

class NextOfKin(BaseModel):
    name: str
    phone: str
    relationship: str

class User(Document):
    phone: str
    full_name: str
    hashed_password: Optional[str] = None
    id_number: Optional[str] = None
    family_members: List[FamilyMember] = Field(default_factory=list)
    next_of_kin: Optional[NextOfKin] = None
    role: str = "Member"  # Admin, Treasurer, Secretary, Member
    status: str = "Active"
    join_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = ["phone", "role"]