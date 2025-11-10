import logging

from starlette.websockets import WebSocket

from src.app.main.components.auth.domain import AuthServiceI, AuthInfo, AuthHTTPException
from src.base.state import project_settings
from ..bearer_auth_mixin import BearerAuthMixin

_logger = logging.getLogger(__name__)


class WSJWTBearerAuthDependency(BearerAuthMixin):
    def __init__(self, auth_service: AuthServiceI) -> None:
        self._auth_service = auth_service

    async def __call__(self, websocket: WebSocket) -> AuthInfo | None:
        authorization = websocket.headers.get("Authorization")

        try:
            access_token = await self.extract_token(authorization)
            return await self._auth_service.authenticate(access_token)
        except AuthHTTPException as error:
            await websocket.close(
                code=error.payload.application_status_code,
                reason=error.payload.message
            )
        except Exception as error:
            _logger.error(f"Unexpected error while authenticating user: {error}")
            await websocket.close(
                code=project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.INTERNAL_SERVER_ERROR.application_status_code,
                reason=project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.INTERNAL_SERVER_ERROR.message
            )
