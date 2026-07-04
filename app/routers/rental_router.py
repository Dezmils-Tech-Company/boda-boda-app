from fastapi import APIRouter, Depends, HTTPException
from app.schemas.rental import (
    InventoryItemCreate,
    InventoryItemResponse,
    RentalBookingCreate,
    RentalBookingResponse,
)
from app.services.inventory_service import (
    create_inventory_item,
    delete_inventory_item,
    list_inventory_items,
)
from app.services.rental_service import (
    approve_booking,
    create_booking,
    get_pending_bookings,
    get_user_bookings,
)
from app.core.security import get_current_user, require_admin
from app.exceptions.exceptions import BookingConflict, ResourceNotFound

router = APIRouter()

@router.post("/bookings", response_model=RentalBookingResponse)
async def create_rental_booking(booking: RentalBookingCreate, current_user=Depends(get_current_user)):
    return await create_booking(booking, current_user)

@router.get("/my-bookings", response_model=list[RentalBookingResponse])
async def my_bookings(current_user=Depends(get_current_user)):
    return await get_user_bookings(current_user.id)

@router.get("/inventory", response_model=list[InventoryItemResponse])
async def get_inventory(available_only: bool = False, current_user=Depends(get_current_user)):
    items = await list_inventory_items()
    if available_only:
        items = [item for item in items if item.available_quantity > 0]
    return items

@router.post("/inventory", response_model=InventoryItemResponse)
async def add_inventory_item(item_data: InventoryItemCreate, current_user=Depends(require_admin)):
    return await create_inventory_item(item_data)

@router.delete("/inventory/{item_id}")
async def remove_inventory_item(item_id: str, current_user=Depends(require_admin)):
    await delete_inventory_item(item_id)
    return {"status": "success", "message": "Inventory item removed"}

@router.get("/bookings/pending", response_model=list[RentalBookingResponse])
async def pending_bookings(current_user=Depends(require_admin)):
    return await get_pending_bookings()

@router.post("/bookings/{booking_id}/approve", response_model=RentalBookingResponse)
async def approve_rental_booking(booking_id: str, current_user=Depends(require_admin)):
    return await approve_booking(booking_id, current_user)