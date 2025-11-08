from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from .data import di  # type: ignore
from .data.di import TranslationDataContainer
from .domain import TranslationServiceI
from .services_impl import TranslationServiceImpl


class TranslationComponentContainer(DeclarativeContainer):
    _data_container = providers.Container[TranslationDataContainer](TranslationDataContainer)

    translation_service = providers.Singleton[TranslationServiceI](
        TranslationServiceImpl,
        translation_repository=_data_container.provided.translation_repository
    )
