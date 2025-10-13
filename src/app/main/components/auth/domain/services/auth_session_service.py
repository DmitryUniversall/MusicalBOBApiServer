from abc import ABC, abstractmethod

from src.app.main.components.auth.domain import AuthSessionInternal
from src.base.utils.interface import InterfaceMeta
from src.base.utils.types import UUIDString


class AuthSessionService(ABC, metaclass=InterfaceMeta):
    @abstractmethod
    def generate_session_uuid(self) -> str:
        ...

    @abstractmethod
    async def get_session(self, user_id: int, session_uuid: UUIDString) -> AuthSessionInternal:
        ...

    @abstractmethod
    async def revoke_session(self, user_id: int, session_uuid: UUIDString) -> None:
        ...

    @abstractmethod
    async def create_session(
            self,
            user_id: int,
            ip_address: str,
            user_agent: str,
            session_name: str,
            access_token_uuid: UUIDString,
            refresh_token_uuid: UUIDString
    ) -> AuthSessionInternal:
        ...

    @abstractmethod
    async def get_user_sessions(self, user_id: int) -> tuple[AuthSessionInternal, ...]:
        ...

    @abstractmethod
    async def update_session(self, updated_session: AuthSessionInternal) -> None:
        ...

    @abstractmethod
    async def revoke_other_sessions(self, user_id: int, keep_session_uuid: UUIDString) -> None:
        ...

    @abstractmethod
    async def get_session_from_access_token(self, access_token: str) -> AuthSessionInternal:
        ...

    @abstractmethod
    async def get_session_from_refresh_token(self, refresh_token: str) -> AuthSessionInternal:
        ...
