from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from starlette.requests import Request

from .http_auth import HTTPJWTBearerAuthDependency
from ...domain import AuthInfo


def auth_protected():
    from src.app.main.di import GlobalContainer

    @inject
    async def wrapper(
            request: Request,
            jwt_auth: HTTPJWTBearerAuthDependency = Depends(Provide[GlobalContainer.shortcut_jwt_auth_dependency])
    ) -> AuthInfo:
        return await jwt_auth(request)

    return wrapper
