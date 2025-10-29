from http import HTTPStatus

import jwt
import pydantic

from src.app.main.components.users import UsersServiceI, UserInternal
from src.base.exceptions import DoesNotExistError
from src.base.utils.types import JsonDict
from .jwt_tools import decode_jwt_token
from ..domain.entities import AccessTokenPayload, RefreshTokenPayload, AuthTokenPayload
from ..domain.exceptions import TokenExpiredHTTPException, TokenInvalidHTTPException, AuthUserUnknownHTTPException

_user_service = UsersServiceI.get_implementation()  # type: ignore


def decode_jwt_token_with_http_exceptions(token: str) -> JsonDict:
    try:
        return decode_jwt_token(token)
    except jwt.ExpiredSignatureError as error:
        raise TokenExpiredHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error
    except jwt.PyJWTError as error:
        raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error


def decode_access_token_with_http_exceptions(token: str) -> AccessTokenPayload:
    try:
        return AccessTokenPayload.model_validate(decode_jwt_token_with_http_exceptions(token))
    except pydantic.ValidationError as error:
        raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error


def decode_refresh_token_with_http_exceptions(token: str) -> RefreshTokenPayload:
    try:
        return RefreshTokenPayload.model_validate(decode_jwt_token_with_http_exceptions(token))
    except pydantic.ValidationError as error:
        raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error


async def get_user_from_token_payload(payload: AuthTokenPayload) -> UserInternal:
    try:
        return await _user_service.get_user_by_id(payload.user_id)
    except DoesNotExistError as error:
        raise AuthUserUnknownHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error
