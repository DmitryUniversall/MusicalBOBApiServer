from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.components.di import ComponentsContainer
from .utils_container import UtilsContainer


class GlobalContainer(DeclarativeContainer):
    utils = providers.Container[UtilsContainer](UtilsContainer)

    components = providers.Container[ComponentsContainer](
        ComponentsContainer,
        _utils_container=utils
    )

    # Shortcuts
    shortcut_auth_service = components.provided.auth.auth_service.call()
    shortcut_jwt_auth_dependency = components.provided.auth.jwt_auth_dependency.call()
    shortcut_ym_search_service = components.provided.ym_search.ym_search_service.call()
    shortcut_translation_service = components.provided.translation.translation_service.call()
    shortcut_audio_source_service = components.provided.audio_sources.audio_source_service.call()
