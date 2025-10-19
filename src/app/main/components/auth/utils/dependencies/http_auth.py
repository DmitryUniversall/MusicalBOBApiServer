from starlette.requests import Request

from src.app.main.components.auth.domain.entities.auth_info import AuthInfo
from src.app.main.components.auth.domain.services.auth_service import AuthService
from ..bearer_auth_mixin import BearerAuthMixin

_auth_service = AuthService.get_implementation()


class HTTPJWTBearerAuthDependency(BearerAuthMixin):
    async def __call__(self, request: Request) -> AuthInfo:
        authorization = request.headers.get("Authorization")
        access_token = await self.extract_token(authorization)
        return await _auth_service.authenticate(access_token)
