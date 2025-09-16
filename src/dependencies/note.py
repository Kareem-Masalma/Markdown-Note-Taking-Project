from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.history import HistoryRepository
from src.repositories.note import NoteRepository
from src.services.history import HistoryService
from src.services.note import NoteService


def get_note_service(
    session: AsyncSession = Depends(Connection.get_session),
) -> NoteService:
    note_repository: NoteRepository = NoteRepository(session)
    history_service = HistoryService(HistoryRepository(session))
    note_service = NoteService(note_repository, history_service)
    return note_service
