import logging

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.components.audio_sources import AudioSourceServiceI
from src.app.main.components.search_cache import SearchCacheServiceI
from src.base.state import project_settings
from .internal.repositories import YMSearchRepositoryImpl
from .internal.ym_client import CustomAsyncYMClientI, CustomAsyncYMClientImpl
from ..domain.repositories import YMSearchRepositoryI

_logger = logging.getLogger(__name__)


@providers.Resource
async def _ym_client() -> CustomAsyncYMClientI:
    _logger.info("Initializing YM Search Client")
    client = CustomAsyncYMClientImpl(token=project_settings.YANDEX_MUSIC_TOKEN)
    await client.init()
    return client


class YMSearchDataContainer(DeclarativeContainer):
    # Dependencies
    _audio_source_service = providers.Dependency[AudioSourceServiceI]()
    _search_cache_service = providers.Dependency[SearchCacheServiceI]()

    # Public
    ym_search_repository = providers.Singleton[YMSearchRepositoryI](
        YMSearchRepositoryImpl,
        _ym_client=_ym_client,
        _audio_source_service=_audio_source_service.provided,
        _search_cache_service=_search_cache_service.provided
    )
