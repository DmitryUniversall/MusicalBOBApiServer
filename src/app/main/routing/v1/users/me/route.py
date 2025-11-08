from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.auth import AuthInfo, auth_protected
from src.app.main.components.users import UserPrivate
from .dto import GetMeResponseDTO
from ..component_router_v1 import users_router_v1


@users_router_v1.get("/me/", response_model=None)
@auth_protected()
async def get_me_route(
        *,
        auth_info: AuthInfo,
) -> ApplicationJsonResponse[GetMeResponseDTO]:
    return SuccessResponse[GetMeResponseDTO](
        data=GetMeResponseDTO(
            user=auth_info.user.convert_to(UserPrivate)
        )
    )
