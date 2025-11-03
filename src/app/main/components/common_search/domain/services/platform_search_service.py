import asyncio
from abc import ABC, abstractmethod
from typing import Iterable

from src.app.main.components.common_search.domain.entities import Track, AudioSource, MediaContent, Lyrics
from src.base.state import project_settings
from src.base.utils.async_tools import gather_for_each
from src.base.utils.syntax import default_any


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

    async def _search(self, query: str) -> MediaContent:
        if query.startswith("https://"):
            return await self.get_by_url(query)
        return await self.get_by_name(query)

    async def search(self, query: str, timeout: int = None) -> MediaContent:
        with asyncio.timeout(delay=default_any(timeout, project_settings.SEARCH_CRITICAL_TIMEOUT)):
            return await self._search(query)

    async def search_many(self, queries: Iterable[str]) -> tuple[MediaContent, ...]:
        return await gather_for_each(self.search, queries)
