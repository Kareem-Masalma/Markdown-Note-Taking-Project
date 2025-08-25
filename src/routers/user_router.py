from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection

router = APIRouter()


@router.get('/')
async def get_all_users(session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.get('/{username}')
async def get_user_by_username(username: str, session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.post('/login')
async def login(session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.post('/register')
async def register(session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.patch('/{username}')
async def update_user(username: str, session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.delete('/{username}')
async def delete_user(username: str, session: AsyncSession = Depends(Connection.get_session)):
    pass
