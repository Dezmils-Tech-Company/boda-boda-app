import pytest
from datetime import datetime
from app.models.user import User
from app.models.transaction import Transaction
from app.services.savings_service import record_savings_deposit, get_member_savings_balance, get_member_savings_transactions
from unittest.mock import MagicMock


class MockTransaction:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", "test-id")
        self.type = kwargs.get("type", "savings")
        self.amount = kwargs.get("amount", 0.0)
        self.description = kwargs.get("description", "")
        self.member = kwargs.get("member")
        self.created_by = kwargs.get("created_by")
        self.created_at = kwargs.get("created_at", datetime.utcnow())


class MockQuery:
    def __init__(self, items):
        self.items = items
        self._sort_params = None
        self._limit_count = None

    def sort(self, *args, **kwargs):
        # Handle sort(-Transaction.created_at) or similar
        self._sort_params = (args, kwargs)
        return self

    def limit(self, limit):
        self._limit_count = limit
        return self

    async def to_list(self):
        items = self.items
        # Apply limit if specified
        if self._limit_count is not None:
            items = items[:self._limit_count]
        return items


@pytest.mark.asyncio
async def test_record_savings_deposit(monkeypatch):
    """Test recording a savings deposit"""
    # Create a mock user
    test_user = MagicMock(spec=User)
    test_user.id = "test-user-id"

    amount = 100.0
    description = "Monthly savings deposit"

    # Mock the Transaction constructor to return a MockTransaction
    def mock_transaction_init(self, **kwargs):
        # Store the attributes for later verification
        for key, value in kwargs.items():
            setattr(self, key, value)
        # Ensure required fields are set
        if not hasattr(self, 'id'):
            self.id = "test-transaction-id"
        if not hasattr(self, 'created_at'):
            self.created_at = datetime.utcnow()

    # Patch the Transaction model's __init__ method
    monkeypatch.setattr(Transaction, "__init__", mock_transaction_init)
    # Also need to patch the class itself to allow instantiation
    monkeypatch.setattr(Transaction, "__call__", lambda cls, **kwargs: MockTransaction(**kwargs))

    transaction = await record_savings_deposit(
        amount=amount,
        description=description,
        member=test_user,
        created_by=test_user
    )

    assert transaction.id == "test-transaction-id"
    assert transaction.type == "savings"
    assert transaction.amount == amount
    assert transaction.description == description
    assert transaction.member.id == test_user.id
    assert transaction.created_by.id == test_user.id
    assert isinstance(transaction.created_at, datetime)


@pytest.mark.asyncio
async def test_get_member_savings_balance(monkeypatch):
    """Test getting member savings balance"""
    # Create a mock user
    test_user = MagicMock(spec=User)
    test_user.id = "test-user-id"

    # Create mock transactions
    mock_transactions = [
        MockTransaction(
            id="tx1",
            amount=50.0,
            description="Initial deposit",
            member=test_user,
            created_by=test_user
        ),
        MockTransaction(
            id="tx2",
            amount=30.0,
            description="Second deposit",
            member=test_user,
            created_by=test_user
        )
    ]

    # Mock the Transaction.find method to return our transactions
    def mock_find(query):
        # For simplicity in this test, we'll return all transactions
        # In a real implementation, we would parse the query to filter
        return MockQuery(mock_transactions)

    monkeypatch.setattr(Transaction, "find", mock_find)
    # Also mock delete for cleanup
    async def mock_delete():
        pass
    monkeypatch.setattr(Transaction, "delete", mock_delete)

    balance_info = await get_member_savings_balance(str(test_user.id))

    assert balance_info["total_savings"] == 80.0
    assert balance_info["savings_transactions_count"] == 2
    assert len(balance_info["savings_transactions"]) == 2


@pytest.mark.asyncio
async def test_get_member_savings_transactions(monkeypatch):
    """Test getting member savings transactions"""
    # Create a mock user
    test_user = MagicMock(spec=User)
    test_user.id = "test-user-id"

    # Create mock transactions with different timestamps
    mock_transactions = [
        MockTransaction(
            id="tx1",
            amount=25.0,
            description="First deposit",
            member=test_user,
            created_by=test_user,
            created_at=datetime(2023, 1, 1, 10, 0, 0)
        ),
        MockTransaction(
            id="tx2",
            amount=75.0,
            description="Second deposit",
            member=test_user,
            created_by=test_user,
            created_at=datetime(2023, 1, 1, 11, 0, 0)  # Later time
        )
    ]

    # Mock the Transaction.find method to return our transactions
    def mock_find(query):
        return MockQuery(mock_transactions)

    monkeypatch.setattr(Transaction, "find", mock_find)

    transactions = await get_member_savings_transactions(str(test_user.id), limit=10)

    assert len(transactions) == 2
    # Should be ordered by created_at descending (most recent first)
    assert transactions[0].description == "Second deposit"
    assert transactions[1].description == "First deposit"
    assert transactions[0].amount == 75.0
    assert transactions[1].amount == 25.0