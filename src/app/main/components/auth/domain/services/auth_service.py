from abc import ABC, abstractmethod

from src.base.utils.interface import InterfaceMeta
from src.base.utils.types import UUIDString
from ..entities import AuthInfo, AuthTokenPair


class AuthServiceI(ABC, metaclass=InterfaceMeta):
    @abstractmethod
    async def authenticate(self, access_token: str) -> AuthInfo:
        ...

    @abstractmethod
    async def refresh(
            self,
            refresh_token: str,
            current_client_ip: str,
            current_client_user_agent: str
    ) -> AuthTokenPair:
        ...

    @abstractmethod
    async def register(
            self,
            username: str,
            password: str,
            ip_address: str,
            user_agent: str,
            session_name: str,
            **user_fields
    ) -> tuple[AuthInfo, AuthTokenPair]:
        ...

    @abstractmethod
    async def login(
            self,
            username: str,
            password: str,
            ip_address: str,
            user_agent: str,
            session_name: str,
            **user_fields
    ) -> tuple[AuthInfo, AuthTokenPair]:
        ...

    @abstractmethod
    async def revoke_session(self, user_id: int, session_uuid: UUIDString) -> None:
        ...
