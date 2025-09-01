from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.common.utils.render_markdown import render_markdown_to_html
from src.models.user import User
from src.repositories.note_repository import NoteRepository
from src.services.render_service import RenderService

router = APIRouter()


@router.get("/note/{note_id}")
async def get_rendered_note(
        note_id: int,
        user: User = Depends(check_token),
        session: AsyncSession = Depends(Connection.get_session),
):
    render_service = RenderService(NoteRepository(session))
    rendered_html = await render_service.render(note_id)

    return {"note_id": note_id, "rendered_html": rendered_html}
