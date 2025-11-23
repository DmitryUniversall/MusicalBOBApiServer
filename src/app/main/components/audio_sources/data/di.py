from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.common.redis import RedisClientFactory
from src.app.main.components.audio_sources.domain import AudioSourceRepositoryI
from src.base.state import project_settings
from .internal import AudioSourceRepositoryRedisImpl


class AudioSourceDataContainer(DeclarativeContainer):
    # Dependencies
    _redis_client_factory = providers.Dependency[RedisClientFactory]()

    # Private
    _redis_client = providers.Resource(
        _redis_client_factory.provided.call().get_client.call(
            db=project_settings.REDIS_DB_ID
        )
    )

    # Public
    audio_source_repository = providers.Singleton[AudioSourceRepositoryI](
        AudioSourceRepositoryRedisImpl,
        redis_client=_redis_client
    )
