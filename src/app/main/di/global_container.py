from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.components.di import ComponentsContainer
from .utils_container import UtilsContainer


class GlobalContainer(DeclarativeContainer):
    # Lazy dependency is required here to prevent circular imports
    components = providers.Container['ComponentsContainer'](ComponentsContainer)
    utils = providers.Container['UtilsContainer'](UtilsContainer)

    # Shortcuts
    shortcut_auth_service = components.auth.auth_service
    shortcut_jwt_auth_dependency = components.auth.jwt_auth_dependency
    shortcut_ym_search_service = components.ym_search.ym_search_service
    shortcut_translation_service = components.translation.translation_service
