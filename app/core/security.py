from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.core.permissions import UserRole
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        phone: Optional[str] = payload.get('sub')
        role: Optional[str] = payload.get('role')
        if phone is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.find_one(User.phone == phone)
    if not user:
        raise credentials_exception

    if user.role.value != role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token role does not match current user role',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


async def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.Admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin access required',
        )
    return current_user

async def require_treasurer(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.Treasurer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Treasurer access required',
        )
    return current_user

async def require_secretary(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.Secretary:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Secretary access required',
        )
    return current_user

async def require_chairperson(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.Chairperson:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Chairperson access required',
        )
    return current_user

async def require_loan_official(current_user=Depends(get_current_user)):
    if current_user.role not in {UserRole.Treasurer, UserRole.Secretary, UserRole.Chairperson}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Treasurer, Secretary, or Chairperson access required',
        )
    return current_user
