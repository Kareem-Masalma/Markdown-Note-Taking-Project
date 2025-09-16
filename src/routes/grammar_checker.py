from fastapi import APIRouter, Depends, status

from src.auth.tokens import check_token
from src.dependencies.issue import get_issue_service
from src.dependencies.languagetool import get_languagetool_service
from src.models.history import History
from src.schemas.history import HistoryResponse
from src.services.issue import IssueService
from src.services.languagetool import LanguageToolService

router = APIRouter(dependencies=[Depends(check_token)])


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
    language_tool_service: LanguageToolService = Depends(get_languagetool_service),
):

    issues = await language_tool_service.check_grammar(version_id)
    return issues


@router.get(
    "/fix/issue/{issue_id}",
    summary="Fix grammar issue",
    description="This endpoint fixes a grammar issue from the database",
    response_model=HistoryResponse,
    response_description="The returned data is the fixed version",
    responses={
        200: {"description": "The issue successfully fixed."},
        404: {"description": "Issue is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def fix_issue(
    issue_id: int, issue_service: IssueService = Depends(get_issue_service)
):
    version: History = await issue_service.fix_issue(issue_id)
    return version
