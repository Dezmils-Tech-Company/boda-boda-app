from fastapi import APIRouter, Depends, HTTPException
from app.schemas.welfare import WelfareEventCreate, WelfareEventResponse
from app.services.welfare_service import create_welfare_event, get_active_events
from app.core.security import get_current_user, require_admin

router = APIRouter()

@router.post("/events", response_model=WelfareEventResponse)
async def create_event(event_data: WelfareEventCreate, current_user=Depends(require_admin)):
    return await create_welfare_event(event_data, current_user)

@router.get("/events/active", response_model=list[WelfareEventResponse])
async def list_active_events(current_user=Depends(get_current_user)):
    return await get_active_events()