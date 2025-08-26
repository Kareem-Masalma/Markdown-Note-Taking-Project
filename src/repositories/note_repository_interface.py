from abc import ABC, abstractmethod

from src.models.note import Note
from src.schemas.note_schema import NoteIn


class INoteRepository(ABC):
    @abstractmethod
    async def add_new_note(self, note: Note):
        pass

    @abstractmethod
    async def get_all_notes(self) -> list[Note] | None:
        pass

    @abstractmethod
    async def get_note_by_id(self, note_id: int) -> Note | None:
        pass

    @abstractmethod
    async def update_note(self, note_id: int, stored_note: Note, note: NoteIn):
        pass

    @abstractmethod
    async def delete_note(self, note_id: int):
        pass
