from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_phone(self, phone: str):
        return await User.find_one(User.phone == phone)

    async def get_all_active(self):
        return await User.find(User.status == "Active").to_list()

    async def create_user(self, user_data: UserCreate):
        user = User(**user_data.dict())
        await user.insert()
        return user