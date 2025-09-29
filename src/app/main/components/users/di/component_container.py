from dependency_injector import providers, containers

from ..data import UsersDataLayerContainer
from ..domain import UsersRepository, AbstractUsersService
from ..domain.service_impl import UsersServiceImpl


class UsersComponentContainer(containers.DeclarativeContainer):
    # Private (Dependency-containers)
    _data_container = providers.Container(
        UsersDataLayerContainer
    )

    # Private
    _users_repository = providers.Dependency(UsersRepository).override(
        _data_container.users_repository_impl
    )

    _users_service_impl = providers.Singleton(
        UsersServiceImpl,
        users_repository=_users_repository
    )

    # Public
    users_service = providers.Dependency(AbstractUsersService).override(
        _users_service_impl
    )
