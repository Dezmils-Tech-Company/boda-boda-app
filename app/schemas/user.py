from pydantic import BaseModel, Field
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
    image: Optional[str] = Field(default=None, description="Profile image URL", examples=["https://example.com/profile.jpg"])
    photo: Optional[str] = Field(default=None, description="Alternative profile image URL", examples=["https://example.com/profile.jpg"])
    family_members: List[FamilyMember] = Field(default_factory=list)
    next_of_kin: Optional[NextOfKin] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "phone": "+254700000000",
                "full_name": "Jane Doe",
                "pin": "1234",
                "image": "https://example.com/profile.jpg",
                "family_members": [],
                "next_of_kin": {
                    "name": "John Doe",
                    "phone": "+254700000001",
                    "relationship": "Brother"
                }
            }
        }
    }

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    image: Optional[str] = Field(default=None, description="Profile image URL")
    photo: Optional[str] = Field(default=None, description="Alternative profile image URL")
    family_members: Optional[List[FamilyMember]] = None
    next_of_kin: Optional[NextOfKin] = None
    status: Optional[str] = None

class UserResponse(DocumentResponse):
    id: str
    phone: str
    full_name: str
    role: UserRole
    status: str
    image: Optional[str] = None
    photo: Optional[str] = None
    join_date: datetime

    class Config:
        from_attributes = True