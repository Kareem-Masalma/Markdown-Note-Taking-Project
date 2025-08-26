from abc import ABC, abstractmethod

from src.models.user import User
from src.schemas.user_schema import UserUpdate, UserIn


class IUserRepository(ABC):
    @abstractmethod
    async def get_all_users(self) -> list[User] | None:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    async def update_user(self, stored_user: User, user: UserUpdate):
        pass

    @abstractmethod
    async def delete_user(self, username: str):
        pass

    @abstractmethod
    async def add_new_user(self, user: User):
        pass
