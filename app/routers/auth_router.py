from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    verify_password,
    get_password_hash,
)
from app.core.security import get_current_user

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    user = await authenticate_user(credentials.phone, credentials.pin)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or PIN",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.phone, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.phone, "role": user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    token_data = verify_refresh_token(refresh_token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": token_data.phone, "role": token_data.role})
    new_refresh_token = create_refresh_token({"sub": token_data.phone, "role": token_data.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
    }

@router.post("/reset-pin")
async def reset_pin(
    current_pin: str = Body(...),
    new_pin: str = Body(...),
    current_user=Depends(get_current_user),
):
    if not verify_password(current_pin, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current PIN is invalid")

    current_user.hashed_password = get_password_hash(new_pin)
    await current_user.save()
    return {"message": "PIN updated successfully"}