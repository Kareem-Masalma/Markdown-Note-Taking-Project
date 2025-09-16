from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.folder import Folder
from src.models.note import Note
from src.repositories.base_repository import BaseRepository


class FolderRepository(BaseRepository[Folder]):
    def __init__(self, session):
        super().__init__(session, Folder)

    async def rename_folder(self, stored_folder: Folder, new_name: str) -> Folder:
        stored_folder.name = new_name
        await self.session.commit()
        await self.session.refresh(stored_folder)
        return stored_folder

    async def get_folder_by_name_parent(
        self, folder_name: str, parent_id: int
    ) -> Optional[Folder]:
        query = select(Folder).where(
            (Folder.name == folder_name) & (Folder.parent_id == parent_id)
        )
        res = await self.session.execute(query)
        return res.scalars().first()
