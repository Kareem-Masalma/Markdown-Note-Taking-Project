from fastapi import APIRouter, Depends, Response, Header, status

from src.dependencies.render import get_render_service
from src.schemas.render import RenderResponse
from src.services.render import RenderService

router = APIRouter()


@router.get(
    "/note/{note_id}",
    summary="Render a note",
    description="This endpoint render a markdown note to HTML code",
    response_model=RenderResponse,
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
    render_service: RenderService = Depends(get_render_service),
):

    rendered_html = await render_service.render(if_none_match, response, note_id)
    return rendered_html
