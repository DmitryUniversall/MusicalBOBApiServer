from abc import ABC, abstractmethod
from typing import Optional

from src.app.main.components.common_search import Playlist, Track, AudioSource
from src.base.utils.interface import InterfaceMeta


class YMSearchRepositoryI(ABC, metaclass=InterfaceMeta):
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
    async def search_track_by_name(self, query: str) -> Optional[Track]:
        ...

    @abstractmethod
    async def get_audio_sources(self, url: str) -> tuple[AudioSource, ...]:
        ...

    @abstractmethod
    async def get_lyrics(self, url: str) -> Optional[str]:
        ...
