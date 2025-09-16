from fastapi import HTTPException

from src.models.history import History
from src.models.note import Note
from src.repositories.history import HistoryRepository


class HistoryService:
    def __init__(self, history_repository: HistoryRepository):
        self.history_repository = history_repository

    async def create_new_history_version(self, note: Note, message: str):
        """
        This method creates new version of a note and add it to the history database.

        :param note: The note to add.
        :param message: The message of the version.
        :return:
        """
        try:
            history = History(
                note_id=note.id,
                note_title=note.title,
                note_content=note.content,
                rev_description=message,
            )
            await self.history_repository.create(history)
            return history
        except Exception as e:
            raise e

    async def get_version_by_id(self, version_id: int):
        """
        This method get a version of a note by its id.

        :param version_id: The id of the version.
        :return: The version from database if found.
        """
        try:
            history = await self.history_repository.get_version_by_id(version_id)
            if not history:
                raise HTTPException(status_code=404, detail="Version not found")

            return history
        except Exception as e:
            raise e

    async def get_note_versions(self, note_id: int):
        """
        This method gets all versions of a note, by the note id.

        :param note_id: The id of the note to get the versions.
        :return: A list of note versions if found.
        """
        try:
            versions = await self.history_repository.get_all_note_versions(note_id)
            if not versions:
                raise HTTPException(status_code=404, detail="No versions were found")

            return versions
        except Exception as e:
            raise e
