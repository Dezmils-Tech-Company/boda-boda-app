from app.models.audit_log import AuditLog
from app.models.inventory_item import InventoryItem
from app.models.rental_booking import RentalBooking

async def create_booking(booking_data, member):
    booking_items = []
    for item_data in booking_data.items:
        item = await InventoryItem.get(item_data.item_id)
        if not item:
            raise ValueError(f"Inventory item {item_data.item_id} not found")
        if item.available_quantity < item_data.quantity:
            raise ValueError(f"Not enough quantity for item {item.name}")
        item.available_quantity -= item_data.quantity
        await item.save()
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

async def get_user_bookings(member_id):
    return await RentalBooking.find(RentalBooking.member.id == member_id).to_list()