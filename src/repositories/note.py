from typing import List, Optional
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload

from src.models.note import Note
from src.models.note_tag import note_tags
from src.schemas.note import NoteUpdate
from src.repositories.base_repository import BaseRepository, T


class NoteRepository(BaseRepository[Note]):
    def __init__(self, session):
        super().__init__(session, Note)

    async def get_by_id(self, note_id: int) -> Optional[Note]:
        query = (
            select(Note)
            .where((Note.deleted == 0) & (Note.id == note_id))
            .options(
                selectinload(Note.parent),
                selectinload(Note.tags),
                selectinload(Note.user),
            )
        )
        res = await self.session.execute(query)
        note = res.scalars().first()
        return note

    async def get_all(self) -> List[T]:
        """
        This method to get all note from the database where deleted field is set to be 0.

        :return: All notes found inside the database.
        """
        query = (
            select(Note)
            .where(Note.deleted == 0)
            .options(
                selectinload(Note.parent),
                selectinload(Note.tags),
                selectinload(Note.user),
            )
        )
        res = await self.session.execute(query)
        notes = res.scalars().all()
        return notes

    async def update_note(self, stored_note: Note, note: NoteUpdate) -> Note:
        update_data = note.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(stored_note, field, value)

        await self.session.commit()
        await self.session.refresh(stored_note)
        return stored_note

    async def get_user_notes(self, user_id: int) -> List[Note]:
        query = (
            select(Note)
            .where((Note.deleted == 0) & (Note.user_id == user_id))
            .options(
                selectinload(Note.parent),
                selectinload(Note.tags),
                selectinload(Note.user),
            )
        )
        res = await self.session.execute(query)
        return res.scalars().all()

    async def add_tag_note(self, note_id: int, tag_id: int) -> None:
        stmt = insert(note_tags).values(note_id=note_id, tag_id=tag_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_folder_notes(self, folder_id: int):
        stmt = (
            update(Note)
            .where(Note.parent_id == folder_id)
            .values(deleted=1)
        )
        await self.session.execute(stmt)
        await self.session.commit()


    async def get_folder_notes(self, folder_id: int) -> List[Note]:
        query = (
            select(Note)
            .where((Note.deleted == 0) & (Note.parent_id == folder_id))
            .options(
                selectinload(Note.parent),
                selectinload(Note.tags),
                selectinload(Note.user),
            )
        )
        res = await self.session.execute(query)
        return res.scalars().all()
