from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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
    id_number: Optional[str] = None
    family_members: List[FamilyMember] = []
    next_of_kin: Optional[NextOfKin] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    family_members: Optional[List[FamilyMember]] = None
    next_of_kin: Optional[NextOfKin] = None
    status: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    phone: str
    full_name: str
    role: str
    status: str
    join_date: datetime

    class Config:
        from_attributes = True