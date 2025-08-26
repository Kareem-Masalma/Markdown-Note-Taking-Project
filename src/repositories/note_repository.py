from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.note import Note
from src.repositories.note_repository_interface import INoteRepository
from src.schemas.note_schema import NoteIn


class NoteRepository(INoteRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_new_note(self, note: Note):
        self.session.add(note)
        await self.session.commit()

    async def get_all_notes(self) -> list[Note] | None:
        res = await self.session.execute(select(Note).where(Note.deleted == 0))
        notes: list[Note] = res.scalars().all()
        return notes

    async def get_note_by_id(self, note_id: int) -> Note | None:
        res = await self.session.execute(
            select(Note).where((Note.id == note_id) & (Note.deleted == 0))
        )
        note = res.scalars().first()
        return note

    async def update_note(self, note_id: int, stored_note: Note, note: NoteIn):
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
        try:
            note = await self.get_note_by_id(note_id)
            note.deleted = 1
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
