from typing import TYPE_CHECKING

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from .auth.di import AuthComponentContainer
from .translation.di import TranslationComponentContainer
from .users.di import UsersComponentContainer
from .ym_search.di import YMSearchComponentContainer

if TYPE_CHECKING:
    from src.app.main.di import UtilsContainer


class ComponentsContainer(DeclarativeContainer):
    # Dependencies
    _utils_container: providers.Dependency['UtilsContainer'] = providers.Dependency()

    # Public
    users = providers.Container[UsersComponentContainer](UsersComponentContainer)

    auth = providers.Container[AuthComponentContainer](
        AuthComponentContainer,
        _users_container=users,
        _redis_client_factory=_utils_container.provided.redis_client_factory
    )

    translation = providers.Container[TranslationComponentContainer](TranslationComponentContainer)

    ym_search = providers.Container[YMSearchComponentContainer](YMSearchComponentContainer)
