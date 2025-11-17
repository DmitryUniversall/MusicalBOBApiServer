from abc import ABC, abstractmethod
from typing import Iterable, Optional

from src.app.main.components.audio_sources import AudioSource
from ..entities import MediaContent, Lyrics, Track


class AbstractPlatformSearchService(ABC):
    @abstractmethod
    async def get_by_url(self, url: str) -> MediaContent:
        ...

    @abstractmethod
    async def get_by_name(self, query: str) -> MediaContent:
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
    async def search(self, query: str, timeout: Optional[float] = None) -> MediaContent:
        ...

    @abstractmethod
    async def search_many(self, queries: Iterable[str]) -> tuple[MediaContent, ...]:
        ...
