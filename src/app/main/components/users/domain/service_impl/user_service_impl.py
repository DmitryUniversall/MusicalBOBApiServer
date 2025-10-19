import hashlib

from src.app.main.components.users.domain import UserInternal, UsersService
from src.app.main.components.users.domain.repositories.user_repositry import UsersRepository


class UsersServiceImpl(UsersService):
    def __init__(self) -> None:
        self._user_repository = UsersRepository.get_implementation()

    def hash_password(self, password_raw: str, encoding: str = "utf-8") -> str:
        return hashlib.sha256(password_raw.encode(encoding=encoding)).hexdigest()

    async def create_user(self, username: str, password_raw: str, **fields) -> UserInternal:
        return await self._user_repository.create_user(username, self.hash_password(password_raw), **fields)

    async def get_by_username(self, username: str, **fields) -> UserInternal:
        return await self._user_repository.get_user_by_username(username, **fields)

    async def get_user_by_id(self, user_id: int) -> UserInternal:
        return await self._user_repository.get_user_by_id(user_id)

    async def get_by_auth_credentials(self, username: str, password_raw: str, **fields) -> UserInternal:
        return await self._user_repository.get_user_by_auth_credentials(username, self.hash_password(password_raw), **fields)
