from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.history import History
from src.repositories.base_repository import BaseRepository


class HistoryRepository(BaseRepository[History]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, History)

    async def get_all_note_versions(self, note_id: int) -> list[History]:
        res = await self.session.execute(
            select(History).where(History.note_id == note_id)
        )
        return res.scalars().all()

    async def update_version(self, version: History):
        await self.session.commit()
        await self.session.refresh(version)
