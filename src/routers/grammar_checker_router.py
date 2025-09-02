from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.models.history import History
from src.models.user import User
from src.repositories.history_repository import HistoryRepository
from src.repositories.issue_repositoy import IssueRepository
from src.schemas.history_schema import HistoryOut
from src.services.issue_service import IssueService
from src.services.languagetool_service import LanguageToolService

router = APIRouter()


@router.get(
    "/version/{version_id}",
    summary="Check the grammar of a note",
    description="This endpoint checks the grammar of a specific version of a note",
    response_description="The returned data is the issues if found",
    responses={
        200: {"description": "The note successfully checked"},
        304: {"description": "Note not modified"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
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
                await issue_service.create_issue(issue, version_id)

        return issues
    except Exception as e:
        raise e


@router.get(
    "/fix/issue/{issue_id}",
    summary="Fix grammar issue",
    description="This endpoint fixes a grammar issue from the database",
    response_model=HistoryOut,
    response_description="The returned data is the fixed version",
    responses={
        200: {"description": "The issue successfully fixed."},
        404: {"description": "Issue is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def fix_issue(
    issue_id: int,
    user: User = Depends(check_token),
    session: AsyncSession = Depends(Connection.get_session),
):
    issue_service = IssueService(IssueRepository(session))
    version: History = await issue_service.fix_issue(issue_id)
    return version
