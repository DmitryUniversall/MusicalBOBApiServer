from abc import ABC, abstractmethod
from typing import Optional, Iterable

from src.app.main.components.common_search import SearchEntity, Track, Playlist


class SearchCacheServiceI(ABC):
    @abstractmethod
    async def get_cached_track_by_source(self, source: str) -> Optional[Track]:
        ...

    @abstractmethod
    async def get_cached_playlist_by_source(self, source: str) -> Optional[Playlist]:
        ...

    @abstractmethod
    async def cache_search_entity(self, entity: SearchEntity) -> None:
        ...

    @abstractmethod
    async def cache_search_entities(self, entities: Iterable[SearchEntity]) -> None:
        ...
