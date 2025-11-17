import asyncio
from abc import ABC
from typing import Optional, Iterable

from src.app.main.components.common_search import MediaContent, AbstractPlatformSearchService
from src.base.state import project_settings
from src.base.utils.async_tools import gather_for_each


class BasePlatformSearchService(AbstractPlatformSearchService, ABC):
    async def _search(self, query: str) -> MediaContent:
        if query.startswith("https://"):
            return await self.get_by_url(query)
        return await self.get_by_name(query)

    async def search(self, query: str, timeout: Optional[float] = None) -> MediaContent:
        async with asyncio.timeout(delay=timeout or project_settings.SEARCH_CRITICAL_TIMEOUT):
            return await self._search(query)

    async def search_many(self, queries: Iterable[str]) -> tuple[MediaContent, ...]:
        return await gather_for_each(self.search, queries)
