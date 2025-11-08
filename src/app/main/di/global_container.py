from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from src.app.main.components.di import ComponentsContainer
from .utils_container import UtilsContainer


class GlobalContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        modules=["src.app.main.routing"]
    )

    components = providers.Container[ComponentsContainer](ComponentsContainer)
    utils = providers.Container[UtilsContainer](UtilsContainer)

    # Shortcuts
    shortcut_auth_service = components.provided.auth.provided.auth_service
    shortcut_jwt_auth_dependency = components.provided.auth.provided.jwt_auth_dependency
    shortcut_ym_search_service = components.provided.ym_search.provided.ym_search_service
    shortcut_translation_service = components.provided.translation.provided.translation_service
