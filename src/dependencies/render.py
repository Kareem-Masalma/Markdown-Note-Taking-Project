from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.note import NoteRepository
from src.services.render import RenderService


def get_render_service(session: AsyncSession = Depends(Connection.get_session)):
    note_repository: NoteRepository = NoteRepository(session)
    render_service: RenderService = RenderService(note_repository)
    return render_service
