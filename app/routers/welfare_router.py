from fastapi import APIRouter, Depends, HTTPException
from app.schemas.welfare import WelfareEventCreate, WelfareEventProposalCreate, WelfareEventResponse
from app.services.welfare_service import (
    approve_welfare_proposal,
    create_welfare_event,
    get_active_events,
    get_pending_proposals,
    submit_welfare_proposal,
)
from app.core.security import get_current_user, require_admin

router = APIRouter()

@router.post("/events", response_model=WelfareEventResponse)
async def create_event(event_data: WelfareEventCreate, current_user=Depends(require_admin)):
    return await create_welfare_event(event_data, current_user)

@router.post("/events/propose", response_model=WelfareEventResponse)
async def propose_event(event_data: WelfareEventProposalCreate, current_user=Depends(get_current_user)):
    try:
        return await submit_welfare_proposal(event_data, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.post("/events/{event_id}/approve", response_model=WelfareEventResponse)
async def approve_event(event_id: str, current_user=Depends(require_admin)):
    try:
        return await approve_welfare_proposal(event_id, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.get("/events/active", response_model=list[WelfareEventResponse])
async def list_active_events(current_user=Depends(get_current_user)):
    return await get_active_events()

@router.get("/events/pending", response_model=list[WelfareEventResponse])
async def list_pending_proposals(current_user=Depends(require_admin)):
    return await get_pending_proposals()