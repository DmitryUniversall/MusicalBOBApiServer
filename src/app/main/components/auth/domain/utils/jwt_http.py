from http import HTTPStatus

import jwt
import pydantic

from src.app.main.components.auth.domain import AccessTokenPayload, RefreshTokenPayload, AuthTokenPayload
from src.app.main.components.auth.domain.exceptions import TokenExpiredHTTPException, TokenInvalidHTTPException, AuthUserUnknownHTTPException
from src.app.main.components.auth.domain.utils.jwt_tools import decode_jwt_token
from src.app.main.components.users.data.internal.models import UserModel
from src.app.main.components.users.domain import UsersService, UserInternal
from src.base.utils.types import JsonDict


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
    user_service = UsersService.get_implementation()

    try:
        return await user_service.get_user_by_id(payload.user_id)
    except UserModel.DoesNotExist as error:
        raise AuthUserUnknownHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error
