from typing import Optional

from dependency_injector.wiring import Provide
from fastapi import Depends

from src.app.core import route_inject
from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.common.utils.auth import auth_protected
from src.app.main.components.common_search import Track, MediaContent, Lyrics
from src.app.main.components.common_search.domain.exceptions import BadSearchObjectTypeHttpException
from src.app.main.components.translation.domain import TranslationServiceI
from src.app.main.components.ym_search.domain import YMSearchServiceI
from src.app.main.di import GlobalContainer
from src.app.main.routing.v1.ym_search.component_router_v1 import ym_search_router_v1
from .dto import LyricsSearchResult


@ym_search_router_v1.get("/lyrics", dependencies=[Depends(auth_protected)], response_model=None)
@route_inject(
    _ym_search_service=Depends(Provide[GlobalContainer.shortcut_ym_search_service]),
    _translation_service=Depends(Provide[GlobalContainer.shortcut_translation_service])
)
async def ym_search_lyrics_route(
        *,
        query: str,
        translate_to: Optional[str] = None,
        _ym_search_service: YMSearchServiceI,
        _translation_service: TranslationServiceI,
) -> ApplicationJsonResponse[LyricsSearchResult]:
    media: MediaContent = await _ym_search_service.search(query)

    if type(media) is not Track:
        raise BadSearchObjectTypeHttpException()

    lyrics: Lyrics = await _ym_search_service.get_lyrics_for_track(media)
    if translate_to is not None:
        lyrics.translations = await _translation_service.translate_many_to_text(lyrics.lyrics, translate_to.split(";"))

    return SuccessResponse[LyricsSearchResult](
        data=LyricsSearchResult(lyrics=lyrics)
    )
