from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import password, tokens
from src.models.user import User
from src.schemas.user_schema import UserIn


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
    async def update_user(username: str, user: UserIn, session: AsyncSession):
        try:
            stored_user = UserService.get_user_by_username(username, session)
            update_data = user.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(stored_user, field, value)

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

    @staticmethod
    async def signin(logged_user: UserIn, session: AsyncSession) -> dict[str, str | bool]:
        user = await UserService.get_user_by_username(logged_user.username, session)
        verify = password.verify_password(logged_user.password, user.password)
        if verify:
            token = tokens.generate_jwt_token(user)
            return {
                'success': True,
                'token': token,
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }
        return {
            'success': False,
            'details': 'Invalid username or password'
        }

    @staticmethod
    async def register_user(user: UserIn, session: AsyncSession):
        hashed_password = password.hash_password(user.password)
        exists = (await session.execute(select(User).where(User.username == user.username))).scalars().first()
        if exists:
            raise HTTPException(status_code=409, detail="User already exists")

        new_user = User(user.username, user.email, hashed_password)
        session.add(new_user)
        await session.commit()
        return {
            'details': 'user is registers',
            'user': {
                'name': new_user.username,
                'email': new_user.email
            }
        }
