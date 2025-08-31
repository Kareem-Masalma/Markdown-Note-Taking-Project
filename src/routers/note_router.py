"""
This module is the FastAPI Router for notes related endpoints,
it manages CRUD operations for notes. Add new note, delete
available note, update note's data, and read available notes from
database.
"""

from fastapi import APIRouter, Depends, Response, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.common.utils.generate_etag import generate_etag
from src.models.user import User
from src.repositories.note_repository import NoteRepository
from src.schemas.note_schema import NoteOut, NoteIn, NoteUpdate
from src.services.note_service import NoteService

router = APIRouter()


@router.get(
    "/",
    summary="Get all notes",
    description="This endpoint returns all notes available inside the database",
    response_model=list[NoteOut],
    response_description="The returned data are all the notes available inside the database",
    responses={
        200: {"description": "All notes returned successfully"},
        404: {"description": "No notes are found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_all_notes(
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    """
    This method is to get all notes in the database, where deleted field is set to be 0.

    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: The returned value is a list of all available notes inside the database.
    """
    note_service = NoteService(NoteRepository(session))
    notes = await note_service.get_all_notes()
    return notes


@router.get(
    "/{note_id}",
    summary="Get note by its id",
    description="This endpoint return a note if available inside the database",
    response_model=NoteOut,
    response_description="The returned data is the requested note",
    responses={
        200: {"description": "The note requested returned successfully"},
        304: {"description": "Note not modified"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_note_by_id(
        note_id: int,
        response: Response,
        if_none_match: str | None = Header(default=None),
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    """
    This method to get a note by its id.

    :param note_id: The id of the note to be found.
    :param response: The response to be sent.
    :param if_none_match: The value of the previous etag, checked with current content of note.
    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: The note requested.
    """
    note_service = NoteService(NoteRepository(session))
    note = await note_service.get_note_by_note_id(note_id)
    etag = generate_etag(note.content)
    response.headers["ETag"] = etag

    if etag == if_none_match:
        raise HTTPException(status_code=304, detail="Not modified")

    return note


@router.get(
    "/user/{user_id}",
    summary="Get all notes for a certain user",
    description="This endpoint return a all notes of a user if available inside the database",
    response_model=list[NoteOut],
    response_description="The returned data is a list of notes",
    responses={
        200: {"description": "All notes returned successfully"},
        404: {"description": "No notes are found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_users_notes(
        user_id: int,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    """
    This endpoint get all the user's notes available in the database with deleted field set to 0.

    :param user_id: The id of the user to get their notes.
    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: The returned value is the notes of a certain user.
    """
    note_service = NoteService(NoteRepository(session))
    notes = await note_service.get_user_notes(user_id)
    return notes


@router.get(
    "/history/{note_id}",
    summary="Get note's history  by its id",
    description="This endpoint returns note's history if available inside the database",
    response_model=list[NoteOut],
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
    pass


@router.get(
    "/history/{note_id}/{history_id}",
    summary="Get note's version",
    description="This endpoint return a version of a note if available inside the database",
    response_model=NoteOut,
    response_description="The returned data is a version of a note",
    responses={
        200: {"description": "The requested note's history returned successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_note_old_version(
        note_id: int,
        history_id: int,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    """
    This endpoint returns a certain version of a note from its history.

    :param note_id: The id of the note to be found.
    :param history_id: The id of the version to be found.
    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: A certain version of a certain note.
    """
    pass


@router.post(
    "/",
    summary="Add new note",
    description="This endpoint adds new note to the database",
    response_description="The returned data is the added note",
    responses={
        201: {"description": "The note is added successfully"},
    },
    status_code=status.HTTP_201_CREATED,
)
async def add_new_note(
        note: NoteIn,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    """
    This method adds new note to the database.

    :param note: The note to be added.
    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: The note added.
    """
    try:
        note_service = NoteService(NoteRepository(session))
        note = await note_service.add_new_note(note)
        return note
    except Exception as e:
        await session.rollback()
        raise e


@router.patch(
    "/{note_id}",
    summary="Update note",
    description="This endpoint updates a note by its id.",
    response_model=NoteOut,
    response_description="The returned data is the updated note",
    responses={
        200: {"description": "The note updated successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def update_note(
        note_id: int,
        note: NoteUpdate,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    """
    This endpoint to update available note's data, the note shall be available if not HTTPException 404 is raised.

    :param note_id: The id of the note to be updated.
    :param note: The new data to update the note.
    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: The updated note.
    """
    try:
        note_service = NoteService(NoteRepository(session))
        note = await note_service.update_note(note_id, note)
        return note
    except Exception as e:
        await session.rollback()
        raise e


@router.delete(
    "/{note_id}",
    summary="Delete a note",
    description="This endpoint deletes a note if available inside the database",
    response_description="A successful message when deleted.",
    responses={
        200: {"description": "The note deleted successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def delete_note(
        note_id: int,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    """
    This method to delete a note from the database if available, else it raises a 404 HTTPException.

    :param note_id: The id of the note to be deleted.
    :param user: Check if the user is authorized to use the endpoint by checking the jwt token sent in the header.
    :param session: This is the async session used to handle the database.
    :return: Successful message.
    """
    try:
        note_service = NoteService(NoteRepository(session))
        return await note_service.delete_note(note_id)
    except Exception as e:
        await session.rollback()
        raise e
