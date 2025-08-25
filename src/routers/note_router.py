from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/')
async def get_all_notes():
    pass


@router.get('/{note_id}')
async def get_note_by_id(note_id: int):
    pass


@router.get('/user/{user_id}')
async def get_users_notes(user_id: int):
    pass


@router.get('/history/{note_id}')
async def get_note_history(note_id: int):
    pass


@router.get('/history/{note_id}/{history_id}')
async def get_note_old_version(note_id: int, history_id: int):
    pass


@router.post('/')
async def add_new_note():
    pass


@router.patch('/{note_id}')
async def update_note(note_id: int):
    pass


@router.delete('/{note_id}')
async def delete_note(note_id: int):
    pass
