from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.auth import jwt_protected
from src.app.main.components.common_search import Track, MediaContent, AudioSource
from src.app.main.components.common_search.domain.exceptions import BadSearchObjectTypeHttpException
from src.app.main.components.translation.domain import TranslationServiceI
from src.app.main.components.ym_search.domain import YMSearchServiceI
from src.app.main.routing.v1.ym_search.component_router_v1 import ym_search_router_v1
from .dto import AudioSourcesSearchResult

_ym_search_service = YMSearchServiceI.get_implementation()  # type: ignore
_translation_service = TranslationServiceI.get_implementation()  # type: ignore


@ym_search_router_v1.get("/audio_sources", response_model=None)
@jwt_protected
async def ym_search_audio_source_route(query: str) -> ApplicationJsonResponse[AudioSourcesSearchResult]:
    media: MediaContent = await _ym_search_service.search(query)

    if type(media) is not Track:
        raise BadSearchObjectTypeHttpException()

    audio_sources: tuple[AudioSource, ...] = await _ym_search_service.get_audio_sources_for_track(media)
    return SuccessResponse[AudioSourcesSearchResult](
        data=AudioSourcesSearchResult(audio_sources=audio_sources)
    )
