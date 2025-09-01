from typing import TypeVar, Generic, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Generic repository with basic CRUD for soft-deletable models"""

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session: AsyncSession = session
        self.model: type[T] = model

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_all(self) -> List[T]:
        query = select(self.model).where(self.model.deleted == 0)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        query = select(self.model).where(
            (self.model.deleted == 0) & (self.model.id == obj_id)
        )
        res = await self.session.execute(query)
        return res.scalars().first()

    async def delete(self, obj_id: int) -> bool:
        obj = await self.get_by_id(obj_id)
        if obj:
            obj.deleted = 1
            await self.session.commit()
            return True
        return False
