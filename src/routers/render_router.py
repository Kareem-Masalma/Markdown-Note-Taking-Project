from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.models.user import User

router = APIRouter()


@router.get("/note/{note_id}")
async def get_rendered_note(
        note_id: int, user: User = Depends(check_token), session: AsyncSession = Depends(Connection.get_session)
):
    pass
