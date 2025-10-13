from abc import abstractmethod, ABC
from typing import Any

from src.app.main.components.users.domain import UserInternal
from src.base.utils.interface import InterfaceMeta


class UsersRepository(ABC, metaclass=InterfaceMeta):
    @abstractmethod
    async def create_user(self, username: str, password_hashed: str, **fields) -> UserInternal:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserInternal:
        ...

    @abstractmethod
    async def get_user_by_username(self, username: str, **fields) -> UserInternal:
        ...

    @abstractmethod
    async def get_user_by_auth_credentials(self, username: str, password_hashed: str, **fields: Any) -> UserInternal:
        ...
