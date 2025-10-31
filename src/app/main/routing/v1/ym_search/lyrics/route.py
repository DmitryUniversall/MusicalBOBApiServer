from src.app.main.common import ApplicationJsonResponse, SuccessResponse
from src.app.main.components.common_search import Track, MediaContent
from src.app.main.components.common_search.domain.exceptions import BadSearchObjectTypeHttpException
from src.app.main.components.translation.domain import TranslationServiceI
from src.app.main.components.ym_search.domain import YMSearchServiceI
from src.app.main.routing.v1.ym_search.component_router_v1 import ym_search_router_v1
from .dto import LyricsSearchResult


@ym_search_router_v1.get("/lyrics", response_model=None)  # TODO: Add cache
async def ym_search_lyrics_route(query: str, translate_to: str | None = None) -> ApplicationJsonResponse[LyricsSearchResult]:
    _ym_search_service = YMSearchServiceI.get_implementation()  # type: ignore
    _translation_service = TranslationServiceI.get_implementation()  # type: ignore

    media: MediaContent = await _ym_search_service.search(query)

    if type(media) is not Track:
        raise BadSearchObjectTypeHttpException()

    lyrics: str = await _ym_search_service.get_lyrics_for_track(query)

    translations: dict[str, str] = {}
    if translate_to is not None:
        translations.update({
            language_code: await _translation_service.translate(lyrics, language_code)
            for language_code in translate_to.split(";")
        })

    return SuccessResponse[LyricsSearchResult](
        data=LyricsSearchResult(
            lyrics=lyrics,
            translations=translations,
        )
    )
