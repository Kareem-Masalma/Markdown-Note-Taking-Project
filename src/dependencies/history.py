from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.history import HistoryRepository
from src.services.history import HistoryService


def get_history_service(
    session: AsyncSession = Depends(Connection.get_session),
) -> HistoryService:
    history_repository: HistoryRepository = HistoryRepository(session)
    history_service = HistoryService(history_repository)
    return history_service
