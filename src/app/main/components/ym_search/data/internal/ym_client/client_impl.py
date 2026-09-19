from itertools import chain
from logging import getLogger
from typing import Iterable, Optional

import yandex_music
from yandex_music.exceptions import (
    NotFoundError as YMNotFoundError,
    UnauthorizedError as YMUnauthorizedError
)

from src.app.main.components.common_search.domain.exceptions import SearchFailedNotFoundHttpException
from src.app.main.components.common_search.domain.exceptions.generics import ContentUnavailableHttpException
from src.app.main.components.ym_search.data.internal.ym_client.abc import CustomAsyncYMClientI
from src.base.state import project_settings
from src.base.utils.async_tools import gather_all

_logger = getLogger(__name__)


class CustomAsyncYMClientImpl(CustomAsyncYMClientI):
    def __init__(self, *, base_url: Optional[str] = None, **kwargs) -> None:
        super().__init__(**kwargs, base_url=base_url or project_settings.YANDEX_MUSIC_API_BASE_URL)

    async def search_track_by_name(self: yandex_music.ClientAsync, query: str) -> tuple[yandex_music.Track, ...]:
        result = await self.search(text=query, type_='track')

        if not result.tracks:  # If None or empty
            raise SearchFailedNotFoundHttpException(message=f"Nothing found in yandex music for query '{query}'")

        return tuple(result.tracks.results)

    async def get_full_tracks(self, tracks: Iterable[yandex_music.TrackShort]) -> tuple[yandex_music.Track, ...]:
        return await gather_all((short_track.fetch_track_async() for short_track in tracks))

    async def get_track(self, track_id: str, album_id: Optional[str] = None) -> yandex_music.Track:
        # Album is a context hint only: passing a wrong one is worse than passing none
        tracks = await self.tracks(f"{track_id}:{album_id}" if album_id is not None else track_id)

        if len(tracks) == 0:
            raise SearchFailedNotFoundHttpException(message=f"Failed to fetch track from yandex music with {track_id=}; {album_id=}")

        return tracks[0]

    async def get_album_with_tracks(self, album_id: str) -> tuple[yandex_music.Album, tuple[yandex_music.Track, ...]]:
        album = await self.albums_with_tracks(album_id)

        if album.volumes is None:
            raise SearchFailedNotFoundHttpException(message=f"Fetched album (id {album_id}) has no volumes")

        return album, tuple(chain(*album.volumes))

    async def _playlist_with_tracks(self, playlist: Optional[yandex_music.Playlist], not_found_message: str) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        if playlist is None:
            raise SearchFailedNotFoundHttpException(message=not_found_message)

        tracks = playlist.tracks if playlist.tracks is not None else await playlist.fetch_tracks_async()

        return playlist, await self.get_full_tracks(tracks=tracks)

    async def get_playlist(
            self,
            username: str,
            playlist_id: str
    ) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        message = f"Failed to fetch playlist from yandex music with {username=}; {playlist_id=}"

        try:
            playlist = await self.users_playlists(kind=playlist_id, user_id=username)
        except YMNotFoundError as error:
            raise SearchFailedNotFoundHttpException(message=message) from error  # Playlist is private or does not exist

        return await self._playlist_with_tracks(playlist, message)

    async def get_playlist_by_uuid(self, playlist_uuid: str) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        # Playlists shared by link are addressed by uuid (optionally prefixed with "lk."/"ps.")
        # and are served by an endpoint that yandex-music 2.2.0 does not wrap
        message = f"Failed to fetch playlist from yandex music with {playlist_uuid=}"

        try:
            result = await self._request.get(f"{self.base_url}/playlist/{playlist_uuid}")
        except YMNotFoundError as error:
            raise SearchFailedNotFoundHttpException(message=message) from error  # Playlist is private or does not exist

        return await self._playlist_with_tracks(yandex_music.Playlist.de_json(result, self), message)

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

        raise SearchFailedNotFoundHttpException(message="Failed to get lyrics for specified track")
