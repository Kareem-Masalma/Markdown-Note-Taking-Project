from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.history import History
from src.repositories.base_repository import BaseRepository


class HistoryRepository(BaseRepository[History]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, History)

    async def get_version_by_id(self, version_id: int) -> History | None:
        return await self.get_by_id(version_id)

    async def get_all_note_versions(self, note_id: int) -> list[History]:
        res = await self.session.execute(
            select(History).where(History.note_id == note_id)
        )
        return res.scalars().all()
