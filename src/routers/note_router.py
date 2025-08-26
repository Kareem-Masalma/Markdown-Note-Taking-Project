from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection

router = APIRouter()


@router.get("/")
async def get_all_notes(session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.get("/{note_id}")
async def get_note_by_id(
    note_id: int, session: AsyncSession = Depends(Connection.get_session)
):
    pass


@router.get("/user/{user_id}")
async def get_users_notes(
    user_id: int, session: AsyncSession = Depends(Connection.get_session)
):
    pass


@router.get("/history/{note_id}")
async def get_note_history(
    note_id: int, session: AsyncSession = Depends(Connection.get_session)
):
    pass


@router.get("/history/{note_id}/{history_id}")
async def get_note_old_version(
    note_id: int,
    history_id: int,
    session: AsyncSession = Depends(Connection.get_session),
):
    pass


@router.post("/")
async def add_new_note(session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.patch("/{note_id}")
async def update_note(
    note_id: int, session: AsyncSession = Depends(Connection.get_session)
):
    pass


@router.delete("/{note_id}")
async def delete_note(
    note_id: int, session: AsyncSession = Depends(Connection.get_session)
):
    pass
