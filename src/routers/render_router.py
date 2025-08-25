from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection

router = APIRouter()


@router.get('/note/{note_id}')
async def get_rendered_note(note_id: int, session: AsyncSession = Depends(Connection.get_session)):
    pass
