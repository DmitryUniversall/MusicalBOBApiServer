from starlette.requests import Request

from src.app.main.common import ApplicationJsonResponse, ForbiddenHTTPException, SuccessResponse
from src.app.main.components.auth import AuthService
from .dto import RefreshRequestDTO, RefreshResponseDTO
from ..component_router_v1 import auth_router_v1

_auth_service = AuthService.get_implementation()


@auth_router_v1.post("/refresh/")
async def refresh_route(payload: RefreshRequestDTO, request: Request) -> ApplicationJsonResponse:
    if request.client is None:
        raise ForbiddenHTTPException(message="Client is unknown")

    auth_token_pair = await _auth_service.refresh(
        current_client_ip=request.client.host,
        current_client_user_agent=request.headers.get("User-Agent", "unknown"),
        refresh_token=payload.refresh_token
    )

    return SuccessResponse[RefreshResponseDTO](
        data=RefreshResponseDTO(
            access_token=auth_token_pair.access_token,
            refresh_token=auth_token_pair.refresh_token
        )
    )
