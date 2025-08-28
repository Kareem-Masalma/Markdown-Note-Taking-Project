"""
This module is the methods used to handle notes endpoint operations, get note by id, get all notes,
delete note, update note, add new note.
"""

from fastapi import HTTPException

from src.models.note import Note
from src.repositories.note_repository import NoteRepository
from src.schemas.folder_schema import ParentOut
from src.schemas.note_schema import NoteUpdate, NoteIn, NoteOut
from src.schemas.tag_schema import TagOut


class NoteService:

    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def get_all_notes(self) -> list[NoteOut] | None:
        """
        This method is used to get all available notes inside the database with deleted field set to 0,
        it returns all notes if found, else it raises 404 HTTPException.

        :return: The returned value is a list of notes if found.
        """
        notes: list[Note] | None = await self.note_repository.get_all_notes()
        if not notes:
            raise HTTPException(status_code=404, detail="No notes are found")

        return [
            NoteOut(
                id=note.id,
                title=note.title,
                content=note.content,
                username=note.user.username,
                parent=ParentOut(id=note.parent.id, name=note.parent.name),
                tags=[TagOut(id=tag.id, name=tag.name) for tag in note.tags],
            )
            for note in notes
        ]

    async def get_note_by_note_id(self, note_id: int) -> NoteOut | None:
        """
        This method is used to get an available note with deleted field set to 0 by their note_id,
        it returns the note if found, else it raises a 404 HTTPException.
        :param note_id: The id of the note to be found.
        :return: The note's data.
        """
        note: Note | None = await self.note_repository.get_note_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

        note_out = NoteOut(
            id=note.id,
            title=note.title,
            content=note.content,
            username=note.user.username,
            parent=ParentOut(id=note.parent.id, name=note.parent.name),
            tags=[TagOut(id=tag.id, name=tag.name) for tag in note.tags],
        )
        return note_out

    async def update_note(self, note_id: int, note: NoteUpdate) -> NoteOut:
        """
        This method is used to update an available note from database with deleted field set to 0,
        exclude_unset is set to be True, which removes the empty fields that aren't meant to be updated.

        :param note_id: The id of the note to be updated.
        :param note: New note's data to update.
        :return: The update note, if not found it raised 404 HTTPException.
        """

        stored_note = await self.note_repository.get_note_by_id(note_id)

        if not stored_note:
            raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

        await self.note_repository.update_note(stored_note, note)

        return NoteOut(
            id=updated_note.id,
            title=updated_note.title,
            content=updated_note.content,
            username=updated_note.user.username,
            parent=ParentOut(id=updated_note.parent.id, name=updated_note.parent.name),
            tags=[TagOut(id=tag.id, name=tag.name) for tag in updated_note.tags],
        )

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

        new_note = Note(title=note.title, content=note.content, user_id=note.user_id, parent_id=note.parent_id)

        await self.note_repository.add_new_note(new_note)

        tags = note.tag_ids
        if tags:
            for tag in tags:
                await self.note_repository.add_tag_note(new_note.id, tag)

        return {
            "details": "note is added successfully",
            "user": {"id": new_note.id, "title": new_note.title},
        }

    async def get_user_notes(self, user_id: int) -> list[NoteOut]:
        notes: list[Note] | None = await self.note_repository.get_user_notes(user_id)
        if not notes:
            raise HTTPException(status_code=404, detail="No notes are found")

        return [
            NoteOut(
                id=note.id,
                title=note.title,
                content=note.content,
                username=note.user.username,
                parent=ParentOut(id=note.parent.id, name=note.parent.name),
                tags=[TagOut(id=tag.id, name=tag.name) for tag in note.tags],
            )
            for note in notes
        ]
