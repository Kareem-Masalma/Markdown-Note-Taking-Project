"""
This module is for handling jwt tokens, it generates new token, encrypts it, and verify it on login.
"""

from datetime import datetime, timedelta, UTC

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.models.user import User
from jose import jwt
from src.config.definitions import SECRETE, ALGO

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.repositories.user import UserRepository
from src.services.user import UserService

bearer_scheme = HTTPBearer()


def generate_jwt_token(user: User) -> str:
    """
    This method is used to generate new token after logging in successfully.

    :param user: The logged-in user.
    :return: The new jwt token.
    """
    expire = datetime.now(UTC) + timedelta(minutes=60)
    payload = {"username": user.username, "exp": int(expire.timestamp())}

    token = jwt.encode(payload, SECRETE, algorithm=ALGO)

    return token


def encrypt_jwt_token(token: str) -> dict[str, str | int]:
    """
    This method encrypts a jwt token.

    :param token: The jwt token.
    :return: Encrypted jwt token.
    """
    try:
        data = jwt.decode(token, SECRETE, ALGO)
        return data
    except Exception as e:
        raise HTTPException(status_code=409)


async def check_token(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(Connection.get_session),
) -> User:
    """
    This method to check token when logging in.

    :param token: The jwt token.
    :param session: This is the async session used to handle the database.
    :return: The user on success, else it raises 409 HTTPException.
    """
    token = token.credentials
    data = encrypt_jwt_token(token)
    username = data["username"]
    user_service = UserService(UserRepository(session))
    saved_user = await user_service.get_user_by_username(username)
    if not saved_user:
        raise HTTPException(status_code=409, detail="Unauthorized")
    return saved_user
