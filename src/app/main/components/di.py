from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.components.auth.di import AuthComponentContainer
from src.app.main.components.translation.di import TranslationComponentContainer
from src.app.main.components.users.di import UsersComponentContainer
from src.app.main.components.ym_search.data.internal.repositories import YMSearchRepositoryImpl


class ComponentsContainer(DeclarativeContainer):
    users = providers.Container[UsersComponentContainer](UsersComponentContainer)
    auth = providers.Container[AuthComponentContainer](AuthComponentContainer)
    translation = providers.Container[TranslationComponentContainer](TranslationComponentContainer)
    ym_search = providers.Container[YMSearchRepositoryImpl](YMSearchRepositoryImpl)
