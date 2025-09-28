from dependency_injector import containers, providers
from ..components.users import UsersComponentContainer

WIRING_MODULES = [
    "src.app.main.components.users"
]


class ApplicationContainer(containers.DeclarativeContainer):
    # Wiring configuration
    wiring_config = containers.WiringConfiguration(modules=WIRING_MODULES)

    # Private (Dependency-containers)
    _users_component_container = providers.Container(UsersComponentContainer)

    # Public
    users_service = _users_component_container.users_service
