"""
This module is the methods used to handle folders endpoint operations, get folder by id, get all folders,
delete folder, rename folder, create folder.
"""

from fastapi import HTTPException

from src.models.folder import Folder
from src.repositories.folder_repository import FolderRepository
from src.schemas.folder_schema import FolderOut, FolderIn, ParentOut


class FolderService:

    def __init__(self, folder_repository: FolderRepository):
        self.folder_repository = folder_repository

    async def get_all_folders(self) -> list[FolderOut] | None:
        """
        This method is used to get all available folders inside the database with deleted field set to 0,
        it returns all folders if found, else it raises 404 HTTPException.

        :return: The returned value is a list of folders if found.
        """
        folders: list[Folder] | None = await self.folder_repository.get_all_folders()
        if not folders:
            raise HTTPException(status_code=404, detail="No folders are found")

        return folders

    async def get_folder_by_id(self, folder_id: int) -> FolderOut | None:
        """
        This method is used to get an available folder with deleted field set to 0 by their folder_id,
        it returns the folder if found, else it raises a 404 HTTPException.

        :param folder_id: The id of the folder to be found.
        :return: The folder's data.
        """
        folder: Folder | None = await self.folder_repository.get_folder_by_id(folder_id)
        if not folder:
            raise HTTPException(status_code=404, detail=f"Folder not found")

        folder_out = FolderOut(
            id=folder.id,
            name=folder.name,
            parent=ParentOut(id=folder.parent.id, name=folder.parent.name)
        )
        return folder_out

    async def rename_folder(self, folder_id: int, name: str) -> FolderOut:
        """
        This method is used to rename an available folder from database with deleted field set to 0.

        :param folder_id: The id of the folder to be updated.
        :param name: New folder's name to update.
        :return: The update folder, if not found it raised 404 HTTPException.
        """

        stored_folder = await self.folder_repository.get_folder_by_id(folder_id)

        if not stored_folder:
            raise HTTPException(status_code=404, detail=f"Folder not found")

        await self.folder_repository.rename_folder(stored_folder, name)

        folder_out = FolderOut(
            id=folder.id,
            name=folder.name,
            parent=ParentOut(id=folder.parent.id, name=folder.parent.name)
        )
        return folder_out

    async def delete_folder(self, folder_id: int):
        """
        This method to delete an available folder from database with deleted fild set to 1, this method softly deletes the
        folder, which means the folder is not removed from the database, but the deleted field will be set to 1.

        :param folder_id: The id of the folder to be deleted.
        :return: True on Success, else it raised 404 HTTPException.
        """
        await self.folder_repository.delete_folder(folder_id)
        return True

    async def create_folder(self, folder: FolderIn):
        """
        This method to add new folder to the database.

        :param folder: The new folder information.
        :return: The new folder created.
        """

        new_folder = Folder(
            name=folder.name, parent_id=folder.parent
        )

        await self.folder_repository.create_folder(new_folder)

        return {
            "details": "Folder is added successfully",
            "folder": {"id": new_folder.id, "title": new_folder.name},
        }
