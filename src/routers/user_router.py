from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.models.user import User
from src.schemas.user_schema import UserOut, UserIn
from src.services.user_service import UserService

router = APIRouter()


@router.get('/', description="This endpoint returns all users available inside the database",
            response_model=list[UserOut])
async def get_all_users(session: AsyncSession = Depends(Connection.get_session)):
    users = UserService.get_all_users(session)
    return users


@router.get('/{username}', description="This endpoint returns a specific user by their username",
            response_model=UserOut)
async def get_user_by_username(username: str, session: AsyncSession = Depends(Connection.get_session)):
    user = UserService.get_user_by_username(username, session)
    return user


@router.post('/login', description="This endpoint for a valid user to login")
async def login(session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.post('/register', description="This endpoint for registering new user")
async def register(user: UserIn = Query(..., title="New User", description="The new user to register to database"),
                   session: AsyncSession = Depends(Connection.get_session)):
    pass


@router.patch('/{username}', description="This endpoint updates a user's data by their username")
async def update_user(username: str, user: UserIn, session: AsyncSession = Depends(Connection.get_session)):
    stored_user: User = await UserService.get_user_by_username(username, session)
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stored_user, field, value)
    updated_user = await UserService.update_user(stored_user, session)
    return {"success": True, "user": updated_user}


@router.delete('/{username}', description="This endpoint deletes a certain user by their username")
async def delete_user(username: str, session: AsyncSession = Depends(Connection.get_session)):
    await UserService.delete_user(username, session)
    return {'success': True, 'message': f'user {username} deleted'}
