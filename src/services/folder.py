"""
This module is the methods used to handle folders endpoint operations, get folder by id, get all folders,
delete folder, rename folder, create folder.
"""

from fastapi import HTTPException

from src.models.folder import Folder
from src.models.note import Note
from src.repositories.folder import FolderRepository
from src.repositories.note import NoteRepository
from src.schemas.folder import FolderResponse, FolderRequest, ParentResponse
from src.schemas.note import NoteResponse
from src.schemas.tag import TagResponse


class FolderService:

    def __init__(self, folder_repository: FolderRepository, note_repository: NoteRepository):
        self.folder_repository = folder_repository
        self.note_repository = note_repository

    async def get_all_folders(self) -> list[FolderResponse] | None:
        """
        This method is used to get all available folders inside the database with deleted field set to 0,
        it returns all folders if found, else it raises 404 HTTPException.

        :return: The returned value is a list of folders if found.
        """
        try:
            folders: list[Folder] | None = await self.folder_repository.get_all()
            if not folders:
                raise HTTPException(status_code=404, detail="No folders are found")

            return folders
        except Exception as e:
            raise e

    async def get_folder_by_id(self, folder_id: int) -> FolderResponse | None:
        """
        This method is used to get an available folder with deleted field set to 0 by their folder_id,
        it returns the folder if found, else it raises a 404 HTTPException.

        :param folder_id: The id of the folder to be found.
        :return: The folder's data.
        """
        try:
            folder: Folder | None = await self.folder_repository.get_by_id(folder_id)
            if not folder:
                raise HTTPException(status_code=404, detail=f"Folder not found")

            folder_out = FolderResponse(
                id=folder.id,
                name=folder.name,
                parent=ParentResponse(id=folder.parent.id, name=folder.parent.name),
            )
            return folder_out
        except Exception as e:
            raise e

    async def rename_folder(self, folder_id: int, name: str) -> FolderResponse:
        """
        This method is used to rename an available folder from database with deleted field set to 0.

        :param folder_id: The id of the folder to be updated.
        :param name: New folder's name to update.
        :return: The update folder, if not found it raised 404 HTTPException.
        """
        try:
            stored_folder = await self.folder_repository.get_by_id(folder_id)

            if not stored_folder:
                raise HTTPException(status_code=404, detail=f"Folder not found")

            await self.folder_repository.rename_folder(stored_folder, name)

            folder_out = FolderResponse(
                id=stored_folder.id,
                name=stored_folder.name,
                parent=ParentResponse(
                    id=stored_folder.parent.id, name=stored_folder.parent.name
                ),
            )
            return folder_out
        except Exception as e:
            raise e

    async def delete_folder(self, folder_id: int):
        """
        This method to delete an available folder from database with deleted fild set to 1, this method softly deletes the
        folder, which means the folder is not removed from the database, but the deleted field will be set to 1.

        :param folder_id: The id of the folder to be deleted.
        :return: True on Success, else it raised 404 HTTPException.
        """
        try:
            exists = self.get_folder_by_id(folder_id)

            if not exists:
                raise HTTPException(status_code=404, detail="Folder doesn't exists.")

            await self.folder_repository.delete(folder_id)
            note_repo = NoteRepository(self.folder_repository.session)
            await note_repo.delete_folder_notes(folder_id)
            return True
        except Exception as e:
            raise e

    async def create_folder(self, folder: FolderRequest):
        """
        This method to add new folder to the database.

        :param folder: The new folder information.
        :return: The new folder created.
        """
        try:
            new_folder = Folder(name=folder.name, parent_id=folder.parent)

            exists = await self.check_folder_existence(
                new_folder.name, new_folder.parent_id
            )
            if exists:
                raise HTTPException(status_code=409, detail="Folder already exists.")

            await self.folder_repository.create(new_folder)

            return {
                "details": "Folder is added successfully",
                "folder": {"id": new_folder.id, "title": new_folder.name},
            }
        except Exception as e:
            raise e

    async def get_folder_notes(self, folder_id: int) -> list[NoteResponse]:
        """
        This method to get all notes that belongs to certain folder by its id.

        :param folder_id: The id of the folder to get its notes.
        :return: Folder child notes.
        """
        try:
            notes: list[Note] | None = await self.note_repository.get_folder_notes(
                folder_id
            )
            if not notes:
                raise HTTPException(status_code=404, detail="No notes are found")

            return [
                NoteResponse(
                    id=note.id,
                    title=note.title,
                    content=note.content,
                    username=note.user.username,
                    parent=ParentResponse(id=note.parent.id, name=note.parent.name),
                    tags=[TagResponse(id=tag.id, name=tag.name) for tag in note.tags],
                )
                for note in notes
            ]
        except Exception as e:
            raise e

    async def check_folder_existence(self, folder_name: str, parent_id: int) -> bool:
        """
        This method to check if a folder exists inside a certain parent.

        :param folder_name: The name of the folder.
        :param parent_id: The parent folder.
        :return: If the folder exists or not.
        """
        try:
            exist = await self.folder_repository.get_folder_by_name_parent(
                folder_name, parent_id
            )
            if exist:
                return True
            return False
        except Exception as e:
            raise e
