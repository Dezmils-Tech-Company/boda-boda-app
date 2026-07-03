from app.models.welfare_event import WelfareEvent
from app.models.event_contribution import EventContribution
from app.models.user import User
from app.repositories.base_repository import BaseRepository

class WelfareRepository(BaseRepository[WelfareEvent]):
    def __init__(self):
        super().__init__(WelfareEvent)

    async def create_event(self, event_data, created_by):
        event = WelfareEvent(**event_data.dict(), created_by=created_by)
        await event.insert()

        # Auto create contributions
        members = await User.find(User.status == "Active").to_list()
        for member in members:
            contrib = EventContribution(
                welfare_event=event.id,
                member=member.id,
                amount_due=event.amount_per_member
            )
            await contrib.insert()

        return event

    async def get_active_events(self):
        return await WelfareEvent.find(WelfareEvent.status == "Active").to_list()