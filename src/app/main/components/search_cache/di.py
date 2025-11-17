from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.common.redis import RedisClientFactory
from .data import SearchCacheDataContainer
from .domain import SearchCacheServiceI
from .services_impl import SearchCacheServiceImpl


class SearchCacheComponentContainer(DeclarativeContainer):
    # Dependencies
    _redis_client_factory = providers.Dependency[RedisClientFactory]()

    # Private
    _data_container = providers.Container(
        SearchCacheDataContainer,
        _redis_client_factory=_redis_client_factory
    )

    # Public
    search_cache_service = providers.Singleton[SearchCacheServiceI](
        SearchCacheServiceImpl,
        _search_cache_repository=_data_container.search_cache_repository
    )
