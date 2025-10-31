from abc import ABC, abstractmethod
from typing import Optional, Iterable

from src.app.main.components.common_search import Track
from src.app.main.components.common_search.domain.entities.audio_sources import AudioSource
from src.app.main.components.common_search.domain.entities.media_content import MediaContent
from src.base.utils.async_tools import gather_for_each


class AbstractPlatformSearchService(ABC):
    def __str__(self) -> str:
        return self.__class__.__name__

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
    async def get_lyrics_by_url(self, url: str) -> Optional[str]:
        ...

    @abstractmethod
    async def get_audio_sources_for_track(self, track: Track) -> tuple[AudioSource, ...]:
        ...

    @abstractmethod
    async def get_lyrics_for_track(self, track: Track) -> str:
        ...

    async def search(self, query: str) -> MediaContent:
        if query.startswith("https://"):
            return await self.get_by_url(query)
        return await self.get_by_name(query)

    async def search_many(self, queries: Iterable[str]) -> tuple[MediaContent, ...]:
        return await gather_for_each(self.search, queries)
