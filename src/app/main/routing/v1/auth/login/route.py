from dependency_injector.wiring import Provide
from fastapi import Depends
from starlette.requests import Request

from src.app.core import route_inject
from src.app.main.common import ApplicationJsonResponse, ForbiddenHTTPException, SuccessResponse
from src.app.main.components.auth import AuthServiceI, AuthSessionPrivate
from src.app.main.components.users import UserPrivate
from src.app.main.di import GlobalContainer
from .dto import LoginRequestDTO, LoginResponseDTO
from ..component_router_v1 import auth_router_v1


@auth_router_v1.post("/login/", response_model=None)
@route_inject(
    _auth_service=Depends(Provide[GlobalContainer.shortcut_auth_service])
)
async def login_route(
        *,
        request: Request,
        payload: LoginRequestDTO,
        _auth_service: AuthServiceI
) -> ApplicationJsonResponse[LoginResponseDTO]:
    if request.client is None:
        raise ForbiddenHTTPException(message="Client is unknown")

    auth_info, auth_token_pair = await _auth_service.login(
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent", "unknown"),
        **payload.model_dump()
    )

    return SuccessResponse[LoginResponseDTO](
        data=LoginResponseDTO(
            user=auth_info.user.convert_to(UserPrivate),
            session=auth_info.session.convert_to(AuthSessionPrivate),
            access_token=auth_token_pair.access_token,
            refresh_token=auth_token_pair.refresh_token
        )
    )
