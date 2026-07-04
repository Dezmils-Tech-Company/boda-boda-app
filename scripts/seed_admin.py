import asyncio
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.database import init_db
from app.models.user import User
from app.services.auth_service import get_password_hash


async def seed_admin() -> None:
    await init_db()

    phone = os.getenv("ADMIN_PHONE")
    pin = os.getenv("ADMIN_PIN")
    full_name = os.getenv("ADMIN_NAME", "Admin")

    if not phone or not pin:
        raise RuntimeError("ADMIN_PHONE and ADMIN_PIN must be set in the environment")

    existing = await User.find_one(User.phone == phone)
    if existing:
        existing.full_name = full_name
        existing.role = "Admin"
        existing.hashed_password = get_password_hash(pin)
        existing.status = "Active"
        await existing.save()
        print(f"Updated existing admin user: {phone}")
        return

    user = User(
        phone=phone,
        full_name=full_name,
        hashed_password=get_password_hash(pin),
        role="Admin",
        status="Active",
    )
    await user.insert()
    print(f"Created admin user: {phone}")


if __name__ == "__main__":
    asyncio.run(seed_admin())
