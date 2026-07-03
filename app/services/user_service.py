from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import get_password_hash

async def create_user(user_data: UserCreate):
    existing = await User.find_one(User.phone == user_data.phone)
    if existing:
        raise ValueError("A user with this phone already exists")

    user_dict = user_data.dict()
    pin = user_dict.pop("pin", None)
    if not pin:
        raise ValueError("PIN is required")

    user_dict["hashed_password"] = get_password_hash(pin)
    user = User(**user_dict)
    await user.insert()
    return user

async def get_user_by_phone(phone: str):
    return await User.find_one(User.phone == phone)

async def get_all_users():
    return await User.all().to_list()

async def update_user(user_id: str, update_data: UserUpdate):
    user = await User.get(user_id)
    if user:
        await user.update({"$set": update_data.dict(exclude_unset=True)})
    return user