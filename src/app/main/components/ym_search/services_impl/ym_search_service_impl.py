from typing import Optional, re

from src.app.main.components.common_search import AudioSource, MediaContent
from ..domain import YMSearchServiceI
from ..domain.repositories import YMSearchRepositoryI
from ...common_search.domain.exceptions import BadUrlFormatHttpException, SearchFailedNotFoundHttpException


class YMSearchServiceImpl(YMSearchServiceI):
    def __init__(self) -> None:
        self._ym_search_repository: YMSearchRepositoryI = YMSearchRepositoryI.get_implementation()

    async def search_by_url(self, url: str) -> MediaContent:
        if not url.startswith("https://music.yandex.ru"):
            raise BadUrlFormatHttpException(message=f"Cannot fetch media from yandex music: invalid url")

        if re.search(r"/track/\d+/?", url):
            return await self._ym_search_repository.get_track_by_url(url=url)
        elif re.search(r"album/\d+", url):
            return await self._ym_search_repository.get_album_by_url(url=url)
        elif re.search(r"users/(\S+?)/playlists/(\d+)", url):
            return await self._ym_search_repository.get_playlist_by_url(url=url)

        raise BadUrlFormatHttpException(message=f"Cannot fetch media from yandex music: invalid url")

    async def search_by_name(self, query: str) -> MediaContent:  # TODO
        tracks = await self._ym_search_repository.search_track_by_name(query)

        if not tracks:
            raise SearchFailedNotFoundHttpException(message=f"Failed fetch media from yandex music: nothing found")

        best_track = tracks[0]
        best_track.variations = tracks[1:]

        return best_track

    async def get_audio_sources(self, url: str) -> tuple[AudioSource]:
        pass

    async def get_lyrics(self, url: str) -> Optional[str]:
        pass
