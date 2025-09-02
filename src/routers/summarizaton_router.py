from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.tokens import check_token
from src.common.db.connection import Connection
from src.models.user import User
from src.repositories.note_repository import NoteRepository
from src.services.summarize_notes_service import SummarizeNotes

router = APIRouter()


@router.get(
    "/summ/note/{note_id}",
    summary="Summarize note",
    description="This endpoint summarize note using gemini api.",
    response_description="The returned data is the summarized note",
    responses={
        200: {"description": "The note successfully summarized"},
        404: {"description": "Note is not found"},
    },
    status_code=status.HTTP_200_OK,
)
async def get_note_summary(
    note_id: int,
    user: User = Depends(check_token),
    session: AsyncSession = Depends(Connection.get_session),
):
    summarize_service = SummarizeNotes(NoteRepository(session))

    response = await summarize_service.summarize(note_id)

    return response
