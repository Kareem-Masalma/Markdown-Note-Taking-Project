from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.repositories.user import UserRepository
from src.services.user import UserService


def get_user_service(
    session: AsyncSession = Depends(Connection.get_session),
) -> UserService:
    user_repository: UserRepository = UserRepository(session)
    user_service = UserService(user_repository)
    return user_service
