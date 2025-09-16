from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.folder import FolderRepository
from src.repositories.note import NoteRepository
from src.services.folder import FolderService


def get_folder_service(
    session: AsyncSession = Depends(Connection.get_session),
) -> FolderService:
    folder_repository: FolderRepository = FolderRepository(session)
    note_repository: NoteRepository = NoteRepository(session)
    folder_service = FolderService(folder_repository, note_repository)
    return folder_service
