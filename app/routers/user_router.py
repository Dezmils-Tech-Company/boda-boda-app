from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import create_user, get_user_by_phone, get_all_users, update_user
from app.core.security import get_current_user, require_admin

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_new_user(user_data: UserCreate, current_user=Depends(require_admin)):
    return await create_user(user_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user=Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
async def get_all_members(current_user=Depends(require_admin)):
    return await get_all_users()

@router.get("/{phone}", response_model=UserResponse)
async def get_user(phone: str, current_user=Depends(get_current_user)):
    user = await get_user_by_phone(phone)
    if not user:
        raise HTTPException(404, "User not found")
    return user