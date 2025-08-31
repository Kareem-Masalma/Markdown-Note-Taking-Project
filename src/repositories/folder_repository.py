"""
This module is the repository for the folder to interact with the database. Basic CRUD operations.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.folder import Folder
from src.models.note import Note
from src.repositories.folder_repository_interface import IFolderRepository


class FolderRepository(IFolderRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_folder(self, folder: Folder):
        """
        This method to add new folder to the database.

        :param folder: The folder to be added.
        """
        self.session.add(folder)
        await self.session.commit()

    async def get_all_folders(self) -> list[Folder] | None:
        """
        This method to get all folders from the database where deleted field is set to be 0.

        :return: All folders found inside the database.
        """
        query = (
            select(Folder)
            .where(Folder.deleted == 0)
        )
        res = await self.session.execute(query)
        folders = res.scalars().all()
        return folders

    async def get_folder_by_id(self, folder_id: int) -> Folder | None:
        """
        This method to get a folder by id from the database.

        :param folder_id: The id of the folder to get.
        :return: The folder if found in the database.
        """
        query = (
            select(Folder)
            .where((Folder.deleted == 0) & (Folder.id == folder_id))
            .options(selectinload(Folder.parent))
        )
        res = await self.session.execute(query)
        folder = res.scalars().first()
        return folder

    async def rename_folder(self, stored_folder: Folder, name: str):
        """
        This method to update a folder inside the database.

        :param stored_folder: The folder to be updated.
        :param name: The new name for the folder.
        """
        try:
            stored_folder.name = name
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete_folder(self, folder_id: int):
        """
        This method to delete a folder from the database if found.

        :param folder_id: The id of the folder to be deleted.
        """
        try:
            folder = await self.get_folder_by_id(folder_id)
            folder.deleted = 1
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_folder_notes(self, folder_id):
        """
        This method to get all notes inside a folder by their parent(folder) id.

        :param folder_id: The id of the folder which its children notes are requested.
        :return: All the child notes of the folder.
        """
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
        notes = res.scalars().all()
        return notes

    async def get_folder_by_name_parent(self, folder_name: str, parent_id: int):
        query = (
            select(Folder)
            .where((Folder.name == folder_name) & (Folder.parent_id == parent_id))
        )
        res = await self.session.execute(query)
        folder = res.scalars().first()
        return folder
