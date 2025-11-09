from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from .auth.di import AuthComponentContainer
from .translation.di import TranslationComponentContainer
from .users.di import UsersComponentContainer
from .ym_search.di import YMSearchComponentContainer


class ComponentsContainer(DeclarativeContainer):
    users = providers.Container[UsersComponentContainer](UsersComponentContainer)
    auth = providers.Container[AuthComponentContainer](AuthComponentContainer)
    translation = providers.Container[TranslationComponentContainer](TranslationComponentContainer)
    ym_search = providers.Container[YMSearchComponentContainer](YMSearchComponentContainer)
