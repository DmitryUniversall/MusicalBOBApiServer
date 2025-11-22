from dependency_injector.wiring import Provide
from fastapi.params import Depends

from src.app.core import route_inject
from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.common.utils.auth import auth_protected
from src.app.main.components.audio_sources import AudioSourceServiceI
from src.app.main.components.common_search import Track
from src.app.main.components.common_search.domain.exceptions import BadSearchObjectTypeHttpException
from src.app.main.components.ym_search import YMSearchServiceI
from src.app.main.di import GlobalContainer
from src.app.main.routing.v1.ym_search.component_router_v1 import ym_search_router_v1
from .dto import AudioSourceSearchResult


@ym_search_router_v1.get("/audio-sources", dependencies=[Depends(auth_protected)], response_model=None)
@route_inject(
    _ym_search_service=Depends(Provide[GlobalContainer.shortcut_ym_search_service]),
    _audio_source_service=Depends(Provide[GlobalContainer.shortcut_audio_source_service])
)
async def ym_search_audio_source_route(
        *,
        query: str,
        _ym_search_service: YMSearchServiceI,
        _audio_source_service: AudioSourceServiceI
) -> ApplicationJsonResponse[AudioSourceSearchResult]:
    media = await _ym_search_service.search(query)

    if type(media) is not Track:
        raise BadSearchObjectTypeHttpException()

    audio_sources = await _ym_search_service.get_audio_sources_for_track(media)

    return SuccessResponse[AudioSourceSearchResult](
        data=AudioSourceSearchResult(
            audio_sources=audio_sources
        )
    )
