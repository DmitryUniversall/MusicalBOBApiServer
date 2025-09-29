from dependency_injector import providers, containers

from ..data import AuthDataLayerContainer
from ..domain import AbstractAuthSessionRepository, AuthSessionServiceImpl, AbstractAuthSessionService


class AuthComponentContainer(containers.DeclarativeContainer):
    # Private (Dependency-containers)
    _data_container = providers.Container(
        AuthDataLayerContainer
    )

    # Private
    _auth_session_repository = providers.Dependency(AbstractAuthSessionRepository).override(
        _data_container.auth_session_repository_impl
    )

    _auth_session_service_impl = providers.Singleton(
        AuthSessionServiceImpl,
        auth_session_repository=_auth_session_repository
    )

    # Public
    auth_session_service = providers.Dependency(AbstractAuthSessionService).override(
        _auth_session_service_impl
    )
