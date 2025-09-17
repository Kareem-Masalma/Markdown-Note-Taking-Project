"""
This module is the repository for the user to interact with the database. Basic CRUD operations.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserUpdate


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self) -> list[User] | None:
        """
        This method to get all users in database that has deleted field set to 0
        :return: All users found in database.
        """
        res = await self.session.execute(select(User).where(User.deleted == 0))
        users: list[User] = res.scalars().all()
        return users

    async def get_user_by_username(self, username: str) -> User | None:
        """
        This method to get a user by their username with deleted field set to 0.

        :param username: The name of the user to be found inside the database.
        :return: The user if found in the database.
        """
        res = await self.session.execute(
            select(User).where((User.username == username) & (User.deleted == 0))
        )
        user = res.scalars().first()
        return user

    async def update_user(self, stored_user: User, user: UserUpdate):
        """
        This method to update the user's data.
        :param stored_user: The user to be updated.
        :param user: The new data to update the user.
        :return: The updated user
        """

        update_data = user.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(stored_user, field, value)

        await self.session.commit()
        await self.session.refresh(user)

    async def delete_user(self, username: str):
        """
        This method to delete a user from the database.
        :param username: The user to be deleted.
        """

        user = await self.get_user_by_username(username)
        user.deleted = 1
        await self.session.commit()

    async def add_new_user(self, user: User):
        """
        This method to add new user to the database.
        :param user: The user to be added.
        """
        self.session.add(user)
        await self.session.commit()
