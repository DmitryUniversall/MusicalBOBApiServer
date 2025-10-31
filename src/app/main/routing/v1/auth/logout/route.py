from fastapi import Depends

from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.auth import AuthServiceI, AuthInfo, HTTPJWTBearerAuthDependency
from ..component_router_v1 import auth_router_v1

_jwt_auth = HTTPJWTBearerAuthDependency()


@auth_router_v1.get("/logout/", response_model=None)
async def logout_route(auth_info: AuthInfo = Depends(_jwt_auth)) -> ApplicationJsonResponse[None]:
    _auth_service = AuthServiceI.get_implementation()  # type: ignore

    await _auth_service.revoke_session(auth_info.user.id, auth_info.session.session_uuid)
    return SuccessResponse[None]()
