import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.database import init_db
from app.services.auth_service import get_password_hash
from app.models.user import User
from app.models.group_settings import GroupSettings
from app.models.welfare_event import WelfareEvent
from app.models.event_contribution import EventContribution
from app.models.inventory_item import InventoryItem
from app.models.rental_booking import RentalBooking
from app.models.subscription_payment import SubscriptionPayment
from app.models.loan import Loan, RepaymentItem
from app.models.transaction import Transaction
from app.models.audit_log import AuditLog


def create_repayment_schedule(amount: float, tenure_months: int) -> list[RepaymentItem]:
    monthly_amount = round(amount / tenure_months, 2)
    schedule = []
    for month_idx in range(1, tenure_months + 1):
        due_date = datetime.utcnow() + timedelta(days=30 * month_idx)
        schedule.append(RepaymentItem(due_date=due_date, amount=monthly_amount))
    return schedule


async def clear_collections() -> None:
    models = [
        AuditLog,
        EventContribution,
        GroupSettings,
        InventoryItem,
        Loan,
        RentalBooking,
        SubscriptionPayment,
        Transaction,
        WelfareEvent,
        User,
    ]

    for model in models:
        collection = model.get_motor_collection()
        await collection.delete_many({})


async def seed_users() -> dict[str, User]:
    users = {
        "admin": User(
            phone="254700000001",
            full_name="Admin User",
            hashed_password=get_password_hash("1111"),
            role="Admin",
            status="Active",
        ),
        "treasurer": User(
            phone="254700000002",
            full_name="Treasurer User",
            hashed_password=get_password_hash("2222"),
            role="Treasurer",
            status="Active",
        ),
        "secretary": User(
            phone="254700000003",
            full_name="Secretary User",
            hashed_password=get_password_hash("3333"),
            role="Secretary",
            status="Active",
        ),
        "member_a": User(
            phone="254700000004",
            full_name="Rider A",
            hashed_password=get_password_hash("4444"),
            id_number="A1234567",
            role="Member",
            status="Active",
        ),
        "member_b": User(
            phone="254700000005",
            full_name="Rider B",
            hashed_password=get_password_hash("5555"),
            id_number="B2345678",
            role="Member",
            status="Active",
        ),
        "member_c": User(
            phone="254700000006",
            full_name="Rider C",
            hashed_password=get_password_hash("6666"),
            id_number="C3456789",
            role="Member",
            status="Active",
        ),
    }

    for user in users.values():
        await user.insert()
    return users


async def seed_group_settings() -> None:
    settings = [
        GroupSettings(
            monthly_subscription_amount=1000.0,
            default_interest_rate=1.5,
            late_payment_penalty=100.0,
            redemption_month="December",
        ),
        GroupSettings(
            monthly_subscription_amount=1200.0,
            default_interest_rate=2.0,
            late_payment_penalty=150.0,
            redemption_month="December",
        ),
        GroupSettings(
            monthly_subscription_amount=900.0,
            default_interest_rate=1.0,
            late_payment_penalty=75.0,
            redemption_month="December",
        ),
    ]
    for setting in settings:
        await setting.insert()


async def seed_inventory_items() -> list[InventoryItem]:
    items = [
        InventoryItem(
            name="Spare Wheel",
            category="Parts",
            total_quantity=10,
            available_quantity=8,
            daily_rate=150.0,
            deposit_rate=500.0,
            photos=["/images/spare_wheel.jpg"],
            condition="Good",
            location="Warehouse A",
        ),
        InventoryItem(
            name="Helmet",
            category="Safety",
            total_quantity=15,
            available_quantity=12,
            daily_rate=50.0,
            deposit_rate=100.0,
            photos=["/images/helmet.jpg"],
            condition="Excellent",
            location="Warehouse B",
        ),
        InventoryItem(
            name="Tool Kit",
            category="Tools",
            total_quantity=8,
            available_quantity=6,
            daily_rate=120.0,
            deposit_rate=300.0,
            photos=["/images/toolkit.jpg"],
            condition="Good",
            location="Workshop",
        ),
        InventoryItem(
            name="Chairs",
            category="Event",
            total_quantity=50,
            available_quantity=50,
            daily_rate=30.0,
            deposit_rate=100.0,
            photos=["/images/chairs.jpg"],
            condition="Good",
            location="Event Store",
        ),
        InventoryItem(
            name="Tents",
            category="Event",
            total_quantity=10,
            available_quantity=10,
            daily_rate=500.0,
            deposit_rate=1500.0,
            photos=["/images/tents.jpg"],
            condition="Good",
            location="Event Store",
        ),
        InventoryItem(
            name="PA System",
            category="Audio",
            total_quantity=3,
            available_quantity=3,
            daily_rate=800.0,
            deposit_rate=2500.0,
            photos=["/images/pa_system.jpg"],
            condition="Good",
            location="Equipment Room",
        ),
        InventoryItem(
            name="Generator",
            category="Power",
            total_quantity=2,
            available_quantity=2,
            daily_rate=1200.0,
            deposit_rate=4000.0,
            photos=["/images/generator.jpg"],
            condition="Good",
            location="Equipment Room",
        ),
    ]
    for item in items:
        await item.insert()
    return items


async def seed_rental_bookings(users: dict[str, User], items: list[InventoryItem]) -> None:
    bookings = [
        RentalBooking(
            member=users["member_a"],
            items=[{"item_id": str(items[0].id), "quantity": 1}],
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=3),
            total_amount=450.0,
            deposit_paid=500.0,
            status="Confirmed",
            condition_before={"wheel": "Good"},
        ),
        RentalBooking(
            member=users["member_b"],
            items=[{"item_id": str(items[1].id), "quantity": 2}],
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=2),
            total_amount=100.0,
            deposit_paid=200.0,
            status="Confirmed",
            condition_before={"helmets": "New"},
        ),
        RentalBooking(
            member=users["member_c"],
            items=[{"item_id": str(items[2].id), "quantity": 1}],
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=1),
            total_amount=120.0,
            deposit_paid=300.0,
            status="Pending",
            condition_before={"tool_kit": "Good"},
        ),
    ]
    for booking in bookings:
        await booking.insert()


async def seed_subscription_payments(users: dict[str, User]) -> None:
    payments = [
        SubscriptionPayment(
            member=users["member_a"],
            month=1,
            year=2026,
            amount=1000.0,
            status="Paid",
            payment_date=datetime.utcnow(),
        ),
        SubscriptionPayment(
            member=users["member_b"],
            month=1,
            year=2026,
            amount=1000.0,
            status="Paid",
            payment_date=datetime.utcnow(),
        ),
        SubscriptionPayment(
            member=users["member_c"],
            month=1,
            year=2026,
            amount=1000.0,
            status="Pending",
        ),
    ]
    for payment in payments:
        await payment.insert()


async def seed_welfare_events(users: dict[str, User]) -> list[WelfareEvent]:
    events = [
        WelfareEvent(
            event_type="Accident Support",
            title="Rider Hospital Support",
            description="Support for a rider injured during a delivery.",
            affected_member=users["member_a"],
            amount_per_member=1500.0,
            deadline=datetime.utcnow() + timedelta(days=14),
            status="Active",
            created_by=users["secretary"],
        ),
        WelfareEvent(
            event_type="Fuel Relief",
            title="Fuel Assistance",
            description="Small fuel support fund for daily riders.",
            affected_member=users["member_b"],
            amount_per_member=800.0,
            deadline=datetime.utcnow() + timedelta(days=7),
            status="Active",
            created_by=users["treasurer"],
        ),
        WelfareEvent(
            event_type="School Fees",
            title="Dependent School Support",
            description="Help a rider pay for a child’s school fees.",
            affected_member=users["member_c"],
            amount_per_member=2000.0,
            deadline=datetime.utcnow() + timedelta(days=30),
            status="Active",
            created_by=users["admin"],
        ),
    ]
    for event in events:
        await event.insert()
    return events


async def seed_event_contributions(events: list[WelfareEvent], users: dict[str, User]) -> None:
    contributions = [
        EventContribution(
            welfare_event=events[0],
            member=users["member_b"],
            amount_due=1500.0,
            amount_paid=1500.0,
            status="Paid",
            payment_date=datetime.utcnow(),
        ),
        EventContribution(
            welfare_event=events[1],
            member=users["member_a"],
            amount_due=800.0,
            amount_paid=400.0,
            status="Partial",
            payment_date=datetime.utcnow(),
        ),
        EventContribution(
            welfare_event=events[2],
            member=users["member_c"],
            amount_due=2000.0,
            amount_paid=0.0,
            status="Pending",
        ),
    ]
    for contrib in contributions:
        await contrib.insert()


async def seed_loans(users: dict[str, User]) -> None:
    loans = [
        Loan(
            member=users["member_a"],
            amount=10000.0,
            interest_rate=2.5,
            tenure_months=6,
            monthly_installment=round(10250.0 / 6, 2),
            purpose="Purchase vehicle spare parts",
            guarantors=[users["member_b"], users["member_c"]],
            status="Pending",
            repayment_schedule=create_repayment_schedule(10250.0, 6),
        ),
        Loan(
            member=users["member_b"],
            amount=8000.0,
            interest_rate=3.0,
            tenure_months=4,
            monthly_installment=round(8240.0 / 4, 2),
            purpose="Repair boda boda frame",
            guarantors=[users["member_a"], users["member_c"]],
            status="Pending",
            repayment_schedule=create_repayment_schedule(8240.0, 4),
        ),
        Loan(
            member=users["member_c"],
            amount=12000.0,
            interest_rate=2.0,
            tenure_months=8,
            monthly_installment=round(12240.0 / 8, 2),
            purpose="Buy petrol for business",
            guarantors=[users["member_a"], users["member_b"]],
            status="Pending",
            repayment_schedule=create_repayment_schedule(12240.0, 8),
        ),
    ]
    for loan in loans:
        await loan.insert()


async def seed_transactions(users: dict[str, User]) -> None:
    transactions = [
        Transaction(
            type="Subscription",
            amount=1000.0,
            member=users["member_a"],
            reference_id="SUB12345",
            description="Monthly subscription payment",
            created_by=users["member_a"],
        ),
        Transaction(
            type="Loan Repayment",
            amount=1708.33,
            member=users["member_b"],
            reference_id="LOAN98765",
            description="Loan repayment installment",
            created_by=users["member_b"],
        ),
        Transaction(
            type="Rental Deposit",
            amount=500.0,
            member=users["member_c"],
            reference_id="RENT45678",
            description="Rental deposit payment",
            created_by=users["member_c"],
        ),
    ]
    for txn in transactions:
        await txn.insert()


async def seed_audit_logs(users: dict[str, User]) -> None:
    audits = [
        AuditLog(
            action="seed",
            entity_type="User",
            entity_id=str(users["admin"].id),
            performed_by=users["admin"],
            details={"message": "Seed admin created"},
        ),
        AuditLog(
            action="seed",
            entity_type="Loan",
            entity_id="loan-seed-1",
            performed_by=users["treasurer"],
            details={"message": "Seed loan created"},
        ),
        AuditLog(
            action="seed",
            entity_type="InventoryItem",
            entity_id="inventory-seed-1",
            performed_by=users["secretary"],
            details={"message": "Seed inventory item created"},
        ),
    ]
    for audit in audits:
        await audit.insert()


async def seed_all() -> None:
    await init_db()
    await clear_collections()

    users = await seed_users()
    await seed_group_settings()
    items = await seed_inventory_items()
    await seed_rental_bookings(users, items)
    await seed_subscription_payments(users)
    events = await seed_welfare_events(users)
    await seed_event_contributions(events, users)
    await seed_loans(users)
    await seed_transactions(users)
    await seed_audit_logs(users)

    print("Database seeding completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed_all())
