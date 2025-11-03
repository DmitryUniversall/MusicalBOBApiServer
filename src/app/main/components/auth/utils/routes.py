from functools import wraps

from fastapi import Depends

from src.app.main.components.auth.domain import AuthInfo
from .dependencies import HTTPJWTBearerAuthDependency

_jwt_auth = HTTPJWTBearerAuthDependency()


def jwt_protected(func):
    @wraps(func)
    async def wrapper(*args, auth_info: AuthInfo = Depends(_jwt_auth), **kwargs):
        return await func(*args, auth_info=auth_info, **kwargs)

    return wrapper
