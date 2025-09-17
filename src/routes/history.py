from fastapi import APIRouter, Depends, status

from src.auth.tokens import check_token
from src.dependencies.history import get_history_service
from src.dependencies.issue import get_issue_service
from src.models.issue import Issue
from src.schemas.history import HistoryResponse
from src.services.history import HistoryService
from src.services.issue import IssueService

router = APIRouter(dependencies=[Depends(check_token)])


@router.get(
    "/{note_id}",
    summary="Get note's history  by its id",
    description="This endpoint returns note's history if available inside the database",
    response_model=list[HistoryResponse],
    response_description="The returned data is the history of a note",
    responses={
        200: {"description": "All note's history is returned successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_note_history(
    note_id: int, history_service: HistoryService = Depends(get_history_service)
):
    """
    This endpoint to get the history and all the previous versions of a certain note.

    :param note_id: The id of the note to get its history.
    :param history_service: The service to operate logic for history.
    :return: The history of the note.
    """
    versions = await history_service.get_note_versions(note_id)
    return versions


@router.get(
    "/version/{version_id}",
    summary="Get note's version",
    description="This endpoint return a version of a note if available inside the database",
    response_model=HistoryResponse,
    response_description="The returned data is a version of a note",
    responses={
        200: {"description": "The requested note's history returned successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_note_old_version(
    version_id: int, history_service: HistoryService = Depends(get_history_service)
):
    """
    This endpoint returns a certain version of a note from its history.

    :param version_id: The id of the version to be found.
    :param history_service: The service to operate logic for history.
    :return: A certain version of a certain note.
    """
    version = await history_service.get_version_by_id(version_id)
    return version


@router.get(
    "/version/issues/{issue_id}",
    summary="Get version's issues",
    description="This endpoint returns the issues of a version from database if found",
    response_description="The returned data is the issues of a version",
    responses={
        200: {"description": "The requested note's history returned successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_version_issues(
    version_id: int, issue_service: IssueService = Depends(get_issue_service)
):
    """
    This endpoint returns issues of a certain version.

    :param version_id: The id of the version to be found.
    :param issue_service: The service to operate logic for history.
    :return: A certain version of a certain note.
    """
    issues: list[Issue] = await issue_service.version_issues(version_id)
    return issues
