from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from googletrans import Translator

from .internal.repositories_impl import TranslationRepositoryImpl
from ..domain import TranslationRepositoryI


class TranslationDataContainer(DeclarativeContainer):
    # Private
    _translator = providers.Singleton[Translator](Translator)

    # Public
    translation_repository = providers.Singleton[TranslationRepositoryI](
        TranslationRepositoryImpl,
        translator=_translator
    )
