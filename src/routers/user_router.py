from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/')
async def get_all_users():
    pass


@router.get('/{username}')
async def get_user_by_username(username: str):
    pass


@router.post('/login')
async def login():
    pass


@router.post('/register')
async def register():
    pass


@router.patch('/{username}')
async def update_user(username: str):
    pass


@router.delete('/{username}')
async def delete_user(username: str):
    pass
