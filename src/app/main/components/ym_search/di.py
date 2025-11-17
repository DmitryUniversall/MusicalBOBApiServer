from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from .data import di  # type: ignore
from .data.di import YMSearchDataContainer
from .domain import YMSearchServiceI
from .services_impl import YMSearchServiceImpl
from ..audio_sources import AudioSourceServiceI
from ..search_cache import SearchCacheServiceI


class YMSearchComponentContainer(DeclarativeContainer):
    # Dependencies
    _audio_source_service = providers.Dependency[AudioSourceServiceI]()
    _search_cache_service = providers.Dependency[SearchCacheServiceI]()

    # Private
    _data_container = providers.Container[YMSearchDataContainer](
        YMSearchDataContainer,
        _audio_source_service=_audio_source_service.provided,
        _search_cache_service=_search_cache_service.provided,
    )

    # Public
    ym_search_service = providers.Singleton[YMSearchServiceI](
        YMSearchServiceImpl,
        _ym_search_repository=_data_container.ym_search_repository
    )
