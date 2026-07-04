from bson import ObjectId
from pydantic import BaseModel, field_validator
from typing import Any, Optional

class BaseResponse(BaseModel):
    status: str = "success"
    message: str
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    detail: Optional[str] = None


class DocumentResponse(BaseModel):
    id: str

    model_config = {
        "from_attributes": True,
        "json_encoders": {ObjectId: str},
    }

    @field_validator("id", mode="before")
    @classmethod
    def coerce_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value