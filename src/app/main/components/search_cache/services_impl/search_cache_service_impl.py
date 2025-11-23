from typing import Iterable, Optional

from src.app.main.components.common_search import Track, Playlist, SearchEntity
from src.app.main.components.search_cache.domain import SearchCacheRepositoryI, SearchCacheServiceI


class SearchCacheServiceImpl(SearchCacheServiceI):
    def __init__(self, _search_cache_repository: SearchCacheRepositoryI) -> None:
        self._search_cache_repository = _search_cache_repository

    async def get_cached_track_by_source(self, source: str) -> Optional[Track]:
        return await self._search_cache_repository.get_cached_search_entity_by_source(source, Track)

    async def get_cached_playlist_by_source(self, source: str) -> Optional[Playlist]:
        return await self._search_cache_repository.get_cached_search_entity_by_source(source, Playlist)

    async def cache_search_entity(self, entity: SearchEntity) -> None:
        await self._search_cache_repository.cache_search_entity(entity)

    async def cache_search_entities(self, entities: Iterable[SearchEntity]) -> None:
        await self._search_cache_repository.cache_search_entities(entities)
