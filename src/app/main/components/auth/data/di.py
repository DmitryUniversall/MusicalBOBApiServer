from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.app.main.components.auth.data.internal.repositories_impl import AuthSessionRepositoryRedisImpl
from src.app.main.components.auth.domain import AuthSessionRepositoryI


class AuthDataContainer(DeclarativeContainer):
    auth_session_repository = providers.Singleton[AuthSessionRepositoryI](AuthSessionRepositoryRedisImpl)
