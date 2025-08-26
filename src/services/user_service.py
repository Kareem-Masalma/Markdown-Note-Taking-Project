"""
This module is the methods used to handle the users endpoint operations, get user by username, get all users,
delete user, update user, register new user and login.
"""

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import password, tokens
from src.models.user import User
from src.schemas.user_schema import UserIn, UserUpdate


class UserService:

    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[User] | None:
        """
        This method is used to get all available users inside the database with deleted field set to 0,
        it returns all users if found, else it raises 404 HTTPException.

        :param session: This is the async session used to handle the database.
        :return: The returned value is a list of users if found.
        """
        res = await session.execute(select(User).where(User.deleted == 0))
        users: list[User] = res.scalars().all()
        if len(users) == 0:
            raise HTTPException(status_code=404, detail="No users found")
        return users

    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
        """
        This method is used to get an available user with deleted field set to 0 by their username,
        it returns the user if found, else it raises a 404 HTTPException.
        :param username: The username of the user to be found.
        :param session: This is the async session used to handle the database.
        :return: The user's data.
        """
        res = await session.execute(
            select(User).where((User.username == username) & (User.deleted == 0))
        )
        user = res.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User {username} not found")
        return user

    @staticmethod
    async def update_user(username: str, user: UserUpdate, session: AsyncSession):
        """
        This method is used to update an available user from database with deleted field set to 0,
        exclude_unset is set to be True, which removes the empty fields that aren't meant to be updated.

        :param username: The username of the user to be updated.
        :param user: New user's data to update.
        :param session: This is the async session used to handle the database.
        :return: The update user, if not found it raised 404 HTTPException.
        """
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
        """
        This method to delete an available user from database with deleted fild set to 1, this method softly deletes the
        user, which means the user is not removed from the database, but the deleted field will be set to 1.

        :param username: The username of the user to be deleted.
        :param session: This is the async session used to handle the database.
        :return: True on Success, else it raised 404 HTTPException.
        """
        try:
            user = UserService.get_user_by_username(username, session)
            user.deleted = 1
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def login(
        logged_user: UserIn, session: AsyncSession
    ) -> dict[str, str | bool]:
        """
        This method is used to check the user's credentials to sign them in.

        :param logged_user: The user's data.
        :param session: This is the async session used to handle the database.
        :return: On success jwt token is returned.
        """
        user = await UserService.get_user_by_username(logged_user.username, session)
        verify = password.verify_password(logged_user.password, user.password)
        if verify:
            token = tokens.generate_jwt_token(user)
            return {
                "success": True,
                "token": token,
                "user": {"username": user.username, "email": user.email},
            }
        return {"success": False, "details": "Invalid username or password"}

    @staticmethod
    async def register_user(user: UserIn, session: AsyncSession):
        """
        This method to add new user to the database, the user shall not be available even with deleted fields set to 1.

        :param user: The new user information.
        :param session: This is the async session used to handle the database.
        :return: The new user created. If the user is already exists it raises 409 HTTPException.
        """
        hashed_password = password.hash_password(user.password)
        exists = (
            (await session.execute(select(User).where(User.username == user.username)))
            .scalars()
            .first()
        )
        if exists:
            raise HTTPException(status_code=409, detail="User already exists")

        new_user = User(user.username, user.email, hashed_password)
        session.add(new_user)
        await session.commit()
        return {
            "details": "user is registers",
            "user": {"name": new_user.username, "email": new_user.email},
        }
