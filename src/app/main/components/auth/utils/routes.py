from functools import wraps

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.app.core import route_inject
from src.app.main.components.auth.domain import AuthInfo
from src.app.main.di import GlobalContainer


def auth_protected():
    def decorator(func):
        @wraps(func)
        @route_inject(
            auth_info=Depends(
                Provide[GlobalContainer.shortcut_jwt_auth_dependency]
            )
        )
        async def wrapper(*args, auth_info: AuthInfo, **kwargs):
            return await func(*args, **kwargs, auth_info=auth_info)

        return wrapper

    return decorator
