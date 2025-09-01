from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.issue import Issue


class IssueRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_issue(self, issue: Issue):
        try:
            self.session.add(issue)
            await self.session.commit()

        except Exception as e:
            raise e

    async def get_issue_by_id(self, issue_id: int):
        try:
            query = select(Issue).where(Issue.id == issue_id)
            res = await self.session.execute(query)
            issue: Issue = res.scalars().first()

        except Exception as e:
            raise e

    async def get_version_issues(self, version_id):
        try:
            query = select(Issue).where(Issue.version_id == version_id)
            res = await self.session.execute(query)
            issue: Issue = res.scalars().first()

        except Exception as e:
            raise e
