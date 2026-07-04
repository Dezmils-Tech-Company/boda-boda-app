from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.core.permissions import UserRole
from app.schemas.base import DocumentResponse

class FamilyMember(BaseModel):
    name: str
    age: Optional[int] = None
    relationship: str

class NextOfKin(BaseModel):
    name: str
    phone: str
    relationship: str

class UserCreate(BaseModel):
    phone: str
    full_name: str
    pin: str
    role: Optional[UserRole] = UserRole.Member
    id_number: Optional[str] = None
    family_members: List[FamilyMember] = []
    next_of_kin: Optional[NextOfKin] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    family_members: Optional[List[FamilyMember]] = None
    next_of_kin: Optional[NextOfKin] = None
    status: Optional[str] = None

class UserResponse(DocumentResponse):
    id: str
    phone: str
    full_name: str
    role: UserRole
    status: str
    join_date: datetime

    class Config:
        from_attributes = True