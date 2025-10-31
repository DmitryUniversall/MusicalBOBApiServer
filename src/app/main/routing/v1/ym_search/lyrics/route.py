from functools import lru_cache
from typing import Optional

from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.common_search import Track, MediaContent
from src.app.main.components.common_search.domain.exceptions import SearchFailedNotFoundHttpException
from src.app.main.routing.v1.ym_search import ym_search_router_v1
from src.app.main.routing.v1.ym_search.lyrics.dto import LyricsSearchResult

_ym_search_service = YMSearchServiceI.get_implementation()  # type: ignore
_translation_service = TranslationServiceI.get_implementation()  # type: ignore


@ym_search_router_v1.get("/lyrics")
@lru_cache(maxsize=None)
def ym_search_lyrics_route(query: str, translate_to: Optional[str] = None) -> ApplicationJsonResponse[LyricsSearchResult]:
    media: MediaContent = _ym_search_service.search(query)

    if type(media) is not Track:
        raise SearchFailedNotFoundHttpException(message="Specified object cannot have lyrics")

    lyrics: Optional[str] = _ym_search_service.get_lyrics_for_track(query)

    translations: Optional[dict[str, str]] = None
    if translate_to is not None:
        translations = {language_code: _translation_service.translate_to(lyrics, language_code) for language_code in translate_to.split(";")}

    return SuccessResponse[LyricsSearchResult](
        data=LyricsSearchResult(
            lyrics=lyrics,
            translations=translations,
        )
    )
