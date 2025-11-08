from abc import ABC, abstractmethod

from src.app.main.components.common_search import Playlist, Track, AudioSource, Lyrics


class YMSearchRepositoryI(ABC):
    @abstractmethod
    async def get_album_by_url(self, url: str) -> Playlist:
        ...

    @abstractmethod
    async def get_playlist_by_url(self, url: str) -> Playlist:
        ...

    @abstractmethod
    async def get_track_by_url(self, url: str) -> Track:
        ...

    @abstractmethod
    async def get_audio_sources_by_url(self, url: str) -> tuple[AudioSource, ...]:
        ...

    @abstractmethod
    async def get_lyrics_by_url(self, url: str) -> Lyrics:
        ...

    @abstractmethod
    async def get_audio_sources_for_track(self, track: Track) -> tuple[AudioSource, ...]:
        ...

    @abstractmethod
    async def get_lyrics_for_track(self, track: Track) -> Lyrics:
        ...

    @abstractmethod
    async def search_track_by_name(self, query: str) -> Track:
        ...
