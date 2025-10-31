from starlette.requests import Request

from src.app.main.common import ApplicationJsonResponse, ForbiddenHTTPException, CreatedResponse
from src.app.main.components.auth import AuthServiceI, AuthSessionPrivate
from src.app.main.components.users import UserPrivate
from .dto import RegisterRequestDTO, RegisterResponseDTO
from ..component_router_v1 import auth_router_v1


@auth_router_v1.post("/register/", response_model=None)
async def register_route(request: Request, payload: RegisterRequestDTO) -> ApplicationJsonResponse[RegisterResponseDTO]:
    _auth_service = AuthServiceI.get_implementation()  # type: ignore

    if request.client is None:
        raise ForbiddenHTTPException(message="Client is unknown")

    auth_info, auth_token_pair = await _auth_service.register(
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent", "unknown"),
        **payload.model_dump()
    )

    return CreatedResponse[RegisterResponseDTO](
        data=RegisterResponseDTO(
            user=auth_info.user.convert_to(UserPrivate),
            session=auth_info.session.convert_to(AuthSessionPrivate),
            access_token=auth_token_pair.access_token,
            refresh_token=auth_token_pair.refresh_token
        )
    )
