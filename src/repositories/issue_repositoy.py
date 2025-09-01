from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.issue import Issue
from src.repositories.base_repository import BaseRepository


class IssueRepository(BaseRepository[Issue]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Issue)

    async def get_issue_by_id(self, issue_id: int) -> Issue | None:
        return await self.get_by_id(issue_id)

    async def get_version_issues(self, version_id: int) -> list[Issue]:
        res = await self.session.execute(
            select(Issue).where(Issue.version_id == version_id)
        )
        return res.scalars().all()
