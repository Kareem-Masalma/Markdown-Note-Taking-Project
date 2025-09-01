from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.history import History
from src.repositories.history_repository_interface import IHistoryRepository


class HistoryRepository(IHistoryRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_history_version(self, history: History):
        try:
            self.session.add(history)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_version_by_id(self, version_id: int):
        try:
            query = select(History).where(History.id == version_id)
            res = await self.session.execute(query)
            version = res.scalars().first()
            return version
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_all_note_versions(self, note_id: int):
        try:
            query = select(History).where(History.note_id == note_id)
            res = await self.session.execute(query)
            versions = res.scalars().all()
            return versions
        except Exception as e:
            await self.session.rollback()
            raise e
