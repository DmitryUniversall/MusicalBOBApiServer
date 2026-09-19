from abc import abstractmethod, ABC
from typing import Iterable, Optional

import yandex_music

yandex_music.ClientAsync._ClientAsync__notice_displayed = True


class CustomAsyncYMClientI(ABC, yandex_music.ClientAsync):
    @abstractmethod
    async def search_track_by_name(self: yandex_music.ClientAsync, query: str) -> tuple[yandex_music.Track, ...]:
        ...

    @abstractmethod
    async def get_full_tracks(self, tracks: Iterable[yandex_music.TrackShort]) -> tuple[yandex_music.Track, ...]:
        ...

    @abstractmethod
    async def get_track(self, track_id: str, album_id: Optional[str] = None) -> yandex_music.Track:
        ...

    @abstractmethod
    async def get_album_with_tracks(self, album_id: str) -> tuple[yandex_music.Album, tuple[yandex_music.Track, ...]]:
        ...

    @abstractmethod
    async def get_playlist(self, username: str, playlist_id: str) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        ...

    @abstractmethod
    async def get_playlist_by_uuid(self, playlist_uuid: str) -> tuple[yandex_music.Playlist, tuple[yandex_music.Track, ...]]:
        ...

    @abstractmethod
    async def get_audio_sources_by_raw(self, raw: yandex_music.Track) -> tuple[str, ...]:
        ...

    @abstractmethod
    async def get_lyrics_by_raw(self, raw: yandex_music.Track) -> str:
        ...
