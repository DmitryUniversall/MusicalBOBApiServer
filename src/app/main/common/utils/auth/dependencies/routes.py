from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from starlette.requests import Request

from src.app.main.components.auth import AuthInfo, AuthServiceI
from src.app.main.di import GlobalContainer
from .http_auth import HTTPJWTBearerAuthDependency


@inject
async def auth_protected(
        request: Request,
        auth_service: AuthServiceI = Depends(Provide[GlobalContainer.shortcut_auth_service])
) -> AuthInfo:
    jwt_auth = HTTPJWTBearerAuthDependency(auth_service)
    return await jwt_auth(request)
