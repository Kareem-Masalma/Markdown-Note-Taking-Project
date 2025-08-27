"""
This module is the methods used to handle notes endpoint operations, get note by id, get all notes,
delete note, update note, add new note.
"""

from fastapi import HTTPException

from src.models.note import Note
from src.repositories.note_repository import NoteRepository
from src.schemas.note_schema import NoteUpdate, NoteIn


class UserService:

    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def get_all_notes(self) -> list[Note] | None:
        """
        This method is used to get all available notes inside the database with deleted field set to 0,
        it returns all notes if found, else it raises 404 HTTPException.

        :return: The returned value is a list of notes if found.
        """
        notes: list[Note] | None = await self.note_repository.get_all_notes()
        if not notes:
            raise HTTPException(status_code=404, detail="No notes are found")
        return notes

    async def get_note_by_note_id(self, note_id: int) -> Note | None:
        """
        This method is used to get an available note with deleted field set to 0 by their note_id,
        it returns the note if found, else it raises a 404 HTTPException.
        :param note_id: The id of the note to be found.
        :return: The note's data.
        """
        note: Note | None = await self.note_repository.get_note_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

        return note

    async def update_note(self, note_id: int, note: NoteUpdate):
        """
        This method is used to update an available note from database with deleted field set to 0,
        exclude_unset is set to be True, which removes the empty fields that aren't meant to be updated.

        :param note_id: The id of the note to be updated.
        :param note: New note's data to update.
        :return: The update note, if not found it raised 404 HTTPException.
        """

        stored_note = await self.note_repository.get_note_by_id(note_id)

        if not note_id:
            raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

        await self.note_repository.update_note(stored_note, note)

        return note

    async def delete_note(self, note_id: int):
        """
        This method to delete an available note from database with deleted fild set to 1, this method softly deletes the
        user, which means the note is not removed from the database, but the deleted field will be set to 1.

        :param note_id: The id of the note to be deleted.
        :return: True on Success, else it raised 404 HTTPException.
        """
        await self.note_repository.delete_note(note_id)
        return True

    async def add_new_note(self, note: NoteIn):
        """
        This method to add new note to the database.

        :param note: The new note information.
        :return: The new note created.
        """

        new_note = Note(note.title, note.content, note.user_id, note.parent_id)

        await self.note_repository.add_new_note(new_note)

        return {
            "details": "user is registers",
            "user": {"name": new_note.id, "title": new_note.title},
        }
