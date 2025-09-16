"""
This module is the methods used to handle the users endpoint operations, get user by username, get all users,
delete user, update user, register new user and login.
"""

from fastapi import HTTPException

from src.auth import password, tokens
from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UserRequest, UserUpdate


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all_users(self) -> list[User] | None:
        """
        This method is used to get all available users inside the database with deleted field set to 0,
        it returns all users if found, else it raises 404 HTTPException.

        :return: The returned value is a list of users if found.
        """
        try:
            users: list[User] | None = await self.user_repository.get_all_users()
            if not users:
                raise HTTPException(status_code=404, detail="No users found")
            return users
        except Exception as e:
            raise e

    async def get_user_by_username(self, username: str) -> User | None:
        """
        This method is used to get an available user with deleted field set to 0 by their username,
        it returns the user if found, else it raises a 404 HTTPException.
        :param username: The username of the user to be found.
        :return: The user's data.
        """
        try:
            user: User | None = await self.user_repository.get_user_by_username(
                username
            )
            if not user:
                raise HTTPException(
                    status_code=404, detail=f"User {username} not found"
                )

            return user
        except Exception as e:
            raise e

    async def update_user(self, username: str, user: UserUpdate) -> UserUpdate:
        """
        This method is used to update an available user from database with deleted field set to 0,
        exclude_unset is set to be True, which removes the empty fields that aren't meant to be updated.

        :param username: The username of the user to be updated.
        :param user: New user's data to update.
        :return: The update user, if not found it raised 404 HTTPException.
        """
        try:
            stored_user = await self.user_repository.get_user_by_username(username)

            if not stored_user:
                raise HTTPException(
                    status_code=404, detail=f"User {username} not found"
                )

            await self.user_repository.update_user(stored_user, user)

            return user
        except Exception as e:
            raise e

    async def delete_user(self, username: str):
        """
        This method to delete an available user from database with deleted fild set to 1, this method softly deletes the
        user, which means the user is not removed from the database, but the deleted field will be set to 1.

        :param username: The username of the user to be deleted.
        :return: True on Success, else it raised 404 HTTPException.
        """
        try:
            await self.user_repository.delete_user(username)
            return True
        except Exception as e:
            raise e

    async def login(self, logged_user: UserRequest) -> dict[str, str | bool]:
        """
        This method is used to check the user's credentials to sign them in.

        :param logged_user: The user's data.
        :return: On success jwt token is returned.
        """
        try:
            user = await self.get_user_by_username(logged_user.username)
            verify = password.verify_password(logged_user.password, user.password)
            if verify:
                token = tokens.generate_jwt_token(user)
                return {
                    "success": True,
                    "token": token,
                    "user": {"username": user.username, "email": user.email},
                }
            return {"success": False, "details": "Invalid username or password"}
        except Exception as e:
            raise e

    async def register_user(self, user: UserRequest):
        """
        This method to add new user to the database, the user shall not be available even with deleted fields set to 1.

        :param user: The new user information.
        :return: The new user created. If the user is already exists it raises 409 HTTPException.
        """
        try:
            hashed_password = password.hash_password(user.password)
            exists = await self.user_repository.get_user_by_username(user.username)
            if exists:
                raise HTTPException(status_code=409, detail="User already exists")

            new_user = User(
                username=user.username, email=user.email, password=hashed_password
            )

            await self.user_repository.add_new_user(new_user)

            return {
                "details": "user is registers",
                "user": {"name": new_user.username, "email": new_user.email},
            }
        except Exception as e:
            raise e
