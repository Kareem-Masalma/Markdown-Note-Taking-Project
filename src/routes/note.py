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
from src.dependencies.note import get_note_service
from src.models.user import User
from src.repositories.history import HistoryRepository
from src.repositories.note import NoteRepository
from src.schemas.folder import ParentResponse
from src.schemas.note import NoteResponse, NoteRequest, NoteUpdate
from src.schemas.tag import TagResponse
from src.services.history import HistoryService
from src.services.note import NoteService

router = APIRouter(dependencies=[Depends(check_token)])


@router.get(
    "/",
    summary="Get all notes",
    description="This endpoint returns all notes available inside the database",
    response_model=list[NoteResponse],
    response_description="The returned data are all the notes available inside the database",
    responses={
        200: {"description": "All notes returned successfully"},
        404: {"description": "No notes are found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_all_notes(note_service: NoteService = Depends(get_note_service)):
    """
    This method is to get all notes in the database, where deleted field is set to be 0.

    :param note_service: The note service to be used to get all notes.
    :return: The returned value is a list of all available notes inside the database.
    """
    notes = await note_service.get_all_notes()
    return notes


@router.get(
    "/{note_id}",
    summary="Get note by its id",
    description="This endpoint return a note if available inside the database",
    response_model=NoteResponse,
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
    note_service: NoteService = Depends(get_note_service),
):
    """
    This method to get a note by its id.

    :param note_id: The id of the note to be found.
    :param response: The response to be sent.
    :param if_none_match: The value of the previous etag, checked with current content of note.
    :param note_service: The note service to be used to get the note.
    :return: The note requested.
    """
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
    response_model=list[NoteResponse],
    response_description="The returned data is a list of notes",
    responses={
        200: {"description": "All notes returned successfully"},
        404: {"description": "No notes are found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_users_notes(
    user_id: int,
    note_service: NoteService = Depends(get_note_service),
):
    """
    This endpoint get all the user's notes available in the database with deleted field set to 0.

    :param user_id: The id of the user to get their notes.

    :param note_service: The note service to be used to get the user's notes.
    :return: The returned value is the notes of a certain user.
    """
    notes = await note_service.get_user_notes(user_id)
    return notes


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
    note: NoteRequest,
    note_service: NoteService = Depends(get_note_service),
):
    """
    This method adds new note to the database.

    :param note: The note to be added.
    :param note_service: The note service to be used to add the new note.
    :return: The note added.
    """

    note = await note_service.add_new_note(note)
    return note


@router.patch(
    "/{note_id}",
    summary="Update note",
    description="This endpoint updates a note by its id.",
    response_model=NoteResponse,
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
    note_service: NoteService = Depends(get_note_service),
):
    """
    This endpoint to update available note's data, the note shall be available if not HTTPException 404 is raised.

    :param note_id: The id of the note to be updated.
    :param note: The new data to update the note.
    :param note_service: The note service to be used to update the note.
    :return: The updated note.
    """

    note = await note_service.update_note(note_id, note)
    return note


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
    note_service: NoteService = Depends(get_note_service),
):
    """
    This method to delete a note from the database if available, else it raises a 404 HTTPException.

    :param note_id: The id of the note to be deleted.
    :param note_service: The note service to be used to delete the note.
    :return: Successful message.
    """

    note = await note_service.delete_note(note_id)
    return note
