from typing import Annotated

from dependency_injector.wiring import Provide
from fastapi.params import Depends

from src.app.core import route_inject
from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.common.utils.auth import auth_protected
from src.app.main.components.auth import AuthServiceI, AuthInfo
from src.app.main.di import GlobalContainer
from ..component_router_v1 import auth_router_v1


@auth_router_v1.get("/logout/", response_model=None)
@route_inject(
    _auth_service=Depends(Provide[GlobalContainer.shortcut_auth_service])
)
async def logout_route(
        *,
        auth_info: Annotated[AuthInfo, Depends(auth_protected)],
        _auth_service: AuthServiceI
) -> ApplicationJsonResponse[None]:
    await _auth_service.revoke_session(auth_info.user.id, auth_info.session.session_uuid)
    return SuccessResponse[None]()
