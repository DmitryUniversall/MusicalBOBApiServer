from dependency_injector import containers, providers

from ..internal.repositories import AuthSessionRepositoryRedisImpl


# This container should NOT be imported or used directly. You must use it only through AuthComponentContainer
class AuthDataLayerContainer(containers.DeclarativeContainer):
    # Public
    auth_session_repository_impl = providers.Singleton(AuthSessionRepositoryRedisImpl)
