from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.history import HistoryRepository
from src.repositories.issue import IssueRepository
from src.services.issue import IssueService


def get_issue_service(
    session: AsyncSession = Depends(Connection.get_session),
) -> IssueService:
    issue_repository: IssueRepository = IssueRepository(session)
    history_repository: HistoryRepository = HistoryRepository(session)
    issue_service = IssueService(issue_repository, history_repository)
    return issue_service
