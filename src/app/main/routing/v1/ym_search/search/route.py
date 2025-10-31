from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.common_search import MediaContent, MediaContentType
from src.app.main.components.ym_search.domain import YMSearchServiceI
from src.app.main.routing.v1.ym_search import ym_search_router_v1
from .dto import SearchResultDTO

_ym_search_service = YMSearchServiceI.get_implementation()  # type: ignore


@ym_search_router_v1.get("/search")
def ym_search_route(query: str) -> ApplicationJsonResponse[SearchResultDTO]:
    media: MediaContent = _ym_search_service.search(query)

    return SuccessResponse[SearchResultDTO](
        data=SearchResultDTO(
            type=MediaContentType(type(media)),
            media=media,
        )
    )
