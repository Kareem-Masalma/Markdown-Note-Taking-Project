from abc import ABC, abstractmethod

from src.models.folder import Folder


class IFolderRepository(ABC):

    @abstractmethod
    async def create_folder(self, folder: Folder):
        pass

    @abstractmethod
    async def get_all_folders(self) -> list[Folder] | None:
        pass

    @abstractmethod
    async def get_folder_by_id(self, folder_id: int) -> Folder | None:
        pass

    @abstractmethod
    async def rename_folder(self, stored_folder: Folder, name: str):
        pass

    @abstractmethod
    async def delete_folder(self, folder_id: int):
        pass
