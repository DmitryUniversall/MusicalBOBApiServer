from datetime import datetime, timedelta
from typing import Union, Literal
from uuid import uuid4

from pydantic import Field, field_validator

from src.app.core import BaseSchema
from src.app.main.components.auth.domain.entities.auth_token_payload.auth_token_type import AuthTokenType
from src.base.state import project_settings
from src.base.utils.types import UUIDString


class AuthTokenPayload(BaseSchema):
    token_uuid: str = Field(default_factory=lambda: str(uuid4()))
    token_type: AuthTokenType
    exp: datetime
    user_id: int
    session_uuid: UUIDString

    # noinspection PyNestedDecorators
    @field_validator('token_type', mode="before")
    @classmethod
    def set_token_type(cls, value: Union[str, AuthTokenType]) -> AuthTokenType:
        return AuthTokenType(value) if isinstance(value, str) else value


class RefreshTokenPayload(AuthTokenPayload):
    @staticmethod
    def calculate_refresh_expire_at(start: datetime | None = None, ttl: int | None = None) -> datetime:
        start = start if start is not None else datetime.now()
        ttl = ttl if ttl is not None else project_settings.REFRESH_TOKEN_TTL
        return start + timedelta(seconds=ttl)

    token_type: Literal[AuthTokenType.REFRESH] = AuthTokenType.REFRESH
    exp: datetime = Field(default_factory=calculate_refresh_expire_at)


class AccessTokenPayload(AuthTokenPayload):
    @staticmethod
    def calculate_access_expire_at(start: datetime | None = None, ttl: int | None = None) -> datetime:
        start = start if start is not None else datetime.now()
        ttl = ttl if ttl is not None else project_settings.ACCESS_TOKEN_TTL
        return start + timedelta(seconds=ttl)

    token_type: Literal[AuthTokenType.ACCESS] = AuthTokenType.ACCESS
    exp: datetime = Field(default_factory=calculate_access_expire_at)
