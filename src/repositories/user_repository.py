from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.user_repository_interface import IUserRepository
from src.schemas.user_schema import UserUpdate


class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self) -> list[User] | None:
        res = await self.session.execute(select(User).where(User.deleted == 0))
        users: list[User] = res.scalars().all()
        return users

    async def get_user_by_username(self, username: str) -> User | None:
        res = await self.session.execute(
            select(User).where((User.username == username) & (User.deleted == 0))
        )
        user = res.scalars().first()
        return user

    async def update_user(self, stored_user: User, user: UserUpdate):
        try:
            update_data = user.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(stored_user, field, value)

            await self.session.commit()
            await self.session.refresh(user)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete_user(self, username: str):
        try:
            user = await self.get_user_by_username(username)
            user.deleted = 1
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def add_new_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
