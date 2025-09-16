from fastapi import APIRouter, Depends, status

from src.auth.tokens import check_token
from src.dependencies.summarization import get_summarization_service
from src.services.summarization import SummarizeNotes

router = APIRouter(dependencies=[Depends(check_token)])


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
    note_id: int, summarize_service: SummarizeNotes = Depends(get_summarization_service)
):
    response = await summarize_service.summarize(note_id)
    return response
