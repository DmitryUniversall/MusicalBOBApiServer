import logging

from src.app.main.components.audio_sources import AudioSource
from src.app.main.components.common_search import (
    MediaContent,
    Track,
    Lyrics,
    BadSearchObjectTypeHttpException,
    BadUrlFormatHttpException,
    SearchFailedNotFoundHttpException
)
from ..domain import YMSearchServiceI
from ..domain.entities import (
    YMAlbumLink,
    YMLink,
    YMSearchLink,
    YMSharedPlaylistLink,
    YMTrackLink,
    YMUserPlaylistLink,
    is_ym_url,
    parse_ym_link
)
from ..domain.repositories import YMSearchRepositoryI

_logger = logging.getLogger(__name__)


class YMSearchServiceImpl(YMSearchServiceI):
    def __init__(
            self,
            _ym_search_repository: YMSearchRepositoryI
    ) -> None:
        self._ym_search_repository = _ym_search_repository

    def _is_url_query(self, query: str) -> bool:
        return is_ym_url(query)

    def _parse_url(self, url: str) -> YMLink:
        link = parse_ym_link(url)

        if link is None:
            # Yandex changes url shapes from time to time; this log line is how we learn
            # about it before users start reporting broken links
            _logger.warning(f"Unrecognized yandex music url: {url!r}")
            raise BadUrlFormatHttpException(message="Cannot fetch media from yandex music: invalid url")

        return link

    def _parse_track_url(self, url: str) -> YMTrackLink:
        link = self._parse_url(url)

        if not isinstance(link, YMTrackLink):
            raise BadSearchObjectTypeHttpException(
                message="Cannot fetch media from yandex music: url does not point to a track"
            )

        return link

    async def get_by_url(self, url: str) -> MediaContent:
        match self._parse_url(url):
            case YMTrackLink() as link:
                return await self._ym_search_repository.get_track(link)
            case YMAlbumLink() as link:
                return await self._ym_search_repository.get_album(link)
            case YMUserPlaylistLink() | YMSharedPlaylistLink() as link:
                return await self._ym_search_repository.get_playlist(link)
            case YMSearchLink() as link:
                return await self.get_by_name(link.query)
            case link:
                raise BadSearchObjectTypeHttpException(
                    message=f"Cannot fetch media from yandex music: {type(link).__name__} is not supported yet"
                )

    async def get_by_name(self, query: str) -> MediaContent:
        track = await self._ym_search_repository.search_track_by_name(query)

        if track is None:
            raise SearchFailedNotFoundHttpException(message=f"Failed fetch media from yandex music: nothing found")

        return track

    async def get_audio_sources_by_url(self, url: str) -> tuple[AudioSource, ...]:
        return await self._ym_search_repository.get_audio_sources_for_link(self._parse_track_url(url))

    async def get_audio_sources_for_track(self, track: Track) -> tuple[AudioSource, ...]:
        return await self._ym_search_repository.get_audio_sources_for_track(track=track)

    async def get_lyrics_by_url(self, url: str) -> Lyrics:
        return await self._ym_search_repository.get_lyrics_for_link(self._parse_track_url(url))

    async def get_lyrics_for_track(self, track: Track) -> Lyrics:
        return await self._ym_search_repository.get_lyrics_for_track(track=track)
