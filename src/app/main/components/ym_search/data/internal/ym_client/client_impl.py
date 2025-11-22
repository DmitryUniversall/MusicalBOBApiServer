import re
from itertools import chain
from logging import getLogger
from typing import Iterable, Optional

import yandex_music
from yandex_music.exceptions import (
    NotFoundError as YMNotFoundError,
    UnauthorizedError as YMUnauthorizedError
)

from src.app.main.components.common_search.domain.exceptions import SearchFailedNotFoundHttpException, BadUrlFormatHttpException
from src.app.main.components.common_search.domain.exceptions.generics import ContentUnavailableHttpException
from src.app.main.components.ym_search.data.internal.ym_client.abc import CustomAsyncYMClientI
from src.base.state import project_settings
from src.base.utils.async_tools import gather_all
from src.base.utils.regex import UUID_REGEX

_logger = getLogger(__name__)


class CustomAsyncYMClientImpl(CustomAsyncYMClientI):
    def __init__(self, *, base_url: Optional[str] = None, **kwargs) -> None:
        super().__init__(**kwargs, base_url=base_url or project_settings.YANDEX_MUSIC_API_BASE_URL)

    async def search_track_by_name(self: yandex_music.ClientAsync, query: str) -> tuple[yandex_music.Track, ...]:
        result = await self.search(text=query, type_='track')

        if not result.tracks:  # If None or empty
            raise SearchFailedNotFoundHttpException(message=f"Nothing found in yandex music for query '{query}'")

        return tuple(result.tracks.results)

    async def get_album_with_tracks_by_url(self, url: str) -> tuple[yandex_music.Album, tuple[yandex_music.Track, ...]]:
        if (match := re.search(r"album/(\d+)", url)) is None:
            raise BadUrlFormatHttpException(message=f"Cannot fetch album from yandex music by url '{url}': invalid url")

        album_id = int(match.group(1))

        return await self.get_album_with_tracks(album_id)

    async def get_track_by_url(self, url: str) -> yandex_music.Track:
        if (match := re.search(r"album/(\d+)/track/(\d+)", url)) is not None:
            album_id, track_id = int(match.group(1)), int(match.group(2))
        elif (match := re.search(r"track/(\d+)", url)) is not None:
            album_id, track_id = int(match.group(1)), int(match.group(1))
        else:
            raise BadUrlFormatHttpException(message=f"Cannot fetch track from yandex music by url '{url}': invalid url")

        return await self.get_track(
            album_id=album_id,
            track_id=track_id
        )

    async def _get_playlist_with_tracks_by_uuid(self, uuid: str) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        raise NotImplementedError()

    async def get_playlist_with_tracks_by_url(self, url: str) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        if (match := re.search(f"playlists/({UUID_REGEX})", url)) is not None:
            return await self._get_playlist_with_tracks_by_uuid(match.group(1))
        elif (match := re.search(r"users/(\S+?)/playlists/(\d+)", url)) is not None:
            return await self.get_playlist(username=match.group(1), playlist_id=int(match.group(2)))

        raise BadUrlFormatHttpException(message=f"Cannot fetch playlist from yandex music by url '{url}': invalid url")

    async def get_audio_sources_by_url(self, url: str) -> tuple[str, ...]:
        track = await self.get_track_by_url(url)
        return await self.get_audio_sources_by_raw(raw=track)

    async def get_lyrics_by_url(self, url: str) -> str:
        track = await self.get_track_by_url(url)
        return await self.get_lyrics_by_raw(raw=track)

    async def get_full_tracks(self, tracks: Iterable[yandex_music.TrackShort]) -> tuple[yandex_music.Track, ...]:
        return await gather_all((short_track.fetch_track_async() for short_track in tracks))

    async def get_track(self, album_id: int, track_id: int) -> yandex_music.Track:
        tracks = await self.tracks(f"{track_id}:{album_id}")

        if len(tracks) == 0:
            raise SearchFailedNotFoundHttpException(message=f"Failed to fetch track from yandex music with {album_id=}; {track_id=}")

        return tracks[0]

    async def get_album_with_tracks(self, album_id: int) -> tuple[yandex_music.Album, tuple[yandex_music.Track, ...]]:
        album = await self.albums_with_tracks(album_id)

        if album.volumes is None:
            raise SearchFailedNotFoundHttpException(message=f"Fetched album (id {album_id}) has no volumes")

        return album, tuple(chain(*album.volumes))

    async def get_playlist(
            self,
            username: str,
            playlist_id: int
    ) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        try:
            playlist = await self.users_playlists(kind=playlist_id, user_id=username)
            return playlist, await self.get_full_tracks(tracks=playlist.tracks)
        except YMNotFoundError as error:
            raise SearchFailedNotFoundHttpException(  # Playlist is private or does not exist
                message=f"Failed to fetch playlist from yandex music with {username=}; {playlist_id=}"
            ) from error

    async def get_audio_sources_by_raw(self, raw: yandex_music.Track) -> tuple[str, ...]:
        try:
            download_info = await raw.get_download_info_async()
            return await gather_all((d_inf.get_direct_link_async() for d_inf in download_info))
        except YMUnauthorizedError as error:
            _logger.warning(f"Failed to get audio sources for track '{raw.track_id}': {error.__class__.__name__}: {error}")
            raise ContentUnavailableHttpException(message=f"Failed to get audio sources for track '{raw.track_id}'") from error

    async def get_lyrics_by_raw(self, raw: yandex_music.Track) -> str:
        supplement = await raw.get_supplement_async()

        if lyrics := supplement.lyrics:
            return lyrics.full_lyrics

        raise SearchFailedNotFoundHttpException(messsage="Failed to get lyrics for specified track")
