from fastapi import Depends

from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.auth import AuthServiceI, AuthInfo, HTTPJWTBearerAuthDependency
from src.base.utils.types import UUIDString
from ..component_router_v1 import auth_router_v1

_jwt_auth = HTTPJWTBearerAuthDependency()


@auth_router_v1.post("/sessions/{session_uuid}/terminate/", response_model=None)
async def terminate_session_route(
        session_uuid: UUIDString,
        auth_info: AuthInfo = Depends(_jwt_auth)
) -> ApplicationJsonResponse[None]:
    _auth_service = AuthServiceI.get_implementation()  # type: ignore

    await _auth_service.revoke_session(user_id=auth_info.user.id, session_uuid=session_uuid)

    return SuccessResponse[None]()
