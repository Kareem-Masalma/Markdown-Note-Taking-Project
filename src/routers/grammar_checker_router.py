from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.models.user import User
from src.repositories.history_repository import HistoryRepository
from src.repositories.issue_repositoy import IssueRepository
from src.services.issue_service import IssueService
from src.services.languagetool_service import LanguageToolService

router = APIRouter()


@router.get("/version/{version_id}")
async def check_version_grammar(
        version_id: int,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    try:
        language_tool_service = LanguageToolService(HistoryRepository(session))
        issues = await language_tool_service.check_grammar(version_id)
        if issues and len(issues) > 0:
            issue_service = IssueService(IssueRepository(session))
            for issue in issues:
                await issue_service.create_issue(issue)

        return issues
    except Exception as e:
        raise e
