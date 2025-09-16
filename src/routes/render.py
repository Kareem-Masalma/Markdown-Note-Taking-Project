from fastapi import APIRouter, Depends, Response, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.models.user import User
from src.repositories.note import NoteRepository
from src.services.render import RenderService

router = APIRouter()


@router.get(
    "/note/{note_id}",
    summary="Render a note",
    description="This endpoint render a markdown note to HTML code",
    response_description="The returned data is sanitized HTML code",
    responses={
        200: {"description": "The rendered note requested returned successfully"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_rendered_note(
    note_id: int,
    response: Response,
    if_none_match: str | None = Header(default=None),
    user: User = Depends(check_token),
    session: AsyncSession = Depends(Connection.get_session),
):
    render_service = RenderService(NoteRepository(session))

    rendered_html = await render_service.render(if_none_match, response, note_id)

    return {"note_id": note_id, "rendered_html": rendered_html}
