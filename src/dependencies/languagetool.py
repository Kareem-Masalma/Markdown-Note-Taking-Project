from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.history import HistoryRepository
from src.repositories.issue import IssueRepository
from src.services.issue import IssueService
from src.services.languagetool import LanguageToolService


def get_languagetool_service(
    session: AsyncSession = Depends(Connection.get_session),
) -> LanguageToolService:
    history_repository: HistoryRepository = HistoryRepository(session)
    issue_service: IssueService = IssueService(
        IssueRepository(session), history_repository
    )
    languagetool_service: LanguageToolService = LanguageToolService(
        history_repository, issue_service
    )

    return languagetool_service
