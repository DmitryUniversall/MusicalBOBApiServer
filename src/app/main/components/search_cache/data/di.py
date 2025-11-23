from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.common.redis import RedisClientFactory
from src.app.main.components.search_cache.domain import SearchCacheRepositoryI
from src.base.state import project_settings
from .internal import SearchCacheRepositoryImpl


class SearchCacheDataContainer(DeclarativeContainer):
    # Dependencies
    _redis_client_factory = providers.Dependency[RedisClientFactory]()

    # Private
    _redis_client = providers.Resource(
        _redis_client_factory.provided.call().get_client.call(
            db=project_settings.REDIS_DB_ID
        )
    )

    # Public
    search_cache_repository = providers.Singleton[SearchCacheRepositoryI](
        SearchCacheRepositoryImpl,
        _redis_client=_redis_client
    )
