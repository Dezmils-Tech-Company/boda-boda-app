from fastapi import APIRouter, Depends
from app.schemas.rental import RentalBookingCreate, RentalBookingResponse
from app.services.rental_service import create_booking, get_user_bookings
from app.core.security import get_current_user

router = APIRouter()

@router.post("/bookings", response_model=RentalBookingResponse)
async def create_rental_booking(booking: RentalBookingCreate, current_user=Depends(get_current_user)):
    return await create_booking(booking, current_user)

@router.get("/my-bookings", response_model=list[RentalBookingResponse])
async def my_bookings(current_user=Depends(get_current_user)):
    return await get_user_bookings(current_user.id)