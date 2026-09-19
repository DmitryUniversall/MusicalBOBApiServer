import asyncio
from abc import ABC
from typing import Iterable, Optional

from src.app.main.components.common_search import MediaContent, AbstractPlatformSearchService
from src.base.state import project_settings
from src.base.utils.async_tools import gather_for_each
from src.base.utils.url import has_url_scheme


class BasePlatformSearchService(AbstractPlatformSearchService, ABC):
    def _is_url_query(self, query: str) -> bool:
        """
        Tells a link apart from a free-text search query.

        Platforms that can recognize their own scheme-less links (`music.yandex.ru/track/1`)
        are expected to override this.

        :param query: `str`
            Raw user input.

        :return: `bool`
            `True` if the query must be resolved as a url.
        """

        return has_url_scheme(query)

    async def _search(self, query: str) -> MediaContent:
        if self._is_url_query(query):
            return await self.get_by_url(query)
        return await self.get_by_name(query)

    async def search(self, query: str, timeout: Optional[float] = None) -> MediaContent:
        async with asyncio.timeout(delay=timeout or project_settings.SEARCH_CRITICAL_TIMEOUT):
            return await self._search(query)

    async def search_many(self, queries: Iterable[str]) -> tuple[MediaContent, ...]:
        return await gather_for_each(self.search, queries)
