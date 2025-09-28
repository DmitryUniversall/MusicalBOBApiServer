from dependency_injector import providers, containers

from ..data import DataLayerContainer
from ..domain import UsersRepository, UsersService


# This container should NOT be imported or used directly. You must use it only through ApplicationContainer
class UsersComponentContainer(containers.DeclarativeContainer):
    # Private (Dependency-containers)
    _data_container = providers.Container(DataLayerContainer)

    # Private
    _users_repository = providers.Dependency(UsersRepository).override(
        _data_container.users_repository_impl
    )

    # Public
    users_service = providers.Singleton(
        UsersService,
        user_repo=_users_repository
    )
