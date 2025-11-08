from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from .data import UsersDataContainer
from .domain import UsersServiceI
from .services_impl import UsersServiceImpl


class UsersComponentContainer(DeclarativeContainer):
    # Private
    _data_container = providers.Container[UsersDataContainer](UsersDataContainer)

    # Public
    users_service = providers.Singleton[UsersServiceI](
        UsersServiceImpl,
        users_repository=_data_container.users_repository,
    )
