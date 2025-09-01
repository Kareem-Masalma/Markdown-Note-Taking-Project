from abc import ABC, abstractmethod

from src.models.history import History


class IHistoryRepository(ABC):

    @abstractmethod
    async def create_new_history_version(self, history: History):
        pass

    @abstractmethod
    async def get_version_by_id(self, version_id: int):
        pass

    @abstractmethod
    async def get_all_note_versions(self, note_id: int):
        pass
