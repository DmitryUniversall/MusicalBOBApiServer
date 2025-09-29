from abc import ABC
from typing import Any

from src.app.main.components.users.domain import UserInternal


class UsersRepository(ABC):
    async def create_user(self, username: str, password_hashed: str, **fields) -> UserInternal:
        ...

    async def get_user_by_id(self, user_id: int) -> UserInternal:
        ...

    async def get_user_by_username(self, username: str, **fields) -> UserInternal:
        ...

    async def get_user_by_auth_credentials(self, username: str, password_hashed: str, **fields: Any) -> UserInternal:
        ...
