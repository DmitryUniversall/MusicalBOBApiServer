from abc import ABC, abstractmethod

from src.app.main.components.audio_sources import AudioSource
from src.app.main.components.common_search import Playlist, Track, Lyrics
from ..entities import YMAlbumLink, YMPlaylistLink, YMTrackLink


class YMSearchRepositoryI(ABC):
    @abstractmethod
    async def get_album(self, link: YMAlbumLink) -> Playlist:
        ...

    @abstractmethod
    async def get_playlist(self, link: YMPlaylistLink) -> Playlist:
        ...

    @abstractmethod
    async def get_track(self, link: YMTrackLink) -> Track:
        ...

    @abstractmethod
    async def get_audio_sources_for_link(self, link: YMTrackLink) -> tuple[AudioSource, ...]:
        ...

    @abstractmethod
    async def get_lyrics_for_link(self, link: YMTrackLink) -> Lyrics:
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
