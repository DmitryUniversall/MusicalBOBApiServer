from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.common.redis.redis_client_factory import RedisClientFactory


class UtilsContainer(DeclarativeContainer):
    redis_client_factory = providers.Singleton[RedisClientFactory](RedisClientFactory)
