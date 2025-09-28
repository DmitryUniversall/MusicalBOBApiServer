from dependency_injector import containers, providers

from ..internal.adapters import UserModelAdapter
from ..internal.repository import UsersRepositoryImpl


# This container should NOT be imported or used directly. You must use it only through UsersComponentContainer
class DataLayerContainer(containers.DeclarativeContainer):
    # Internal
    _user_model_adapter = providers.Singleton(UserModelAdapter)

    # Public
    users_repository_impl = providers.Singleton(
        UsersRepositoryImpl,
        model_adapter=_user_model_adapter
    )
