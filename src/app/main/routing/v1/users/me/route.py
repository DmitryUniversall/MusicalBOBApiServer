from fastapi import Depends

from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.auth import HTTPJWTBearerAuthDependency, AuthInfo
from src.app.main.components.users import UserPrivate
from .dto import GetMeResponseDTO
from ..component_router_v1 import users_router_v1

_jwt_auth = HTTPJWTBearerAuthDependency()


@users_router_v1.get("/me/", response_model=None)
async def get_me_route(auth_info: AuthInfo = Depends(_jwt_auth)) -> ApplicationJsonResponse[GetMeResponseDTO]:
    return SuccessResponse[GetMeResponseDTO](
        data=GetMeResponseDTO(
            user=auth_info.user.convert_to(UserPrivate)
        )
    )
