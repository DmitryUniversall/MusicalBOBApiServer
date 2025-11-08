from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from .data import AuthDataContainer
from .domain.services.auth_service import AuthServiceI
from .domain.services.auth_session_service import AuthSessionServiceI
from .services_impl.auth_service_impl import AuthServiceImpl
from .services_impl.auth_session_service_impl import AuthSessionServiceImpl
from .utils import HTTPJWTBearerAuthDependency
from ..users import UsersComponentContainer


class AuthComponentContainer(DeclarativeContainer):
    # Private
    _users_container = providers.Container[UsersComponentContainer](UsersComponentContainer)
    _data_container = providers.Container[AuthDataContainer](AuthDataContainer)

    # Public
    auth_session_service = providers.Singleton[AuthSessionServiceI](
        AuthSessionServiceImpl,
        auth_session_repository=_data_container.provided.auth_session_repository
    )

    auth_service = providers.Singleton[AuthServiceI](
        AuthServiceImpl,
        session_service=auth_session_service,
        user_service=_users_container.provided.users_service
    )

    jwt_auth_dependency = providers.Singleton[HTTPJWTBearerAuthDependency](
        HTTPJWTBearerAuthDependency,
        auth_service=auth_service
    )
