from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.models.user import User
from src.repositories.history_repository import HistoryRepository
from src.schemas.history_schema import HistoryOut
from src.services.history_service import HistoryService

router = APIRouter()


@router.get(
    "/{note_id}",
    summary="Get note's history  by its id",
    description="This endpoint returns note's history if available inside the database",
    response_model=list[HistoryOut],
    response_description="The returned data is the history of a note",
    responses={
        200: {"description": "All note's history is returned successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_note_history(
    note_id: int,
    user: User = Depends(check_token),
    session: AsyncSession = Depends(Connection.get_session),
):
    """
    This endpoint to get the history and all the previous versions of a certain note.

    :param note_id: The id of the note to get its history.
    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: The history of the note.
    """
    history_service = HistoryService(HistoryRepository(session))
    versions = await history_service.get_note_versions(note_id)
    return versions


@router.get(
    "/version/{version_id}",
    summary="Get note's version",
    description="This endpoint return a version of a note if available inside the database",
    response_model=HistoryOut,
    response_description="The returned data is a version of a note",
    responses={
        200: {"description": "The requested note's history returned successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_note_old_version(
    version_id: int,
    user: User = Depends(check_token),
    session: AsyncSession = Depends(Connection.get_session),
):
    """
    This endpoint returns a certain version of a note from its history.

    :param version_id: The id of the version to be found.
    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: A certain version of a certain note.
    """
    history_service = HistoryService(HistoryRepository(session))
    version = await history_service.get_version_by_id(version_id)
    return version