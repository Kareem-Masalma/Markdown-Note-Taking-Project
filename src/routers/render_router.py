from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/note/{note_id}')
async def get_rendered_note(note_id: int):
    pass
