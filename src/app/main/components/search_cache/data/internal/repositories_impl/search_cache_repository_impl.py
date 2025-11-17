from typing import Optional, Iterable

from redis import asyncio as aioredis

from src.app.main.common.redis import RedisCache
from src.app.main.components.common_search import SearchEntity
from src.app.main.components.search_cache.domain import SearchCacheRepositoryI
from src.base.state import project_settings
from src.base.utils.async_tools import gather_all


class SearchCacheRepositoryImpl(SearchCacheRepositoryI):
    def __init__(
            self,
            _redis_client: aioredis.client.Redis
    ) -> None:
        self._redis_client = _redis_client
        self._cache = RedisCache(
            redis_client=self._redis_client,
            key=project_settings.SEARCH_CACHE_REDIS_KEY,
            max_size=project_settings.SEARCH_CACHE_MAX_SIZE
        )

    async def get_cached_search_entity_by_source[T: SearchEntity](self, source: str, schema_cls: type[T]) -> Optional[T]:
        return await self._cache.read_schema(source, schema_cls=schema_cls)

    async def cache_search_entity[T: SearchEntity](self, entity: T) -> None:
        return await self._cache.write_schema(entity.source, entity)

    async def cache_search_entities[T: SearchEntity](self, entities: Iterable[T]) -> None:
        await gather_all(self.cache_search_entity(entity) for entity in entities)
