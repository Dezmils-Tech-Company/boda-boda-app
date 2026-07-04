import pytest

from app.services import welfare_service


class DummyQuery:
    def __init__(self, items):
        self.items = items

    async def to_list(self):
        return list(self.items)


class DummyWelfareEvent:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.id = "event-123"


@pytest.mark.asyncio
async def test_get_pending_proposals_returns_only_pending_events(monkeypatch):
    pending = [DummyWelfareEvent(title="Pending A", status="PendingApproval")]
    active = [DummyWelfareEvent(title="Active A", status="Active")]

    class FakeWelfareEventModel:
        status = "status"

        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def find(*args, **kwargs):
            return DummyQuery(pending + active)

    monkeypatch.setattr(welfare_service, "WelfareEvent", FakeWelfareEventModel)

    result = await welfare_service.get_pending_proposals()

    assert len(result) == 1
    assert result[0].title == "Pending A"
    assert result[0].status == "PendingApproval"
