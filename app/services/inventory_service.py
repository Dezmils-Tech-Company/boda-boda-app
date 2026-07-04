from app.models.inventory_item import InventoryItem
from app.models.rental_booking import RentalBooking
from app.exceptions.exceptions import ResourceNotFound
from app.services.upload_service import upload_image_to_cloudinary


async def create_inventory_item(item_data):
    item_payload = item_data.dict()
    photos = item_payload.pop("photos", [])

    if photos:
        uploaded_photos = []
        for photo in photos:
            if isinstance(photo, str) and photo.startswith(("http://", "https://")):
                uploaded_photos.append(photo)
                continue
            uploaded_result = await upload_image_to_cloudinary(photo)
            uploaded_photos.append(uploaded_result["secure_url"])
        item_payload["photos"] = uploaded_photos
    else:
        item_payload["photos"] = []

    item = InventoryItem(**item_payload)
    await item.insert()
    return item


async def list_inventory_items():
    return await InventoryItem.find_all().to_list()


async def delete_inventory_item(item_id: str):
    item = await InventoryItem.get(item_id)
    if not item:
        raise ResourceNotFound("Inventory item")

    # Prevent deletion if the item is referenced by any booking.
    active_bookings = await RentalBooking.find(
        {"items.item_id": item_id}
    ).to_list()
    if active_bookings:
        raise ResourceNotFound("Inventory item has active or pending bookings")

    await item.delete()
    return True
