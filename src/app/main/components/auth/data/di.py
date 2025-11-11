from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.common.redis.redis_client_factory import RedisClientFactory
from src.app.main.components.auth.domain import AuthSessionRepositoryI, AuthRepositoryI
from src.base.state import project_settings
from .internal.repositories_impl import AuthSessionRepositoryRedisImpl, AuthRepositoryImpl


class AuthDataContainer(DeclarativeContainer):
    # Dependencies
    _redis_client_factory = providers.Dependency[RedisClientFactory]()

    # Private
    _redis_client = providers.Resource(
        _redis_client_factory.provided.call().get_client.call(
            db=project_settings.AUTH_REDIS_DB_ID
        )
    )

    # Public
    auth_repository = providers.Singleton[AuthRepositoryI](AuthRepositoryImpl)

    auth_session_repository = providers.Singleton[AuthSessionRepositoryI](
        AuthSessionRepositoryRedisImpl,
        auth_repository=auth_repository,
        redis_client=_redis_client
    )
