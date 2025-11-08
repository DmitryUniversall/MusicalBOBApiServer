from starlette.requests import Request

from src.app.main.components.auth.domain import AuthServiceI, AuthInfo
from ..bearer_auth_mixin import BearerAuthMixin


class HTTPJWTBearerAuthDependency(BearerAuthMixin):
    def __init__(self, auth_service: AuthServiceI) -> None:
        self._auth_service = auth_service

    async def __call__(self, request: Request) -> AuthInfo:
        authorization = request.headers.get("Authorization")
        access_token = await self.extract_token(authorization)
        return await self._auth_service.authenticate(access_token)
