import uuid
from http import HTTPStatus
from typing import Dict, Any, Union

import jwt
import pydantic

from src.app.main.components.auth.domain import (
    TokenExpiredHTTPException,
    TokenInvalidHTTPException,
    AccessTokenPayload,
    RefreshTokenPayload,
    AuthRepositoryI
)
from src.base.state import project_settings
from src.base.utils.types import UUIDString, JsonDict


class AuthRepositoryImpl(AuthRepositoryI):
    def decode_jwt_token_with_http_exceptions(self, token: str) -> JsonDict:
        try:
            return self.decode_jwt_token(token)
        except jwt.ExpiredSignatureError as error:
            raise TokenExpiredHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error
        except jwt.PyJWTError as error:
            raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error

    def decode_access_token_with_http_exceptions(self, token: str) -> AccessTokenPayload:
        try:
            return AccessTokenPayload.model_validate(self.decode_jwt_token_with_http_exceptions(token))
        except pydantic.ValidationError as error:
            raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error

    def decode_refresh_token_with_http_exceptions(self, token: str) -> RefreshTokenPayload:
        try:
            return RefreshTokenPayload.model_validate(self.decode_jwt_token_with_http_exceptions(token))
        except pydantic.ValidationError as error:
            raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error

    def generate_jwt_token_id(self) -> str:
        return str(uuid.uuid4())

    def create_jwt_token(self, *, payload: JsonDict, exp: Union[int, float]) -> str:
        encoded_jwt = jwt.encode(
            payload={
                "exp": exp,
                **payload
            },
            key=project_settings.SECRET_KEY,
            algorithm=project_settings.TOKEN_ENCRYPTION_ALGORITHM
        )

        return encoded_jwt

    def decode_jwt_token(self, token: str) -> Dict[str, Any]:
        return jwt.decode(
            jwt=token,
            key=project_settings.SECRET_KEY,
            algorithms=[project_settings.TOKEN_ENCRYPTION_ALGORITHM]
        )

    def create_access_token_with_payload(self, payload: 'AccessTokenPayload') -> str:
        return self.create_jwt_token(payload=payload.to_json_dict(exclude='exp'), exp=payload.exp.timestamp())

    def create_refresh_token_with_payload(self, payload: 'RefreshTokenPayload') -> str:
        return self.create_jwt_token(payload=payload.to_json_dict(exclude='exp'), exp=payload.exp.timestamp())

    def create_access_token(self, user_id: int, session_uuid: UUIDString, token_uuid: str | None = None) -> str:
        from src.app.main.components.auth.domain import AccessTokenPayload

        payload: AccessTokenPayload
        if token_uuid is not None:
            payload = AccessTokenPayload(user_id=user_id, session_uuid=session_uuid, token_uuid=token_uuid)
        else:
            payload = AccessTokenPayload(user_id=user_id, session_uuid=session_uuid)

        return self.create_access_token_with_payload(payload=payload)

    def create_refresh_token(self, user_id: int, session_uuid: UUIDString, token_uuid: str | None = None) -> str:
        from src.app.main.components.auth.domain import RefreshTokenPayload

        payload: RefreshTokenPayload
        if token_uuid is not None:
            payload = RefreshTokenPayload(user_id=user_id, session_uuid=session_uuid, token_uuid=token_uuid)
        else:
            payload = RefreshTokenPayload(user_id=user_id, session_uuid=session_uuid)

        return self.create_refresh_token_with_payload(payload=payload)
