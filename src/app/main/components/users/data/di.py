from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.components.users.data.internal.adapters import UserModelAdapter
from src.app.main.components.users.data.internal.repositories_impl import UsersRepositoryImpl
from src.app.main.components.users.domain import UsersRepositoryI


class UsersDataContainer(DeclarativeContainer):
    # Private
    _user_model_adapter = providers.Singleton[UserModelAdapter](UserModelAdapter)

    # Public
    users_repository = providers.Singleton[UsersRepositoryI](
        UsersRepositoryImpl,
        user_model_adapter=_user_model_adapter
    )
