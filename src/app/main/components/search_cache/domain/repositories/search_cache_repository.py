from abc import ABC, abstractmethod
from typing import Optional, Iterable

from src.app.main.components.common_search import SearchEntity


class SearchCacheRepositoryI(ABC):
    @abstractmethod
    async def get_cached_search_entity_by_source[T: SearchEntity](self, source: str, schema_cls: type[T]) -> Optional[T]:
        ...

    @abstractmethod
    async def cache_search_entity[T: SearchEntity](self, entity: T) -> None:
        ...

    @abstractmethod
    async def cache_search_entities[T: SearchEntity](self, entities: Iterable[T]) -> None:
        ...
