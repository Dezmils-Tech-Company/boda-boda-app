from app.models.rental_booking import RentalBooking
from app.repositories.base_repository import BaseRepository

class RentalRepository(BaseRepository[RentalBooking]):
    def __init__(self):
        super().__init__(RentalBooking)

    async def get_user_bookings(self, member_id: str):
        return await RentalBooking.find(RentalBooking.member.id == member_id).to_list()

    async def get_pending_bookings(self):
        return await RentalBooking.find(RentalBooking.status == "Pending").to_list()
    