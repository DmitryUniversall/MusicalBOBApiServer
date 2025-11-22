from typing import Optional

from starlette.requests import Request

from src.app.main.components.auth.domain import AuthServiceI, AuthInfo
from ..bearer_auth_mixin import BearerAuthMixin


class HTTPJWTBearerAuthDependency(BearerAuthMixin):
    def __init__(self, auth_service: AuthServiceI) -> None:
        self._auth_service = auth_service

    async def __call__(self, request: Request, access_token: Optional[str] = None) -> AuthInfo:
        if access_token is None:  # For cases when frontend cannot add token to headers and forced to pass it via parameters
            authorization = request.headers.get("Authorization")
            access_token = await self.extract_token(authorization)

        return await self._auth_service.authenticate(access_token)
