from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.components.auth.domain import AuthSessionRepositoryI, AuthRepositoryI
from .internal.repositories_impl import AuthSessionRepositoryRedisImpl, AuthRepositoryImpl


class AuthDataContainer(DeclarativeContainer):
    auth_repository = providers.Singleton[AuthRepositoryI](AuthRepositoryImpl)

    auth_session_repository = providers.Singleton[AuthSessionRepositoryI](
        AuthSessionRepositoryRedisImpl,
        auth_repository=auth_repository
    )
