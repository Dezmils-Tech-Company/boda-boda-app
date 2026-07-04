from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.permissions import UserRole
from app.models.user import User
from app.schemas.auth import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: Optional[str]) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

async def authenticate_user(phone: str, password: str):
    user = await User.find_one(User.phone == phone)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def verify_refresh_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        phone = payload.get("sub")
        role = payload.get("role")
        if not phone or not role:
            return None
        return TokenData(phone=phone, role=role)
    except JWTError:
        return None