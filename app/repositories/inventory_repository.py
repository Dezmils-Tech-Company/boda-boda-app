from app.models.inventory_item import InventoryItem
from app.repositories.base_repository import BaseRepository

class InventoryRepository(BaseRepository[InventoryItem]):
    def __init__(self):
        super().__init__(InventoryItem)

    async def get_available_items(self):
        return await InventoryItem.find(InventoryItem.available_quantity > 0).to_list()
