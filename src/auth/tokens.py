from datetime import datetime, timedelta, UTC

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import Connection
from src.models.user import User
from jose import jwt
from src.config.definitions import SECRETE, ALGO

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.services.user_service import UserService

bearer_scheme = HTTPBearer()


def generate_jwt_token(user: User) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=60)
    payload = {
        'username': user.username,
        'exp': int(expire.timestamp())
    }

    token = jwt.encode(payload, SECRETE, algorithm=ALGO)

    return token


def encrypt_jwt_token(token: str) -> dict[str, str | int]:
    data = jwt.decode(token, SECRETE, ALGO)
    return data


def check_token(token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
                session: AsyncSession = Depends(Connection.get_session)) -> User:
    token = token.credentials
    data = encrypt_jwt_token(token)
    username = data['username']
    saved_user = UserService.get_user_by_username(username, session)
    if not saved_user:
        raise HTTPException(status_code=409, detail="Unauthorized")
    return saved_user
