from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.common.redis import RedisClientFactory
from .data import AudioSourceDataContainer
from .domain import AudioSourceServiceI
from .services_impl import AudioSourceServiceImpl


class AudioSourceComponentContainer(DeclarativeContainer):
    # Dependencies
    _redis_client_factory = providers.Dependency[RedisClientFactory]()

    # Private
    _data_container = providers.Container[AudioSourceDataContainer](
        AudioSourceDataContainer,
        _redis_client_factory=_redis_client_factory
    )

    # Public
    audio_source_service = providers.Singleton[AudioSourceServiceI](
        AudioSourceServiceImpl,
        _audio_source_repository=_data_container.audio_source_repository
    )
