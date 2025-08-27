"""
This module is the repository for the note to interact with the database. Basic CRUD operations.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.note import Note
from src.repositories.note_repository_interface import INoteRepository
from src.schemas.note_schema import NoteIn, NoteUpdate


class NoteRepository(INoteRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_new_note(self, note: Note):
        """
        This method to add new note to the database.

        :param note: The note to be added.
        """
        self.session.add(note)
        await self.session.commit()

    async def get_all_notes(self) -> list[Note] | None:
        """
        This method to get all note from the database where deleted field is set to be 0.

        :return: All notes found inside the database.
        """
        res = await self.session.execute(select(Note).where(Note.deleted == 0))
        notes: list[Note] = res.scalars().all()
        return notes

    async def get_note_by_id(self, note_id: int) -> Note | None:
        """
        This method to get a note by id from the database.

        :param note_id: The id of the note to get.
        :return: The note if found in the database.
        """
        res = await self.session.execute(
            select(Note).where((Note.id == note_id) & (Note.deleted == 0))
        )
        note = res.scalars().first()
        return note

    async def update_note(self, stored_note: Note, note: NoteUpdate):
        """
        This method to update a note inside the database.

        :param stored_note: The note to be updated.
        :param note: The new data to update.
        """
        try:
            update_data = note.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(stored_note, field, value)

            await self.session.commit()
            await self.session.refresh(note)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete_note(self, note_id: int):
        """
        This method to delete a note from the database if found.
        :param note_id: The id of the note to be deleted.
        """
        try:
            note = await self.get_note_by_id(note_id)
            note.deleted = 1
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
