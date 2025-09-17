from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.note import NoteRepository
from src.services.summarization import SummarizeNotes


def get_summarization_service(session: AsyncSession = Depends(Connection.get_session)):
    note_repository = NoteRepository(session)
    summarize_service = SummarizeNotes(note_repository)
    return summarize_service
