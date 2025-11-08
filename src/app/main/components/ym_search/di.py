from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from .data import di  # type: ignore
from .data.di import YMSearchDataContainer
from .domain import YMSearchServiceI
from .services_impl import YMSearchServiceImpl


class YMSearchContainer(DeclarativeContainer):
    # Private
    _data_container = providers.Container[YMSearchDataContainer](YMSearchDataContainer)

    # Public
    ym_search_service = providers.Singleton[YMSearchServiceI](YMSearchServiceImpl)
