from dependency_injector.wiring import Provide
from fastapi import Depends

from src.app.core import route_inject
from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.auth import AuthServiceI, AuthInfo, auth_protected
from src.app.main.di import GlobalContainer
from src.base.utils.types import UUIDString
from ..component_router_v1 import auth_router_v1


@auth_router_v1.post("/sessions/{session_uuid}/terminate/", dependencies=[Depends(auth_protected())], response_model=None)
@route_inject(
    _auth_service=Depends(Provide[GlobalContainer.shortcut_auth_service])
)
async def terminate_session_route(
        *,
        session_uuid: UUIDString,
        auth_info: AuthInfo,
        _auth_service: AuthServiceI
) -> ApplicationJsonResponse[None]:
    await _auth_service.revoke_session(user_id=auth_info.user.id, session_uuid=session_uuid)
    return SuccessResponse[None]()
