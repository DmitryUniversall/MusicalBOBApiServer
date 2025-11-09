import re

from src.app.main.components.common_search import AudioSource, MediaContent, Track, Lyrics
from src.app.main.components.common_search.domain.exceptions import BadUrlFormatHttpException, SearchFailedNotFoundHttpException
from ..domain import YMSearchServiceI
from ..domain.repositories import YMSearchRepositoryI


class YMSearchServiceImpl(YMSearchServiceI):
    def __init__(self, ym_search_repository: YMSearchRepositoryI) -> None:
        self._ym_search_repository = ym_search_repository

    async def get_by_url(self, url: str) -> MediaContent:
        if not url.startswith("https://music.yandex.ru"):
            raise BadUrlFormatHttpException(message=f"Cannot fetch media from yandex music: invalid url")

        if re.search(r"/track/\d+/?", url):
            return await self._ym_search_repository.get_track_by_url(url=url)
        elif re.search(r"album/\d+", url):
            return await self._ym_search_repository.get_album_by_url(url=url)
        elif re.search(r"users/(\S+?)/playlists/(\d+)", url):
            return await self._ym_search_repository.get_playlist_by_url(url=url)

        raise BadUrlFormatHttpException(message=f"Cannot fetch media from yandex music: invalid url")

    async def get_by_name(self, query: str) -> MediaContent:
        track = await self._ym_search_repository.search_track_by_name(query)

        if track is None:
            raise SearchFailedNotFoundHttpException(message=f"Failed fetch media from yandex music: nothing found")

        return track

    async def get_audio_sources_by_url(self, url: str) -> tuple[AudioSource, ...]:
        return await self._ym_search_repository.get_audio_sources_by_url(url)

    async def get_lyrics_by_url(self, url: str) -> Lyrics:
        return await self._ym_search_repository.get_lyrics_by_url(url=url)

    async def get_audio_sources_for_track(self, track: Track) -> tuple[AudioSource, ...]:
        return await self._ym_search_repository.get_audio_sources_for_track(track=track)

    async def get_lyrics_for_track(self, track: Track) -> Lyrics:
        return await self._ym_search_repository.get_lyrics_for_track(track=track)
