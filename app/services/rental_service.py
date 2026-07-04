from app.models.audit_log import AuditLog
from app.models.inventory_item import InventoryItem
from app.models.rental_booking import RentalBooking
from app.exceptions.exceptions import BookingConflict, ResourceNotFound

async def create_booking(booking_data, member):
    booking_items = []
    for item_data in booking_data.items:
        item = await InventoryItem.get(item_data.item_id)
        if not item:
            raise ResourceNotFound(f"Inventory item {item_data.item_id}")
        if item.available_quantity < item_data.quantity:
            raise BookingConflict(f"Not enough quantity for item {item.name}")
        booking_items.append(item_data)

    total_amount = 0.0
    for item in booking_items:
        inventory_item = await InventoryItem.get(item.item_id)
        total_amount += inventory_item.daily_rate * item.quantity

    booking = RentalBooking(
        member=member,
        items=booking_data.items,
        start_date=booking_data.start_date,
        end_date=booking_data.end_date,
        total_amount=total_amount,
        deposit_paid=getattr(booking_data, "deposit_paid", 0.0),
        status="Pending",
    )
    await booking.insert()
    await AuditLog(
        action="create_rental_booking",
        entity_type="RentalBooking",
        entity_id=str(booking.id),
        performed_by=member,
        details={"total_amount": booking.total_amount, "item_count": len(booking.items)},
    ).insert()
    return booking

async def approve_booking(booking_id: str, approver):
    booking = await RentalBooking.get(booking_id)
    if not booking:
        raise ResourceNotFound("Rental booking")
    if booking.status != "Pending":
        raise BookingConflict("Only pending bookings can be approved")

    for item_data in booking.items:
        item = await InventoryItem.get(item_data.item_id)
        if not item:
            raise ResourceNotFound(f"Inventory item {item_data.item_id}")
        if item.available_quantity < item_data.quantity:
            raise BookingConflict(f"Not enough quantity for item {item.name}")
        item.available_quantity -= item_data.quantity
        await item.save()

    booking.status = "Confirmed"
    await booking.save()
    await AuditLog(
        action="approve_rental_booking",
        entity_type="RentalBooking",
        entity_id=str(booking.id),
        performed_by=approver,
        details={"status": booking.status, "item_count": len(booking.items)},
    ).insert()
    return booking

async def get_user_bookings(member_id):
    return await RentalBooking.find(RentalBooking.member.id == member_id).to_list()

async def get_pending_bookings():
    return await RentalBooking.find(RentalBooking.status == "Pending").to_list()