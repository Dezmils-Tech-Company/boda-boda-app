from typing import Type, TypeVar, Generic, List, Optional
from beanie import Document
from pydantic import BaseModel

T = TypeVar("T", bound=Document)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_by_id(self, id: str) -> Optional[T]:
        return await self.model.get(id)

    async def get_all(self) -> List[T]:
        return await self.model.all().to_list()

    async def create(self, data: BaseModel) -> T:
        obj = self.model(**data.dict())
        await obj.insert()
        return obj

    async def update(self, id: str, data: BaseModel) -> Optional[T]:
        obj = await self.model.get(id)
        if obj:
            await obj.update({"$set": data.dict(exclude_unset=True)})
        return obj

    async def delete(self, id: str) -> bool:
        obj = await self.model.get(id)
        if obj:
            await obj.delete()
            return True
        return False