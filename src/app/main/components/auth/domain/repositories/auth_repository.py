from abc import abstractmethod, ABC
from typing import Union, Any, Optional

from src.base.utils.types import JsonDict, UUIDString
from ..entities import AccessTokenPayload, RefreshTokenPayload


class AuthRepositoryI(ABC):
    @abstractmethod
    def decode_jwt_token_with_http_exceptions(self, token: str) -> JsonDict:
        ...

    @abstractmethod
    def decode_access_token_with_http_exceptions(self, token: str) -> AccessTokenPayload:
        ...

    @abstractmethod
    def decode_refresh_token_with_http_exceptions(self, token: str) -> RefreshTokenPayload:
        ...

    @abstractmethod
    def generate_jwt_token_id(self) -> str:
        ...

    @abstractmethod
    def create_jwt_token(self, *, payload: JsonDict, exp: Union[int, float]) -> str:
        ...

    @abstractmethod
    def decode_jwt_token(self, token: str) -> dict[str, Any]:
        ...

    @abstractmethod
    def create_access_token_with_payload(self, payload: 'AccessTokenPayload') -> str:
        ...

    @abstractmethod
    def create_refresh_token_with_payload(self, payload: 'RefreshTokenPayload') -> str:
        ...

    @abstractmethod
    def create_access_token(self, user_id: int, session_uuid: UUIDString, token_uuid: Optional[str] = None) -> str:
        ...

    @abstractmethod
    def create_refresh_token(self, user_id: int, session_uuid: UUIDString, token_uuid: Optional[str] = None) -> str:
        ...
