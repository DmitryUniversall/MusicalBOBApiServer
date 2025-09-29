from abc import ABC, abstractmethod

from src.app.main.components.users.domain import UserInternal


class AbstractUsersService(ABC):
    @abstractmethod
    def hash_password(self, password_raw: str, encoding: str = "utf-8") -> str:
        ...

    @abstractmethod
    async def create_user(self, username: str, password_raw: str, **fields) -> UserInternal:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserInternal:
        ...

    @abstractmethod
    async def get_by_username(self, username: str, **fields) -> UserInternal:
        ...

    @abstractmethod
    async def get_by_auth_credentials(self, username: str, password_raw: str, **fields) -> UserInternal:
        ...
