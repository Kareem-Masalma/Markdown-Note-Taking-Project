from fastapi import HTTPException

from src.models.history import History
from src.models.note import Note
from src.repositories.history_repository import HistoryRepository


class HistoryService:
    def __init__(self, history_repository: HistoryRepository):
        self.history_repository = history_repository

    async def create_new_history_version(self, note: Note, message: str):
        try:
            history = History(
                note_id=note.id,
                note_title=note.title,
                note_content=note.content,
                rev_description=message,
            )
            await self.history_repository.create_new_history_version(history)
            return history
        except Exception as e:
            raise e

    async def get_version_by_id(self, version_id: int):
        try:
            history = await self.history_repository.get_version_by_id(version_id)
            if not history:
                raise HTTPException(status_code=404, detail="Version not found")

            return history
        except Exception as e:
            raise e

    async def get_note_versions(self, note_id: int):
        try:

            versions = await self.history_repository.get_all_note_versions(note_id)
            if not versions:
                raise HTTPException(status_code=404, detail="No versions were found")

            return versions
        except Exception as e:
            raise e
