from abc import abstractmethod, ABC
from typing import Optional, Iterable

import yandex_music

from src.base.utils.interface import InterfaceMeta

yandex_music.ClientAsync._ClientAsync__notice_displayed = True


class CustomYandexMusicClientI(ABC, yandex_music.ClientAsync, metaclass=InterfaceMeta):
    @abstractmethod
    async def search_track_by_name(self: yandex_music.ClientAsync, query: str) -> tuple[yandex_music.Track, ...]:
        ...

    @abstractmethod
    async def get_album_with_tracks_by_url(self, url: str) -> tuple[yandex_music.Album, tuple[yandex_music.Track, ...]]:
        ...

    @abstractmethod
    async def get_track_by_url(self, url: str) -> yandex_music.Track:
        ...

    @abstractmethod
    async def get_playlist_with_tracks_by_url(self, url: str) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        ...

    @abstractmethod
    async def get_audio_sources_by_url(self, url: str) -> tuple[str, ...]:
        ...

    @abstractmethod
    async def get_lyrics_by_url(self, url: str) -> str:
        ...

    @abstractmethod
    async def get_full_tracks(self, tracks: Iterable[yandex_music.TrackShort]) -> tuple[yandex_music.Track, ...]:
        ...

    @abstractmethod
    async def get_track(self, album_id: int, track_id: int) -> yandex_music.Track:
        ...

    @abstractmethod
    async def get_album_with_tracks(self, album_id: int) -> tuple[yandex_music.Album, tuple[yandex_music.Track, ...]]:
        ...

    @abstractmethod
    async def get_playlist(self, username: str, playlist_id: int) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        ...

    @abstractmethod
    async def get_audio_sources_by_raw(self, raw: yandex_music.Track) -> tuple[str, ...]:
        ...

    @abstractmethod
    async def get_lyrics_by_raw(self, raw: yandex_music.Track) -> str:
        ...
