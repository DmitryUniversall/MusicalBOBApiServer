from dependency_injector.wiring import Provide
from fastapi import Depends

from src.app.core.http import route_inject
from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.common.utils.auth import auth_protected
from src.app.main.components.common_search import MediaContent, MediaContentType
from src.app.main.components.ym_search.domain import YMSearchServiceI
from src.app.main.di import GlobalContainer
from src.app.main.routing.v1.ym_search.component_router_v1 import ym_search_router_v1
from .dto import SearchResultDTO


@ym_search_router_v1.get("/search", dependencies=[Depends(auth_protected)], response_model=None)
@route_inject(
    _ym_search_service=Depends(Provide[GlobalContainer.shortcut_ym_search_service])
)
async def ym_search_route(
        *,
        query: str,
        _ym_search_service: YMSearchServiceI
) -> ApplicationJsonResponse[SearchResultDTO]:
    media: MediaContent = await _ym_search_service.search(query)

    return SuccessResponse[SearchResultDTO](
        data=SearchResultDTO(
            type=MediaContentType.from_type(type(media)),
            media=media,
        )
    )
