from typing import Any, Coroutine

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update

from src.models.user import User


class UserService:

    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[User] | None:
        res = await session.execute(select(User).where(User.deleted == 0))
        users: list[User] = res.scalars().all()
        if len(users) == 0:
            raise HTTPException(status_code=404, detail="No users found")
        return users

    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
        res = await session.execute(select(User).where((User.username == username) & (User.deleted == 0)))
        user = res.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User {username} not found")
        return user

    @staticmethod
    async def update_user(user: User, session: AsyncSession):
        try:
            await session.commit()
            await session.refresh(user)
            return user
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def delete_user(username: str, session: AsyncSession):
        try:
            user = UserService.get_user_by_username(username, session)
            user.deleted = 1
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            raise e
