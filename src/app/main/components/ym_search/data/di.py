from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.base.state import project_settings
from .internal.repositories import YMSearchRepositoryImpl
from .internal.ym_client import CustomAsyncYMClientI, CustomAsyncYMClientImpl
from ..domain.repositories import YMSearchRepositoryI


@providers.Resource
async def _ym_client() -> CustomAsyncYMClientI:
    client = CustomAsyncYMClientImpl(token=project_settings.YANDEX_MUSIC_TOKEN)
    await client.init()
    return client


class YMSearchDataContainer(DeclarativeContainer):
    ym_search_repository = providers.Singleton[YMSearchRepositoryI](
        YMSearchRepositoryImpl,
        ym_client=_ym_client
    )
