from abc import ABC, abstractmethod
from typing import Optional, Iterable

from src.app.main.components.common_search.domain.entities.audio_sources import AudioSource
from src.app.main.components.common_search.domain.entities.media_content import MediaContent
from src.base.utils.async_tools import gather_all


class AbstractPlatformSearchService(ABC):
    def __str__(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    async def search_by_url(self, url: str) -> MediaContent:
        ...

    @abstractmethod
    async def search_by_name(self, query: str) -> MediaContent:
        ...

    @abstractmethod
    async def get_audio_sources(self, url: str) -> tuple[AudioSource]:
        ...

    @abstractmethod
    async def get_lyrics(self, url: str) -> Optional[str]:
        ...

    async def search(self, query: str) -> MediaContent:
        if query.startswith("https://"):
            return await self.search_by_url(query)
        return await self.search_by_name(query)

    async def search_many(self, queries: Iterable[str]) -> tuple[MediaContent, ...]:
        return await gather_all((self.search(query) for query in queries))

    async def search_by_url_many(self, urls: Iterable[str]) -> tuple[MediaContent, ...]:
        return await gather_all((self.search_by_name(url) for url in urls))

    async def get_by_name_many(self, queries: Iterable[str]) -> tuple[MediaContent, ...]:
        return await gather_all((self.search_by_name(query) for query in queries))

    async def get_audio_sources_many(self, urls: Iterable[str]) -> tuple[tuple[AudioSource, ...], ...]:
        return await gather_all((self.get_audio_sources(query) for query in urls))

    async def get_lyrics_many(self, urls: Iterable[str]) -> tuple[Optional[str], ...]:
        return await gather_all((self.get_lyrics(query) for query in urls))
