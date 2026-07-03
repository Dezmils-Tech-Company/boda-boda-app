from app.models.welfare_event import WelfareEvent
from app.models.event_contribution import EventContribution
from app.models.user import User
from datetime import datetime

async def create_welfare_event(event_data, created_by):
    affected_member = await User.get(event_data.affected_member_id)
    if affected_member is None:
        raise ValueError("Affected member not found")

    event = WelfareEvent(
        event_type=event_data.event_type,
        title=event_data.title,
        description=event_data.description,
        affected_member=affected_member,
        amount_per_member=event_data.amount_per_member,
        deadline=event_data.deadline,
        created_by=created_by,
    )
    await event.insert()

    members = await User.find(User.status == "Active").to_list()
    for member in members:
        contrib = EventContribution(
            welfare_event=event.id,
            member=member.id,
            amount_due=event.amount_per_member,
        )
        await contrib.insert()

    return event

async def get_active_events():
    return await WelfareEvent.find(WelfareEvent.status == "Active").to_list()