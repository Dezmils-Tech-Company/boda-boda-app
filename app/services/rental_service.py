from app.models.rental_booking import RentalBooking
from app.models.inventory_item import InventoryItem

async def create_booking(booking_data, member):
    # Check availability (simplified)
    booking = RentalBooking(**booking_data.dict(), member=member)
    await booking.insert()
    return booking

async def get_user_bookings(member_id):
    return await RentalBooking.find(RentalBooking.member.id == member_id).to_list()